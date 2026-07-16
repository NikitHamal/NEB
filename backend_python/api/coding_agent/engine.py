"""Main agent engine for the background coding agent.

The engine orchestrates the agent loop:
1. Clone/setup the repo workspace
2. Create a working branch
3. Iterate: call AI → parse tool calls → execute tools → feed results back
4. On completion: commit, optionally push, create PR
5. Support pause/resume/stop and user interruptions
"""
import json
import logging
import os
import time

from django.conf import settings

from api.models import CodingTask, CodingTaskMessage, CodingProject
from api.utils import now_ms, uuid_str
from api.coding_agent import prompts, tools, provider_adapter, git_manager, queue

logger = logging.getLogger(__name__)

WORKSPACE_PARENT = getattr(settings, 'CODING_AGENT_WORKSPACE_DIR', '/tmp/coding_workspaces')
MAX_ITERATIONS_DEFAULT = 50
COMMIT_MESSAGE_PREFIX = '[coding-agent]'


def process_task(task_id):
    """Main entry point: process a single coding task to completion.
    
    This is called by the worker daemon. It handles the full lifecycle:
    setup → iterate → finish/fail.
    """
    try:
        task = CodingTask.objects.get(pk=task_id)
    except CodingTask.DoesNotExist:
        logger.error('process_task: task %s not found', task_id)
        return
    
    if task.status in (CodingTask.STATUS_COMPLETED, CodingTask.STATUS_STOPPED, CodingTask.STATUS_FAILED):
        logger.info('process_task: task %s already in terminal state %s', task_id, task.status)
        return
    
    project = task.project
    
    workspace, error = _ensure_workspace(project)
    if error:
        queue.mark_failed(task, f'Workspace setup failed: {error}')
        return
    
    success, msg = _ensure_branch(workspace, task, project)
    if not success:
        queue.mark_failed(task, f'Branch setup failed: {msg}')
        return
    
    queue.mark_running(task)
    task.refresh_from_db()
    
    try:
        _run_agent_loop(task, project, workspace)
    except Exception as e:
        logger.exception('Agent loop crashed for task %s: %s', task_id, e)
        task.refresh_from_db()
        if task.status == CodingTask.STATUS_RUNNING:
            queue.mark_failed(task, str(e)[:2000])


def _ensure_workspace(project):
    """Ensure the repo is cloned and ready. Returns (workspace_path, error)."""
    if project.workspace_dir and os.path.exists(project.workspace_dir):
        if os.path.exists(os.path.join(project.workspace_dir, '.git')):
            return project.workspace_dir, None
    
    os.makedirs(WORKSPACE_PARENT, exist_ok=True)
    
    token = _decrypt_token(project.github_token)
    workspace, error = git_manager.clone_repo(
        WORKSPACE_PARENT,
        project.repo_url,
        token,
        depth=1,
    )
    
    if error:
        return None, error
    
    CodingProject.objects.filter(pk=project.id).update(
        workspace_dir=workspace,
        clone_status='ready',
        clone_error='',
        updated_at=now_ms(),
    )
    
    return workspace, None


def _ensure_branch(workspace, task, project):
    """Ensure the task's branch exists and is checked out."""
    return git_manager.create_branch(workspace, task.branch_name, project.default_branch)


