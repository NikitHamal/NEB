import json
import shutil
import tempfile
from pathlib import Path
from unittest import mock

from django.test import SimpleTestCase, TestCase, override_settings

from api.background_agent.events import add_message
from api.background_agent.protocol import parse_model_response
from api.background_agent.qwen_harness.catalog import advertised_tools, is_readonly, tools_xml
from api.background_agent.qwen_harness.execute import run_action_batches
from api.background_agent.qwen_harness.observe import compact_tool_content, numbered_view
from api.background_agent.qwen_harness.prompt import build_system_prompt, format_repair_prompt
from api.background_agent.qwen_harness.recover import action_signature, heal_note, needs_format_repair
from api.background_agent.runner import BackgroundAgentRunner
from api.background_agent.workspace import ToolExecutor
from api.test_background_agent import create_api_user
from api.background_agent.crypto import encrypt_secret
from api.models import BackgroundAgentCredential, BackgroundAgentProject, BackgroundAgentSession, BotConfig
from api.utils import now_ms, uuid_str


HERMES_READ = '''<think>Need the file first.</think>
<tool_call>
{"name": "read_file", "arguments": {"path": "src/app.py", "start_line": 1, "end_line": 80}}
</tool_call>'''

HERMES_PARALLEL = '''<tool_call>
{"name": "glob_files", "arguments": {"pattern": "**/*.py"}}
</tool_call>
<tool_call>
{"name": "search_text", "arguments": {"query": "health", "regex": false}}
</tool_call>'''

HERMES_DONE = '''<tool_call>
{"name": "done", "arguments": {"summary": "Added health check and tests."}}
</tool_call>'''

QWEN_FN = '✿FUNCTION✿: list_files\n✿ARGS✿: {"path": ".", "depth": 2}'

FENCE = '''```tool
name: write_file
args:
  path: hello.py
  content: print("hi")
```'''


