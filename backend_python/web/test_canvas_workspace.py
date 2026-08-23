import json
from unittest import mock

from django.test import Client, TestCase

from api.models import CanvasBoard, CanvasNode, CanvasSnapshot, User
from api.utils import now_ms, uuid_str


class CanvasWorkspaceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            id=uuid_str(), username='canvas_owner', email='canvas@example.com',
            email_verified=True, display_name='Canvas Owner', is_admin=True,
            created_at=now_ms(),
        )
        self.client = Client()
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

    def _board(self, title='Test Canvas'):
        return CanvasBoard.objects.create(
            id=uuid_str(), user=self.user, title=title,
            created_at=now_ms(), updated_at=now_ms(),
        )

    def _node(self, board, title='Card', parent=None, kind='note'):
        return CanvasNode.objects.create(
            id=uuid_str(), board=board, parent=parent, user=self.user,
            prompt='', title=title,
            content=json.dumps({'title': title, 'summary': title, 'sections': []}),
            status='done', x=100, y=120, kind=kind,
            metadata='{}', created_at=now_ms(), updated_at=now_ms(),
        )

    def test_template_creates_structured_board(self):
        response = self.client.post(
            '/ajax/canvas/templates/create/',
            data=json.dumps({'template': 'exam-sprint', 'title': 'Physics Sprint'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data['board']['title'], 'Physics Sprint')
        self.assertGreaterEqual(len(data['nodes']), 4)
        board = CanvasBoard.objects.get(pk=data['board']['id'])
        self.assertEqual(board.user_id, self.user.id)
        self.assertEqual(CanvasNode.objects.filter(board=board).count(), len(data['nodes']))

    def test_manual_note_can_be_typed_tagged_and_pinned(self):
        board = self._board()
        response = self.client.post(
            f'/ajax/canvas/boards/{board.id}/notes/',
            data=json.dumps({
                'title': 'My insight', 'body': 'A compact explanation', 'kind': 'decision',
                'x': 30, 'y': 40, 'meta': {'color': 'purple', 'tags': ['exam', 'priority'], 'pinned': True},
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 201)
        node_id = response.json()['node']['id']
        update = self.client.post(
            f'/ajax/canvas/nodes/{node_id}/update/',
            data=json.dumps({'title': 'Decision point', 'body': 'Updated body', 'kind': 'question', 'meta': {'color': 'amber', 'tags': ['review'], 'pinned': False}}),
            content_type='application/json',
        )
        self.assertEqual(update.status_code, 200)
        payload = update.json()['node']
        self.assertEqual(payload['kind'], 'question')
        self.assertEqual(payload['meta']['color'], 'amber')
        self.assertEqual(payload['meta']['tags'], ['review'])
        self.assertFalse(payload['meta']['pinned'])

    def test_checkpoint_restore_preserves_previous_graph(self):
        board = self._board()
        first = self._node(board, 'Original')
        snapshot = self.client.post(
            f'/ajax/canvas/boards/{board.id}/snapshots/create/',
            data=json.dumps({'label': 'Before experiment'}),
            content_type='application/json',
        )
        self.assertEqual(snapshot.status_code, 201)
        snapshot_id = snapshot.json()['snapshot']['id']
        first.title = 'Changed'
        first.save(update_fields=['title'])
        self._node(board, 'Extra')
        restored = self.client.post(
            f'/ajax/canvas/boards/{board.id}/snapshots/{snapshot_id}/restore/',
            data='{}', content_type='application/json',
        )
        self.assertEqual(restored.status_code, 200)
        self.assertEqual(len(restored.json()['nodes']), 1)
        self.assertEqual(restored.json()['nodes'][0]['title'], 'Original')
        self.assertGreaterEqual(CanvasSnapshot.objects.filter(board=board).count(), 2)

    def test_shared_canvas_can_be_cloned_without_linking_source_nodes(self):
        source_owner = User.objects.create(id=uuid_str(), username='source_owner', email_verified=True, created_at=now_ms())
        source = CanvasBoard.objects.create(
            id=uuid_str(), user=source_owner, title='Shared Map', share_token='shared-token-123',
            settings=json.dumps({'layout': 'radial'}), created_at=now_ms(), updated_at=now_ms(),
        )
        original = CanvasNode.objects.create(
            id=uuid_str(), board=source, user=source_owner, prompt='Why?', title='Source card',
            content=json.dumps({'title': 'Source card', 'summary': 'Shared', 'sections': []}),
            status='done', x=10, y=20, kind='source', metadata='{}', created_at=now_ms(), updated_at=now_ms(),
        )
        response = self.client.post('/ajax/canvas/shared/shared-token-123/clone/', data='{}', content_type='application/json')
        self.assertEqual(response.status_code, 201)
        cloned = CanvasBoard.objects.get(pk=response.json()['board']['id'])
        cloned_node = CanvasNode.objects.get(board=cloned)
        self.assertEqual(cloned.user_id, self.user.id)
        self.assertEqual(cloned_node.title, original.title)
        self.assertNotEqual(cloned_node.id, original.id)
        self.assertEqual(json.loads(cloned.settings)['layout'], 'radial')

    @mock.patch('web.views_canvas_features.generate_plan')
    def test_neby_explore_adds_board_aware_graph_and_checkpoint(self, generate_plan):
        board = self._board('World Models')
        anchor = self._node(board, 'World model', kind='ai')
        generate_plan.return_value = ({
            'summary': 'Added mechanism and retrieval branches.',
            'nodes': [
                {'key': 'mechanism', 'parent': 'anchor', 'title': 'Mechanism', 'prompt': 'How does it work?', 'kind': 'ai', 'summary': 'Mechanism summary', 'sections': []},
                {'key': 'practice', 'parent': 'mechanism', 'title': 'Practice', 'prompt': 'Test me', 'kind': 'practice', 'summary': 'Recall practice', 'sections': []},
                {'key': 'limits', 'parent': 'anchor', 'title': 'Limits', 'prompt': 'Where does it fail?', 'kind': 'comparison', 'summary': 'Failure modes', 'sections': []},
            ],
            'nextQuestions': ['What evidence supports this?'],
        }, 'test-provider')
        response = self.client.post(
            f'/ajax/canvas/boards/{board.id}/neby-explore/',
            data=json.dumps({'goal': 'Deepen my understanding', 'anchorId': anchor.id}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['nodes']), 3)
        self.assertEqual(response.json()['provider'], 'test-provider')
        self.assertTrue(CanvasSnapshot.objects.filter(board=board, label='Before Neby Explore').exists())
        self.assertEqual(CanvasNode.objects.filter(board=board).count(), 4)

    def test_import_rejects_oversized_payload_before_database_work(self):
        board = self._board()
        huge = {'schema': 'nebians-canvas-v2', 'board': {'title': 'Huge'}, 'nodes': [], 'padding': 'x' * (4 * 1024 * 1024)}
        response = self.client.post(
            f'/ajax/canvas/boards/{board.id}/import/',
            data=json.dumps(huge), content_type='application/json',
        )
        self.assertEqual(response.status_code, 413)

    def test_legacy_generation_endpoint_enforces_card_limit_before_llm(self):
        board = self._board()
        now = now_ms()
        CanvasNode.objects.bulk_create([
            CanvasNode(
                id=uuid_str(), board=board, user=self.user, prompt='', title=f'N{i}', content='{}',
                status='done', x=i, y=i, kind='note', metadata='{}', created_at=now + i, updated_at=now + i,
            )
            for i in range(240)
        ])
        response = self.client.post(
            f'/ajax/canvas/boards/{board.id}/nodes/',
            data=json.dumps({'prompt': 'One more'}), content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('240', response.json()['error'])
