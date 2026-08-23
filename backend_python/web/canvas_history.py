import json

from django.db import transaction

from api.models import CanvasNode, CanvasSnapshot
from api.utils import now_ms, uuid_str


MAX_SNAPSHOTS = 24
MAX_IMPORT_NODES = 240
ALLOWED_KINDS = {'ai', 'note', 'question', 'source', 'comparison', 'practice', 'summary', 'task', 'decision', 'warning'}
ALLOWED_COLORS = {'default', 'blue', 'green', 'amber', 'rose', 'purple', 'slate'}


def _json_dict(raw):
    try:
        value = json.loads(raw or '{}')
        return value if isinstance(value, dict) else {}
    except (TypeError, ValueError):
        return {}


def node_record(node):
    return {
        'id': str(node.id),
        'parentId': str(node.parent_id or ''),
        'prompt': node.prompt or '',
        'title': node.title or '',
        'content': _json_dict(node.content),
        'status': node.status,
        'x': node.x,
        'y': node.y,
        'webSearchEnabled': bool(node.web_search_enabled),
        'modelUsed': node.model_used or '',
        'kind': node.kind or 'ai',
        'meta': _json_dict(node.metadata),
        'error': node.error or '',
        'createdAt': node.created_at,
        'updatedAt': node.updated_at,
    }


def board_payload(board):
    nodes = list(CanvasNode.objects.filter(board=board).order_by('created_at'))
    return {
        'schema': 'nebians-canvas-v2',
        'board': {
            'id': str(board.id),
            'title': board.title,
            'settings': _json_dict(board.settings),
            'createdAt': board.created_at,
            'updatedAt': board.updated_at,
        },
        'nodes': [node_record(node) for node in nodes],
    }


def snapshot_board(board, user, label='Checkpoint'):
    payload = board_payload(board)
    snap = CanvasSnapshot.objects.create(
        id=uuid_str(),
        board=board,
        user=user,
        label=(label or 'Checkpoint').strip()[:120] or 'Checkpoint',
        payload=json.dumps(payload, ensure_ascii=False),
        created_at=now_ms(),
    )
    old_ids = list(CanvasSnapshot.objects.filter(board=board).order_by('-created_at').values_list('id', flat=True)[MAX_SNAPSHOTS:])
    if old_ids:
        CanvasSnapshot.objects.filter(id__in=old_ids).delete()
    return snap


def snapshot_summary(snapshot):
    node_count = 0
    try:
        payload = json.loads(snapshot.payload or '{}')
        node_count = len(payload.get('nodes') or [])
    except (TypeError, ValueError):
        pass
    return {
        'id': snapshot.id,
        'label': snapshot.label,
        'createdAt': snapshot.created_at,
        'nodeCount': node_count,
    }


def restore_snapshot(snapshot, user):
    payload = json.loads(snapshot.payload or '{}')
    return replace_board_from_payload(snapshot.board, user, payload, snapshot_label='Before restore')


def replace_board_from_payload(board, user, payload, snapshot_label='Before import'):
    nodes = payload.get('nodes') if isinstance(payload, dict) else None
    if not isinstance(nodes, list):
        raise ValueError('Invalid canvas file')
    if len(nodes) > MAX_IMPORT_NODES:
        raise ValueError(f'Canvas files are limited to {MAX_IMPORT_NODES} cards')
    with transaction.atomic():
        current_nodes = CanvasNode.objects.filter(board=board)
        if current_nodes.exists():
            snapshot_board(board, user, snapshot_label)
        current_nodes.delete()
        now = now_ms()
        id_map = {}
        clean = []
        for item in nodes:
            if not isinstance(item, dict):
                continue
            incoming = str(item.get('id') or uuid_str())[:36]
            new_id = uuid_str()
            id_map[incoming] = new_id
            clean.append((incoming, new_id, item))
        objects = []
        for incoming, new_id, item in clean:
            parent = str(item.get('parentId') or '')
            content = item.get('content') if isinstance(item.get('content'), dict) else {}
            raw_meta = item.get('meta') if isinstance(item.get('meta'), dict) else {}
            color = str(raw_meta.get('color') or 'default').lower()
            if color not in ALLOWED_COLORS:
                color = 'default'
            tags = raw_meta.get('tags') if isinstance(raw_meta.get('tags'), list) else []
            meta = {
                'color': color,
                'tags': [str(tag).strip()[:32] for tag in tags[:8] if str(tag).strip()],
                'pinned': bool(raw_meta.get('pinned')),
            }
            kind = str(item.get('kind') or 'ai').strip().lower()
            if kind not in ALLOWED_KINDS:
                kind = 'ai'
            try:
                x = max(-100000.0, min(100000.0, float(item.get('x', 0))))
                y = max(-100000.0, min(100000.0, float(item.get('y', 0))))
            except (TypeError, ValueError):
                x, y = 0.0, 0.0
            objects.append(CanvasNode(
                id=new_id,
                board=board,
                parent_id=id_map.get(parent) if parent else None,
                user=user,
                prompt=str(item.get('prompt') or '')[:2000],
                title=str(item.get('title') or content.get('title') or 'Card')[:300],
                content=json.dumps(content, ensure_ascii=False),
                status='done',
                x=x,
                y=y,
                web_search_enabled=bool(item.get('webSearchEnabled')),
                model_used=str(item.get('modelUsed') or '')[:100],
                kind=kind,
                metadata=json.dumps(meta, ensure_ascii=False),
                error='',
                created_at=now,
                updated_at=now,
            ))
        CanvasNode.objects.bulk_create(objects)
        board_data = payload.get('board') if isinstance(payload.get('board'), dict) else {}
        settings = board_data.get('settings') if isinstance(board_data.get('settings'), dict) else {}
        if board_data.get('title'):
            board.title = str(board_data['title'])[:200]
        board.settings = json.dumps(settings, ensure_ascii=False)
        board.updated_at = now
        board.save(update_fields=['title', 'settings', 'updated_at'])
    return board_payload(board)


def markdown_export(board):
    payload = board_payload(board)
    lines = [f"# {board.title}", '']
    by_parent = {}
    for node in payload['nodes']:
        by_parent.setdefault(node['parentId'], []).append(node)

    def walk(parent_id, depth):
        for node in by_parent.get(parent_id, []):
            title = node['title'] or node['prompt'] or 'Card'
            lines.append('#' * min(6, depth + 2) + ' ' + title)
            lines.append('')
            content = node.get('content') or {}
            summary = str(content.get('summary') or '').strip()
            if summary:
                lines.append(summary)
                lines.append('')
            for sec in content.get('sections') or []:
                if not isinstance(sec, dict):
                    continue
                if sec.get('type') == 'text' and sec.get('content'):
                    lines.append(str(sec['content']))
                    lines.append('')
                elif sec.get('type') == 'bullets':
                    if sec.get('title'):
                        lines.append(f"**{sec['title']}**")
                    for item in sec.get('items') or []:
                        lines.append(f"- {item}")
                    lines.append('')
                elif sec.get('type') == 'references':
                    lines.append('**Sources**')
                    for ref in sec.get('items') or []:
                        if isinstance(ref, dict):
                            lines.append(f"- {ref.get('title') or ref.get('url') or 'Source'}: {ref.get('url') or ''}")
                    lines.append('')
            if node.get('prompt'):
                lines.append(f"_Prompt: {node['prompt']}_")
                lines.append('')
            walk(node['id'], depth + 1)

    walk('', 0)
    return '\n'.join(lines).strip() + '\n'