class QwenProtocolTests(SimpleTestCase):
    def test_legacy_json_envelope_still_parses(self):
        parsed = parse_model_response(
            'before\n```json\n{"thought":"inspect","actions":[{"tool":"list_files","arguments":{}}],"summary":"s"}\n```'
        )
        self.assertTrue(parsed.parse_ok)
        self.assertEqual(parsed.protocol, 'json')
        self.assertEqual(parsed.thought, 'inspect')
        self.assertEqual(parsed.actions[0]['tool'], 'list_files')

    def test_hermes_tool_call_is_primary(self):
        parsed = parse_model_response(HERMES_READ)
        self.assertTrue(parsed.parse_ok)
        self.assertEqual(parsed.protocol, 'hermes')
        self.assertEqual(parsed.actions[0]['tool'], 'read_file')
        self.assertEqual(parsed.actions[0]['arguments']['path'], 'src/app.py')
        self.assertIn('Need the file first', parsed.thought)

    def test_parallel_hermes_calls(self):
        parsed = parse_model_response(HERMES_PARALLEL)
        self.assertEqual([item['tool'] for item in parsed.actions], ['glob_files', 'search_text'])

    def test_done_becomes_final(self):
        parsed = parse_model_response(HERMES_DONE)
        self.assertEqual(parsed.final, 'Added health check and tests.')
        self.assertEqual(parsed.actions, [])
        self.assertTrue(parsed.parse_ok)

    def test_qwen_fn_markers(self):
        parsed = parse_model_response(QWEN_FN)
        self.assertEqual(parsed.protocol, 'qwen_fn')
        self.assertEqual(parsed.actions[0]['tool'], 'list_files')

    def test_tool_fence(self):
        parsed = parse_model_response(FENCE)
        self.assertEqual(parsed.protocol, 'fence')
        self.assertEqual(parsed.actions[0]['tool'], 'write_file')
        self.assertEqual(parsed.actions[0]['arguments']['path'], 'hello.py')

    def test_ask_user_alias(self):
        parsed = parse_model_response('<tool_call>{"name":"ask","arguments":{"question":"Which API?"}}</tool_call>')
        self.assertTrue(parsed.needs_input)
        self.assertEqual(parsed.thought, 'Which API?')
        self.assertEqual(parsed.actions, [])

    def test_prose_is_not_executed(self):
        parsed = parse_model_response('I changed everything successfully.')
        self.assertEqual(parsed.actions, [])
        self.assertTrue(parsed.needs_input)
        self.assertFalse(parsed.final)
        self.assertFalse(parsed.parse_ok)
        self.assertTrue(needs_format_repair(parsed))

    def test_incomplete_tool_call_still_extracts(self):
        parsed = parse_model_response('<tool_call>\n{"name": "git_status", "arguments": {}}\n')
        self.assertEqual(parsed.actions[0]['tool'], 'git_status')

    def test_system_prompt_is_qwen_native(self):
        prompt = build_system_prompt('Qwen 3.8 Max')
        self.assertIn('<tools>', prompt)
        self.assertIn('<tool_call>', prompt)
        self.assertIn('"name": "edit_file"', tools_xml())
        self.assertLessEqual(len(advertised_tools()), 20)
        self.assertTrue(is_readonly('read_file'))
        self.assertFalse(is_readonly('edit_file'))

    def test_observation_is_far_smaller_than_line_json(self):
        lines = [{'line': i, 'text': f'value_{i}'} for i in range(1, 81)]
        bulky = json.dumps({'ok': True, 'tool': 'read_file', 'result': {'path': 'a.py', 'lines': lines, 'totalLines': 80}})
        compact = compact_tool_content(bulky)
        self.assertIn('path: a.py', compact)
        self.assertLess(len(compact), len(bulky) * 0.55)
        self.assertIn('1|', numbered_view('alpha\nbeta', 1, 2))

    def test_heal_note_for_failed_edit(self):
        note = heal_note('edit_file', {'ok': False, 'error': 'old_text was not found'})
        self.assertIn('Re-read', note)
        self.assertEqual(heal_note('read_file', {'ok': True}), '')

    def test_action_signature_detects_repeats(self):
        actions = [{'tool': 'read_file', 'arguments': {'path': 'a.py'}}]
        self.assertEqual(action_signature(actions), action_signature(list(actions)))
        self.assertNotEqual(
            action_signature(actions),
            action_signature([{'tool': 'read_file', 'arguments': {'path': 'b.py'}}]),
        )

    def test_readonly_batches_run_in_order(self):
        seen = []

        def execute_one(action):
            seen.append(action['tool'])
            return action['tool']

        results = run_action_batches([
            {'tool': 'read_file', 'arguments': {}},
            {'tool': 'list_files', 'arguments': {}},
            {'tool': 'edit_file', 'arguments': {}},
            {'tool': 'git_status', 'arguments': {}},
        ], execute_one)
        self.assertEqual(results, ['read_file', 'list_files', 'edit_file', 'git_status'])
        self.assertEqual(seen, ['read_file', 'list_files', 'edit_file', 'git_status'])

    def test_repair_prompt_asks_for_tool_call_xml(self):
        text = format_repair_prompt('TASK', 'here is some prose')
        self.assertIn('<tool_call>', text)
        self.assertIn('PRIOR OUTPUT', text)