def _run_agent_loop(task, project, workspace):
    """The main agent iteration loop."""
    messages = _build_conversation(task, project)
    iteration = task.iteration
    
    while iteration < task.max_iterations:
        task.refresh_from_db()
        if task.status == CodingTask.STATUS_STOPPED:
            logger.info('Task %s stopped by user', task.id)
            return
        if task.status == CodingTask.STATUS_PAUSED:
            logger.info('Task %s paused, waiting for user input', task.id)
            time.sleep(5)
            continue
        
        iteration += 1
        queue.update_iteration(task, iteration, '')
        
        logger.info('Task %s: iteration %d/%d', task.id, iteration, task.max_iterations)
        
        ai_response = provider_adapter.call_provider(
            task.provider,
            messages,
            task.model_id or None,
        )
        
        parsed = prompts.parse_ai_response(ai_response)
        
        msg = CodingTaskMessage.objects.create(
            id=uuid_str(),
            task_id=task.id,
            role=CodingTaskMessage.ROLE_ASSISTANT,
            content=ai_response[:10000],
            thoughts=parsed['thoughts'][:5000],
            tool_actions=json.dumps(parsed['actions']) if parsed['actions'] else '',
            status_flag=parsed['status'],
            created_at=now_ms(),
        )
        
        messages.append({
            'role': 'assistant',
            'content': ai_response[:6000],
        })
        
        queue.update_iteration(task, iteration, parsed['thoughts'][:2000])
        
        status = parsed['status']
        actions = parsed['actions']
        
        if not actions or status == 'error':
            if status == 'error':
                queue.log_action(task, iteration, 'status', f'AI error: {parsed["thoughts"][:500]}', status='error')
                if iteration >= 3:
                    queue.mark_failed(task, f'AI returned error state: {parsed["thoughts"][:500]}')
                    return
            time.sleep(2)
            continue
        
        has_finish = any(a.get('tool') == 'finish' for a in actions)
        has_need_input = any(a.get('tool') == 'need_input' for a in actions)
        
        tool_results = []
        for action in actions:
            tool_name = action.get('tool', '')
            args = action.get('args', {})
            
            if tool_name in ('finish', 'need_input'):
                continue
            
            result, action_type, file_path, diff = tools.execute_tool(workspace, tool_name, args)
            
            queue.log_action(
                task, iteration, action_type,
                description=f'{tool_name}: {result[:500]}',
                file_path=file_path,
                content_diff=diff,
                status='error' if result.startswith('Error') else 'ok',
            )
            
            tool_results.append({
                'tool': tool_name,
                'args': args,
                'result': result[:4000],
            })
            
            if result.startswith('Error'):
                logger.warning('Task %s: tool %s failed: %s', task.id, tool_name, result[:200])
        
        CodingTaskMessage.objects.filter(pk=msg.id).update(
            tool_results=json.dumps(tool_results) if tool_results else '',
        )
        
        result_text = _format_tool_results(tool_results)
        messages.append({
            'role': 'tool_result',
            'content': result_text[:8000],
        })
        
        CodingTaskMessage.objects.create(
            id=uuid_str(),
            task_id=task.id,
            role=CodingTaskMessage.ROLE_TOOL_RESULT,
            content=result_text[:10000],
            created_at=now_ms(),
        )
        
        if has_need_input:
            need_input_action = next(a for a in actions if a.get('tool') == 'need_input')
            question = need_input_action.get('args', {}).get('question', 'Agent needs input')
            queue.log_action(task, iteration, 'status', f'Waiting for input: {question}')
            queue.mark_paused(task, question)
            return
        
        if has_finish:
            finish_action = next(a for a in actions if a.get('tool') == 'finish')
            summary = finish_action.get('args', {}).get('summary', 'Task completed')
            queue.log_action(task, iteration, 'status', f'Task completed: {summary}')
            _finalize_task(task, project, workspace, summary)
            return
        
        if len(messages) > 60:
            messages = _compact_history(messages, task, project)
    
    logger.info('Task %s: reached max iterations (%d)', task.id, task.max_iterations)
    queue.mark_failed(task, f'Reached maximum iterations ({task.max_iterations}) without completing')


def _build_conversation(task, project):
    """Build the conversation message list for the AI provider."""
    messages = [{'role': 'system', 'content': prompts.SYSTEM_PROMPT}]
    
    repo_info = {
        'full_name': project.repo_full_name,
        'default_branch': project.default_branch,
    }
    
    initial_prompt = prompts.build_initial_prompt(task.goal, task.branch_name, repo_info)
    messages.append({'role': 'user', 'content': initial_prompt})
    
    prior_msgs = CodingTaskMessage.objects.filter(
        task_id=task.id,
    ).order_by('created_at')
    
    for msg in prior_msgs:
        if msg.role == CodingTaskMessage.ROLE_USER:
            messages.append({'role': 'user', 'content': msg.content[:6000]})
        elif msg.role == CodingTaskMessage.ROLE_ASSISTANT:
            content = msg.content[:6000]
            if msg.thoughts:
                content = msg.thoughts[:2000] + '\n\n' + content
            messages.append({'role': 'assistant', 'content': content})
        elif msg.role == CodingTaskMessage.ROLE_TOOL_RESULT:
            messages.append({'role': 'tool_result', 'content': msg.content[:8000]})
    
    return messages


