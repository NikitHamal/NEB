import json
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path
from unittest import mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, SimpleTestCase, TestCase, override_settings
from django.urls import reverse

from api.background_agent.attachments import qwen_files_for_iteration, prompt_attachment_block, save_uploads
from api.background_agent.context import COMPACTION_SYSTEM_PROMPT, SUMMARY_STRUCTURE, compact_if_needed
from api.background_agent.crypto import decrypt_secret, encrypt_secret
from api.background_agent.events import add_message
from api.background_agent.runner import BackgroundAgentRunner, parse_model_response
from api.background_agent.workspace import GitWorkspace, ToolExecutor, WorkspaceError, build_branch_name
from api.models import (
    BackgroundAgentCredential,
    BackgroundAgentProject,
    BackgroundAgentSession,
    BotConfig,
    User,
)
from api.security import hash_password, issue_auth_token
from api.utils import now_ms, uuid_str


def create_api_user(username, *, is_admin=True):
    return User.objects.create(
        id=uuid_str(),
        username=username,
        email=f'{username}@example.com',
        display_name=username.replace('-', ' ').title(),
        password_hash=hash_password('secret-password'),
        is_admin=is_admin,
        created_at=now_ms(),
    )


def login_background_admin(client, user):
    raw_token = issue_auth_token(user)
    session = client.session
    session['auth_token'] = raw_token
    session.save()


class BackgroundAgentProtocolTests(SimpleTestCase):
    def test_encrypted_credential_round_trip_and_tamper_detection(self):
        encrypted = encrypt_secret('github-secret-token')
        self.assertNotIn('github-secret-token', encrypted)
        self.assertEqual(decrypt_secret(encrypted), 'github-secret-token')
        with self.assertRaises(ValueError):
            decrypt_secret(encrypted[:-2] + 'AA')

    def test_model_json_protocol_accepts_fenced_json(self):
        parsed = parse_model_response('before\n```json\n{"thought":"inspect","actions":[{"tool":"list_files","arguments":{}}],"summary":"s"}\n```')
        self.assertEqual(parsed.thought, 'inspect')
        self.assertEqual(parsed.actions[0]['tool'], 'list_files')
        self.assertEqual(parsed.summary, 's')

    def test_model_json_protocol_repairs_nested_json_and_trailing_commas(self):
        parsed = parse_model_response(
            'analysis first {"thought":"edit","actions":[{"tool":"write_file","arguments":{"path":"a.json","content":"{\\"ok\\": true}"},}],"summary":"next",}'
        )
        self.assertEqual(parsed.thought, 'edit')
        self.assertEqual(parsed.actions[0]['arguments']['path'], 'a.json')
        self.assertEqual(parsed.actions[0]['arguments']['content'], '{"ok": true}')

    def test_non_json_provider_output_is_not_executed(self):
        parsed = parse_model_response('I changed everything successfully.')
        self.assertEqual(parsed.actions, [])
        self.assertTrue(parsed.needs_input)
        self.assertFalse(parsed.final)

    def test_generated_branch_never_uses_the_base_branch(self):
        branch = build_branch_name('Fix OAuth callback & tests', 'abcdef12-1234')
        self.assertEqual(branch, 'nebians-agent/fix-oauth-callback-tests-abcdef12')
        self.assertNotEqual(branch, 'main')