class QwenWorkspaceToolTests(TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='qwen-harness-ws-')
        self.settings_override = override_settings(
            BACKGROUND_AGENT_ROOT=Path(self.temp_dir),
            BACKGROUND_AGENT_EXECUTION_BACKEND='local',
            BACKGROUND_AGENT_ALLOW_LOCAL_EXECUTION=False,
        )
        self.settings_override.enable()
        admin = create_api_user('qwen-harness-admin')
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
            repo_full_name='example/qwen',
            clone_url='https://github.com/example/qwen.git',
            default_branch='main',
            created_at=now_ms(),
            updated_at=now_ms(),
        )
        session = BackgroundAgentSession.objects.create(
            id=uuid_str(),
            project=project,
            admin_user=admin,
            goal='Harness workspace tools',
            source_branch='main',
            work_branch='nebians-agent/qwen-harness',
            created_at=now_ms(),
            updated_at=now_ms(),
        )
        from api.background_agent.workspace import GitWorkspace
        self.workspace = GitWorkspace(project, session)
        self.workspace.ensure_dirs()
        self.workspace.worktree.mkdir(parents=True, exist_ok=True)
        (self.workspace.worktree / 'src').mkdir()
        (self.workspace.worktree / 'src' / 'app.py').write_text('def health():\n    return True\n', encoding='utf-8')
        (self.workspace.worktree / 'README.md').write_text('hello\n', encoding='utf-8')
        self.tools = ToolExecutor(self.workspace)

    def tearDown(self):
        self.settings_override.disable()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_glob_and_regex_search(self):
        found = self.tools.glob_files('**/*.py')
        self.assertIn('src/app.py', found['matches'])
        hits = self.tools.search_text(r'def\s+health', regex=True, glob='*.py')
        self.assertTrue(hits['matches'])
        self.assertTrue(any('app.py' in row for row in hits['matches']))

    def test_read_file_includes_numbered_view(self):
        result = self.tools.read_file('src/app.py')
        self.assertIn('view', result)
        self.assertIn('|def health():', result['view'])


class QwenRunnerHermesTests(TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='qwen-harness-runner-')
        self.settings_override = override_settings(
            BACKGROUND_AGENT_ROOT=Path(self.temp_dir) / 'agent-data',
            BACKGROUND_AGENT_EXECUTION_BACKEND='local',
            BACKGROUND_AGENT_ALLOW_LOCAL_EXECUTION=False,
            BACKGROUND_AGENT_PROVIDER_ATTEMPTS=1,
            BACKGROUND_AGENT_QWEN_HARNESS=True,
        )
        self.settings_override.enable()
        import subprocess
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
        admin = create_api_user('qwen-runner-admin')
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
            repo_full_name='example/qwen-local',
            clone_url=str(self.remote),
            default_branch='main',
            preferred_base_branch='main',
            created_at=now_ms(),
            updated_at=now_ms(),
        )
        provider = BotConfig.objects.create(
            name='Qwen 3.8 Max',
            enabled=True,
            bot_username='qwen-harness-provider',
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
            llm_provider='qwen',
            llm_model='qwen3.8-max',
            created_at=now_ms(),
            updated_at=now_ms(),
        )
        add_message(self.session, 'user', self.session.goal)

    def tearDown(self):
        self.settings_override.disable()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @mock.patch('api.background_agent.runner.qwen_proxy.call_qwen')
    def test_hermes_turn_completes_a_session(self, call_qwen):
        call_qwen.side_effect = [
            json.dumps({'branch': 'health-check-module', 'description': 'Adds a health check module'}),
            '''<tool_call>
{"name": "write_file", "arguments": {"path": "health.py", "content": "def health():\\n    return {\\"ok\\": True}\\n"}}
</tool_call>''',
            '''<tool_call>
{"name": "done", "arguments": {"summary": "Added a minimal health check module."}}
</tool_call>''',
        ]
        BackgroundAgentRunner(self.session).run()
        self.session.refresh_from_db()
        self.assertEqual(self.session.status, 'completed')
        self.assertEqual(self.session.work_branch, 'health-check-module')
        self.assertIn('health.py', json.loads(self.session.changed_files))
        system_prompt = call_qwen.call_args_list[1].kwargs['system_prompt']
        self.assertIn('<tools>', system_prompt)
        self.assertIn('<tool_call>', system_prompt)
        user_prompt = call_qwen.call_args_list[2].kwargs.get('user_message') or ''
        self.assertIn('<tool_response>', user_prompt)