def _compact_history(messages, task, project):
    """Compact the conversation history when it gets too long."""
    system_msg = messages[0] if messages and messages[0].get('role') == 'system' else None
    
    summary = f'[Previous conversation summary: The agent has completed {task.iteration} iterations working on: {task.goal[:200]}. '
    summary += f'Last thought: {task.last_thought[:300]}. Continue working.]'
    
    compacted = []
    if system_msg:
        compacted.append(system_msg)
    
    initial_prompt = prompts.build_initial_prompt(task.goal, task.branch_name, {
        'full_name': project.repo_full_name,
        'default_branch': project.default_branch,
    })
    compacted.append({'role': 'user', 'content': initial_prompt})
    compacted.append({'role': 'user', 'content': summary})
    
    for msg in messages[-8:]:
        if msg.get('role') not in ('system',):
            compacted.append(msg)
    
    return compacted


def _format_tool_results(results):
    """Format tool results for feeding back to the AI."""
    if not results:
        return '(No tool results)'
    
    parts = []
    for r in results:
        tool = r.get('tool', 'unknown')
        args = r.get('args', {})
        result = r.get('result', '')
        parts.append(f'### {tool}({json.dumps(args, ensure_ascii=False)[:200]})\n{result}')
    
    return '\n\n'.join(parts)


def _finalize_task(task, project, workspace, summary):
    """Commit changes, optionally push, and create a PR."""
    changed = git_manager.get_changed_files(workspace)
    
    if not changed:
        queue.mark_completed(task)
        return
    
    commit_msg = f'{COMMIT_MESSAGE_PREFIX} {task.title}\n\n{summary[:500]}'
    success, commit_result = git_manager.commit_all(workspace, commit_msg)
    
    if not success:
        queue.log_action(task, task.iteration, 'git', f'Commit: {commit_result}', status='error')
        queue.mark_completed(task)
        return
    
    queue.log_action(task, task.iteration, 'git', f'Committed changes: {commit_result}')
    
    token = _decrypt_token(project.github_token)
    pr_url = ''
    pr_number = None
    
    if token:
        success, push_result = git_manager.push_branch(workspace, task.branch_name, token, project.repo_url)
        queue.log_action(task, task.iteration, 'git', f'Push: {push_result}',
                        status='ok' if success else 'error')
        
        if success:
            pr_body = f"""\
## Coding Agent Task

{summary}

---
*This PR was created by the NEBians Background Coding Agent.*
*Task: {task.title}*
*Provider: {task.provider}*
*Iterations: {task.iteration}*
"""
            pr_url, pr_number, pr_error = git_manager.create_pull_request(
                token,
                project.repo_full_name,
                task.branch_name,
                project.default_branch,
                task.title,
                pr_body,
            )
            
            if pr_error:
                queue.log_action(task, task.iteration, 'git', f'PR creation: {pr_error}', status='error')
            elif pr_url:
                queue.log_action(task, task.iteration, 'git', f'PR created: {pr_url}')
    
    queue.mark_completed(task, pr_url=pr_url, pr_number=pr_number)


def _encrypt_token(token):
    """Encrypt a GitHub token for storage. Uses Django's signer."""
    if not token:
        return ''
    try:
        from django.core.signing import Signer
        signer = Signer(salt='coding-agent-token')
        return signer.sign(token)
    except Exception:
        return token


def _decrypt_token(stored):
    """Decrypt a stored GitHub token."""
    if not stored:
        return ''
    try:
        from django.core.signing import Signer
        signer = Signer(salt='coding-agent-token')
        return signer.unsign(stored)
    except Exception:
        return stored


def add_user_message(task_id, message):
    """Add a user message to a task (for interrupt/follow-up)."""
    msg = CodingTaskMessage.objects.create(
        id=uuid_str(),
        task_id=task_id,
        role=CodingTaskMessage.ROLE_USER,
        content=message,
        created_at=now_ms(),
    )
    
    task = CodingTask.objects.get(pk=task_id)
    if task.status == CodingTask.STATUS_PAUSED:
        CodingTask.objects.filter(pk=task_id).update(
            status=CodingTask.STATUS_QUEUED,
            updated_at=now_ms(),
        )
        queue._notify_worker()
    
    queue._broadcast(task, 'task.user_message', {'message': message[:500]})
    return msg