class BackgroundAgentWorkspaceTests(TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='background-agent-tests-')
        self.settings_override = override_settings(
            BACKGROUND_AGENT_ROOT=Path(self.temp_dir),
            BACKGROUND_AGENT_EXECUTION_BACKEND='local',
            BACKGROUND_AGENT_ALLOW_LOCAL_EXECUTION=False,
        )
        self.settings_override.enable()
        self.admin = create_api_user('agent-admin')
        self.credential = BackgroundAgentCredential.objects.create(
            admin_user=self.admin,
            encrypted_access_token=encrypt_secret('token'),
            created_at=now_ms(),
            updated_at=now_ms(),
        )
        self.project = BackgroundAgentProject.objects.create(
            id=uuid_str(),
            admin_user=self.admin,
            credential=self.credential,
            repo_full_name='example/repo',
            clone_url='https://github.com/example/repo.git',
            default_branch='main',
            preferred_base_branch='main',
            created_at=now_ms(),
            updated_at=now_ms(),
        )
        self.session = BackgroundAgentSession.objects.create(
            id=uuid_str(),
            project=self.project,
            admin_user=self.admin,
            goal='Update the repository safely',
            source_branch='main',
            work_branch='nebians-agent/test-12345678',
            created_at=now_ms(),
            updated_at=now_ms(),
        )
        self.workspace = GitWorkspace(self.project, self.session)
        self.workspace.ensure_dirs()
        self.workspace.worktree.mkdir(parents=True, exist_ok=True)
        self._git('init', '-b', 'main')
        self._git('config', 'user.name', 'Test')
        self._git('config', 'user.email', 'test@example.com')
        (self.workspace.worktree / 'README.md').write_text('original\n', encoding='utf-8')
        (self.workspace.worktree / 'delete-me.txt').write_text('remove\n', encoding='utf-8')
        self._git('add', '.')
        self._git('commit', '-m', 'initial')
        self.session.base_sha = self._git('rev-parse', 'HEAD').stdout.strip()
        self.session.head_sha = self.session.base_sha
        self.session.workspace_path = str(self.workspace.worktree)
        self.session.save(update_fields=['base_sha', 'head_sha', 'workspace_path'])

    def tearDown(self):
        self.settings_override.disable()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _git(self, *args):
        return subprocess.run(
            ['git', *args],
            cwd=self.workspace.worktree,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_workspace_jail_rejects_escape_and_git_metadata(self):
        self.assertIsNone(self.workspace.safe_path('../outside.txt'))
        self.assertIsNone(self.workspace.safe_path('.git/config'))
        self.assertEqual(self.workspace.safe_path('src/new.py'), self.workspace.worktree / 'src/new.py')

    def test_diff_changed_files_and_zip_include_untracked_and_deleted_entries(self):
        (self.workspace.worktree / 'README.md').write_text('updated\n', encoding='utf-8')
        (self.workspace.worktree / 'new.py').write_text('print("ok")\n', encoding='utf-8')
        (self.workspace.worktree / 'delete-me.txt').unlink()

        changed = self.workspace.changed_files()
        self.assertEqual(set(changed), {'README.md', 'new.py', 'delete-me.txt'})
        diff = self.workspace.diff()
        self.assertIn('README.md', diff)
        self.assertIn('new.py', diff)
        self.assertIn('delete-me.txt', diff)

        result = self.workspace.build_artifacts()
        with zipfile.ZipFile(result['zipPath']) as archive:
            names = set(archive.namelist())
            self.assertIn('BACKGROUND_AGENT_MANIFEST.json', names)
            self.assertIn('changes.patch', names)
            self.assertIn('README.md', names)
            self.assertIn('new.py', names)
            self.assertNotIn('delete-me.txt', names)
            manifest = json.loads(archive.read('BACKGROUND_AGENT_MANIFEST.json'))
            self.assertEqual(set(manifest['changedFiles']), set(changed))
        self.assertEqual(self.session.artifacts.count(), 2)

    def test_local_command_execution_is_secure_by_default(self):
        executor = ToolExecutor(self.workspace)
        with self.assertRaises(WorkspaceError):
            executor.run_command(['python', '--version'])

    def test_secret_files_are_hidden_from_tools_diffs_and_artifacts(self):
        (self.workspace.worktree / '.env').write_text('SUPER_SECRET=do-not-send\n', encoding='utf-8')
        (self.workspace.worktree / '.env.example').write_text('SUPER_SECRET=placeholder\n', encoding='utf-8')
        (self.workspace.worktree / 'visible.txt').write_text('find-me\n', encoding='utf-8')
        executor = ToolExecutor(self.workspace)

        listing = executor.list_files('.', depth=2)['entries']
        self.assertNotIn('.env', listing)
        self.assertIn('.env.example', listing)
        self.assertIn('visible.txt', listing)
        with self.assertRaises(WorkspaceError):
            executor.read_file('.env')
        self.assertEqual(executor.search_text('do-not-send')['matches'], [])
        self.assertTrue(executor.search_text('find-me')['matches'])

        changed = self.workspace.changed_files()
        self.assertNotIn('.env', changed)
        self.assertIn('.env.example', changed)
        self.assertNotIn('do-not-send', self.workspace.diff())
        result = self.workspace.build_artifacts()
        with zipfile.ZipFile(result['zipPath']) as archive:
            self.assertNotIn('.env', archive.namelist())
            self.assertNotIn(b'do-not-send', archive.read('changes.patch'))

    def test_patch_tool_rejects_credentials_and_path_escape(self):
        executor = ToolExecutor(self.workspace)
        secret_patch = '''diff --git a/.env b/.env
new file mode 100644
--- /dev/null
+++ b/.env
@@ -0,0 +1 @@
+TOKEN=secret
'''
        escape_patch = '''diff --git a/../outside.txt b/../outside.txt
new file mode 100644
--- /dev/null
+++ b/../outside.txt
@@ -0,0 +1 @@
+outside
'''
        with self.assertRaises(WorkspaceError):
            executor.apply_patch(secret_patch)
        with self.assertRaises(WorkspaceError):
            executor.apply_patch(escape_patch)


class BackgroundAgentContextAndAttachmentTests(TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='background-agent-context-')
        self.settings_override = override_settings(
            BACKGROUND_AGENT_ROOT=Path(self.temp_dir),
            BACKGROUND_AGENT_CONTEXT_WINDOW_TOKENS=16000,
            BACKGROUND_AGENT_CONTEXT_COMPACTION_THRESHOLD=0.50,
            BACKGROUND_AGENT_MAX_ATTACHMENTS=5,
        )
        self.settings_override.enable()
        self.admin = create_api_user('context-admin')
        credential = BackgroundAgentCredential.objects.create(
            admin_user=self.admin,
            encrypted_access_token=encrypt_secret('token'),
            created_at=now_ms(),
            updated_at=now_ms(),
        )
        project = BackgroundAgentProject.objects.create(
            id=uuid_str(),
            admin_user=self.admin,
            credential=credential,
            repo_full_name='example/context',
            clone_url='https://github.com/example/context.git',
            default_branch='main',
            created_at=now_ms(),
            updated_at=now_ms(),
        )
        self.session = BackgroundAgentSession.objects.create(
            id=uuid_str(),
            project=project,
            admin_user=self.admin,
            goal='Use context and files',
            source_branch='main',
            context_window_tokens=16000,
            created_at=now_ms(),
            updated_at=now_ms(),
        )

    def tearDown(self):
        self.settings_override.disable()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_attachments_are_persisted_exposed_to_prompt_and_sent_once(self):
        message = add_message(self.session, 'user', 'Inspect this specification')
        rows = save_uploads(self.session, message, [
            SimpleUploadedFile('requirements.md', b'# Requirements\nBuild the viewer.\n', content_type='text/markdown'),
            SimpleUploadedFile('reference.png', b'\x89PNG\r\n\x1a\nnot-a-real-image', content_type='image/png'),
        ])
        self.assertEqual(len(rows), 2)
        block = prompt_attachment_block(message)
        self.assertIn('requirements.md', block)
        self.assertIn('Build the viewer.', block)
        paths, pending = qwen_files_for_iteration(self.session)
        self.assertEqual(len(paths), 1)
        self.assertEqual([row.file_name for row in pending], ['reference.png'])

    def test_context_compacts_at_threshold_with_exact_system_prompt(self):
        for index in range(10):
            add_message(self.session, 'user' if index % 2 == 0 else 'assistant', f'message-{index}\n' + ('x' * 5000))
        compact_call = mock.Mock(return_value=SUMMARY_STRUCTURE + '\n- preserved state')
        snapshot = compact_if_needed(self.session, 'fixed task prompt', compact_call)
        self.session.refresh_from_db()
        self.assertEqual(compact_call.call_count, 1)
        self.assertEqual(compact_call.call_args.args[0], COMPACTION_SYSTEM_PROMPT)
        self.assertIn('<conversation-history>', compact_call.call_args.args[1])
        self.assertEqual(self.session.context_compactions, 1)
        self.assertIn('# Goal', self.session.context_summary)
        self.assertLess(snapshot.estimated_tokens, snapshot.threshold_tokens)


class BackgroundAgentRunnerIntegrationTests(TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='background-agent-runner-')
        self.settings_override = override_settings(
            BACKGROUND_AGENT_ROOT=Path(self.temp_dir) / 'agent-data',
            BACKGROUND_AGENT_EXECUTION_BACKEND='local',
            BACKGROUND_AGENT_ALLOW_LOCAL_EXECUTION=False,
            BACKGROUND_AGENT_PROVIDER_ATTEMPTS=1,
        )
        self.settings_override.enable()
        source = Path(self.temp_dir) / 'source'
        source.mkdir()
        subprocess.run(['git', 'init', '-b', 'main'], cwd=source, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(['git', 'config', 'user.name', 'Test'], cwd=source, check=True)
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=source, check=True)
        (source / 'README.md').write_text('hello\n', encoding='utf-8')
        subprocess.run(['git', 'add', '.'], cwd=source, check=True)
        subprocess.run(['git', 'commit', '-m', 'initial'], cwd=source, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.remote = Path(self.temp_dir) / 'remote.git'
        subprocess.run(['git', 'clone', '--bare', str(source), str(self.remote)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        admin = create_api_user('runner-admin')
        credential = BackgroundAgentCredential.objects.create(
            admin_user=admin,
            encrypted_access_token=encrypt_secret('token'),
            created_at=now_ms(),
            updated_at=now_ms(),
        )
        project = BackgroundAgentProject.objects.create(
            id=uuid_str(),
            admin_user=admin,
            credential=credential,
            repo_full_name='example/local-repo',
            clone_url=str(self.remote),
            default_branch='main',
            preferred_base_branch='main',
            created_at=now_ms(),
            updated_at=now_ms(),
        )
        provider = BotConfig.objects.create(
            name='Qwen 3.8 Max',
            enabled=True,
            bot_username='runner-background-agent-provider',
            provider='qwen',
            model='qwen3.8-max',
        )
        self.session = BackgroundAgentSession.objects.create(
            id=uuid_str(),
            project=project,
            admin_user=admin,
            bot_config=provider,
            goal='Create a health check module in the repository.',
            source_branch='main',
            status='queued',
            max_iterations=5,
            created_at=now_ms(),
            updated_at=now_ms(),
        )
        add_message(self.session, 'user', self.session.goal)

    def tearDown(self):
        self.settings_override.disable()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @mock.patch('api.background_agent.runner.qwen_proxy.call_qwen')
    def test_runner_clones_branches_edits_and_completes_durably(self, call_qwen):
        call_qwen.side_effect = [
            json.dumps({
                'branch': 'health-check-module',
                'description': 'Adds a health check module to the repository',
            }),
            json.dumps({
                'thought': 'Create the requested module.',
                'actions': [{
                    'tool': 'write_file',
                    'arguments': {'path': 'health.py', 'content': 'def health():\n    return {"ok": True}\n'},
                }],
                'summary': 'Health module created.',
            }),
            json.dumps({
                'thought': 'The change is complete.',
                'actions': [],
                'final': 'Added a minimal health check module.',
                'summary': 'Complete.',
            }),
        ]

        BackgroundAgentRunner(self.session).run()
        self.session.refresh_from_db()
        self.assertEqual(self.session.status, 'completed')
        self.assertEqual(self.session.work_branch, 'health-check-module')
        self.assertNotEqual(self.session.work_branch, 'main')
        self.assertEqual(self.session.agent_state and json.loads(self.session.agent_state).get('branchDescription'),
                         'Adds a health check module to the repository')
        self.assertIn('health.py', json.loads(self.session.changed_files))
        self.assertIn('health.py', self.session.final_diff)
        self.assertEqual(self.session.artifacts.count(), 2)
        self.assertEqual(call_qwen.call_count, 3)
        for invocation in call_qwen.call_args_list:
            self.assertEqual(invocation.kwargs['model'], 'qwen3.8-max')

    def test_parse_branch_response_rejects_invalid_names(self):
        from api.background_agent.runner import BackgroundAgentRunner
        good = BackgroundAgentRunner._parse_branch_response(
            '{"branch": "OAuth Token Refresh!", "description": "Fixes the refresh flow."}',
            'fallback-branch',
        )
        self.assertEqual(good, ('oauth-token-refresh', 'Fixes the refresh flow.'))
        self.assertEqual(
            BackgroundAgentRunner._parse_branch_response('{"branch": "with/slash"}', 'fallback-branch'),
            ('with-slash', ''),
        )
        self.assertEqual(
            BackgroundAgentRunner._parse_branch_response('{"branch": "UPPER-CASE"}', 'fallback-branch'),
            ('upper-case', ''),
        )
        for bad in ('{"branch": "main"}', '{"branch": ""}', 'not json', '{"branch": "a"}'):
            with self.assertRaises(Exception):
                BackgroundAgentRunner._parse_branch_response(bad, 'fallback-branch')


class BackgroundAgentAdminViewTests(TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='background-agent-view-')
        self.settings_override = override_settings(BACKGROUND_AGENT_ROOT=Path(self.temp_dir))
        self.settings_override.enable()
        self.admin = create_api_user('admin')
        self.other_admin = create_api_user('other')
        self.member = create_api_user('member', is_admin=False)
        self.credential = BackgroundAgentCredential.objects.create(
            admin_user=self.admin,
            encrypted_access_token=encrypt_secret('token'),
            github_login='admin-github',
            created_at=now_ms(),
            updated_at=now_ms(),
        )
        self.project = BackgroundAgentProject.objects.create(
            id=uuid_str(),
            admin_user=self.admin,
            credential=self.credential,
            repo_full_name='example/repo',
            clone_url='https://github.com/example/repo.git',
            default_branch='main',
            preferred_base_branch='main',
            created_at=now_ms(),
            updated_at=now_ms(),
        )
        self.provider = BotConfig.objects.create(
            name='Qwen 3.8 Max',
            enabled=True,
            bot_username='test-background-agent-provider',
            provider='qwen',
            model='qwen3.8-max',
        )

    def tearDown(self):
        self.settings_override.disable()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_page_is_platform_admin_only(self):
        url = reverse('web:background_agent')
        self.assertEqual(Client().get(url).status_code, 302)
        member_client = Client()
        login_background_admin(member_client, self.member)
        self.assertEqual(member_client.get(url).status_code, 302)
        admin_client = Client()
        raw_token = issue_auth_token(self.admin)
        session = admin_client.session
        session['auth_token'] = raw_token
        session.save()
        self.assertEqual(admin_client.get(url).status_code, 200)
        self.assertEqual(admin_client.get(reverse('web:background_agent_login')).url, url)


    @override_settings(GITHUB_CLIENT_ID='test-github-client', GITHUB_CLIENT_SECRET='test-secret')
    @mock.patch('web.views_auth.store_background_agent_github', return_value=('octocat', None))
    def test_github_oauth_state_is_bound_to_the_signed_in_admin_session(self, exchange):
        client = Client()
        login_background_admin(client, self.admin)
        connect = client.get(reverse('web:background_agent_github_connect'))
        self.assertEqual(connect.status_code, 302)
        state = client.session.get('background_agent_github_oauth_state')
        self.assertTrue(state and state.startswith('bg::'))

        callback = client.get(reverse('web:github_callback'), {'state': state, 'code': 'oauth-code'})
        self.assertEqual(callback.status_code, 302)
        exchange.assert_called_once()
        self.assertEqual(exchange.call_args.args[0], self.admin)
        self.assertEqual(exchange.call_args.kwargs['code'], 'oauth-code')

        replay = client.get(reverse('web:github_callback'), {'state': state, 'code': 'oauth-code'})
        self.assertEqual(replay.status_code, 403)

    def test_admin_can_queue_session_with_attachment_and_other_admin_cannot_read_it(self):
        client = Client()
        login_background_admin(client, self.admin)
        response = client.post(
            reverse('web:background_agent_create_session'),
            data={
                'projectId': self.project.id,
                'goal': 'Add a complete production-ready health check endpoint and tests.',
                'sourceBranch': 'main',
                'files': SimpleUploadedFile('brief.md', b'# Brief\nUse Django.\n', content_type='text/markdown'),
            },
        )
        self.assertEqual(response.status_code, 201, response.content)
        session_id = response.json()['session']['id']
        session = BackgroundAgentSession.objects.get(pk=session_id)
        self.assertEqual(session.status, 'queued')
        self.assertEqual(session.bot_config, self.provider)
        self.assertEqual(session.messages.filter(role='user').count(), 1)
        self.assertEqual(session.attachments.count(), 1)

        files_response = client.get(reverse('web:background_agent_session_files', args=[session_id]))
        self.assertEqual(files_response.status_code, 200)
        self.assertEqual(files_response.json()['files'], [])

        attachment = session.attachments.get()
        file_response = client.get(
            reverse('web:background_agent_session_file', args=[session_id]),
            {'attachment': attachment.id},
        )
        self.assertEqual(file_response.status_code, 200)
        self.assertEqual(file_response.json()['file']['name'], 'brief.md')
        self.assertIn('Use Django.', file_response.json()['file']['content'])

        preview_response = client.get(
            reverse('web:background_agent_session_preview', args=[session_id]),
            {'attachment': attachment.id},
        )
        self.assertEqual(preview_response.status_code, 200)
        self.assertTrue(preview_response['Content-Type'].startswith('text/plain'))
        self.assertIn('sandbox', preview_response['Content-Security-Policy'])

        other = Client()
        login_background_admin(other, self.other_admin)
        detail = reverse('web:background_agent_session_detail', args=[session_id])
        self.assertEqual(other.get(detail).status_code, 404)

    def test_admin_can_archive_restore_and_delete_finished_session(self):
        session = BackgroundAgentSession.objects.create(
            id=uuid_str(),
            project=self.project,
            admin_user=self.admin,
            bot_config=self.provider,
            title='Finished task',
            goal='Finish the requested production task safely.',
            source_branch='main',
            status='completed',
            created_at=now_ms(),
            updated_at=now_ms(),
        )
        client = Client()
        login_background_admin(client, self.admin)
        url = reverse('web:background_agent_session_lifecycle', args=[session.id])

        archived = client.post(url, data=json.dumps({'action': 'archive'}), content_type='application/json')
        self.assertEqual(archived.status_code, 200)
        session.refresh_from_db()
        self.assertGreater(session.archived_at, 0)

        restored = client.post(url, data=json.dumps({'action': 'restore'}), content_type='application/json')
        self.assertEqual(restored.status_code, 200)
        session.refresh_from_db()
        self.assertEqual(session.archived_at, 0)

        deleted = client.delete(url)
        self.assertEqual(deleted.status_code, 200)
        self.assertFalse(BackgroundAgentSession.objects.filter(pk=session.id).exists())
