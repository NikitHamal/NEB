"""Bounded parallel execution for read-only tool batches."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

from api.background_agent.qwen_harness.catalog import is_readonly


def run_action_batches(actions, execute_one, max_workers: int = 6):
    results = []
    index = 0
    total = len(actions or [])
    while index < total:
        action = actions[index]
        tool = (action.get('tool') or '').strip()
        if is_readonly(tool):
            batch = []
            while index < total and is_readonly((actions[index].get('tool') or '').strip()):
                batch.append(actions[index])
                index += 1
            if len(batch) == 1:
                results.append(execute_one(batch[0]))
                continue
            workers = max(1, min(int(max_workers or 1), len(batch)))
            with ThreadPoolExecutor(max_workers=workers) as pool:
                futures = [pool.submit(execute_one, item) for item in batch]
                results.extend(future.result() for future in futures)
            continue
        results.append(execute_one(action))
        index += 1
    return results
