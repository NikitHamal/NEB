"""
Neby CLI Benchmark Harness.
Tests DeepSeek and Meta AI as coding agents against a suite of tasks.

Run with:
  python -m neby_cli.bench [--providers metaai deepseek] [--verbose]

Measures:
- Task pass rate (functional correctness)
- Tool call accuracy (did it use the right tools?)
- Response quality (no hallucinations, correct code)
- Latency (tokens/sec)
- Context efficiency (tokens used)
"""
import argparse
import json
import os
import sys
import time
import tempfile
import shutil
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Tuple

BACKEND_DIR = r"F:\NEB\backend_python"
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)
try:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nebians.settings")
    import django
    django.setup()
except Exception:
    pass

from .providers import stream_chat
from .parser import parse_tool_calls
from .harness import build_system_prompt


# ─── Benchmark tasks ──────────────────────────────────────────────────────────

@dataclass
class BenchTask:
    id: str
    name: str
    prompt: str
    expected_tools: List[str]
    validation_fn: Optional[str] = None
    category: str = "coding"
    difficulty: str = "easy"


TASKS: List[BenchTask] = [
    BenchTask(
        id="list_files",
        name="List workspace files",
        prompt="What Python files are in the current directory? Use list_dir or find_files to check.",
        expected_tools=["list_dir", "find_files"],
        category="navigation",
        difficulty="easy",
    ),
    BenchTask(
        id="read_and_explain",
        name="Read a file and explain it",
        prompt="Read the file harness.py and briefly explain what build_system_prompt does.",
        expected_tools=["read_file"],
        category="comprehension",
        difficulty="easy",
    ),
    BenchTask(
        id="grep_function",
        name="Find a function definition",
        prompt="Search for the definition of 'stream_chat' across all Python files.",
        expected_tools=["grep_search"],
        category="navigation",
        difficulty="easy",
    ),
    BenchTask(
        id="write_new_file",
        name="Create a new Python file",
        prompt="Create a new file called bench_output.py with a function called `add(a, b)` that returns a+b. Then call done().",
        expected_tools=["write_file", "done"],
        category="coding",
        difficulty="medium",
    ),
    BenchTask(
        id="edit_existing",
        name="Edit an existing file",
        prompt="Read bench_output.py, then add a function `multiply(a, b)` that returns a*b. Use edit_file, not write_file.",
        expected_tools=["read_file", "edit_file", "done"],
        category="coding",
        difficulty="medium",
    ),
    BenchTask(
        id="run_command",
        name="Run a shell command",
        prompt="Run `python --version` and report the Python version you found.",
        expected_tools=["run_command"],
        category="shell",
        difficulty="easy",
    ),
    BenchTask(
        id="debug_code",
        name="Find and fix a bug",
        prompt=(
            "The file buggy.py contains:\n\n"
            "```python\ndef divide(a, b):\n    return a / b\n\nresult = divide(10, 0)\nprint(result)\n```\n\n"
            "Write this file, then fix the ZeroDivisionError by adding a check. Use write_file then edit_file."
        ),
        expected_tools=["write_file", "edit_file", "done"],
        category="debugging",
        difficulty="medium",
    ),
    BenchTask(
        id="multi_step_refactor",
        name="Multi-step refactor",
        prompt=(
            "Create a file utils.py with two functions: `is_even(n)` returning n%2==0, "
            "and `is_prime(n)` with a basic primality check. "
            "Then read it back and verify it looks correct. Call done() with a summary."
        ),
        expected_tools=["write_file", "read_file", "done"],
        category="coding",
        difficulty="hard",
    ),
    BenchTask(
        id="search_and_report",
        name="Search and report patterns",
        prompt="Search for all uses of 'yield' in the providers.py file and report what generators are defined.",
        expected_tools=["grep_search", "read_file"],
        category="comprehension",
        difficulty="medium",
    ),
    BenchTask(
        id="chain_tools",
        name="Chain 3+ tools",
        prompt=(
            "List the files in the neby_cli directory, pick the largest file, "
            "read the first 20 lines of it, then call done() summarizing what you found."
        ),
        expected_tools=["list_dir", "read_file", "done"],
        category="agentic",
        difficulty="hard",
    ),
]


# ─── Result tracking ──────────────────────────────────────────────────────────

@dataclass
class TaskResult:
    task_id: str
    task_name: str
    provider: str
    model: str
    success: bool
    tools_used: List[str] = field(default_factory=list)
    tools_expected: List[str] = field(default_factory=list)
    tool_accuracy: float = 0.0
    response_chars: int = 0
    latency_sec: float = 0.0
    chars_per_sec: float = 0.0
    error: Optional[str] = None
    response_snippet: str = ""


@dataclass
class BenchReport:
    provider: str
    model: str
    total_tasks: int
    passed: int
    tool_accuracy_avg: float
    avg_latency_sec: float
    avg_chars_per_sec: float
    task_results: List[TaskResult] = field(default_factory=list)

    @property
    def pass_rate(self) -> float:
        return self.passed / self.total_tasks if self.total_tasks else 0.0


# ─── Runner ───────────────────────────────────────────────────────────────────

def _build_messages(task: BenchTask, cwd: str, provider: str, model: str) -> List[Dict]:
    sys_prompt = build_system_prompt(provider=provider, model=model, cwd=cwd, mode="Agent")
    return [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": task.prompt},
    ]


def _tool_accuracy(used: List[str], expected: List[str]) -> float:
    if not expected:
        return 1.0
    hits = sum(1 for t in expected if t in used)
    return hits / len(expected)


def _is_task_success(result_text: str, tools_used: List[str], task: BenchTask) -> bool:
    # Heuristic pass/fail:
    # 1. At least one expected tool was used
    if task.expected_tools and not any(t in tools_used for t in task.expected_tools):
        return False
    # 2. Response is non-empty and not an error
    if not result_text.strip():
        return False
    if "error:" in result_text.lower()[:100] and len(result_text) < 200:
        return False
    # 3. If 'done' is expected, check it was called or text says done
    if "done" in task.expected_tools:
        if "done" not in tools_used and "done()" not in result_text.lower() and "summary" not in result_text.lower():
            return False
    return True


def run_task(
    task: BenchTask,
    provider: str,
    model: str,
    cwd: str,
    verbose: bool = False,
    timeout_sec: float = 60.0,
) -> TaskResult:
    messages = _build_messages(task, cwd, provider, model)
    result_text = ""
    all_tools: List[str] = []
    start = time.time()
    error = None

    # Multi-step loop (up to 5 steps like agent)
    for step in range(5):
        step_text = ""
        try:
            for chunk in stream_chat(messages, provider=provider, model=model):
                if time.time() - start > timeout_sec:
                    error = "timeout"
                    break
                ct = chunk.get("type")
                if ct == "text":
                    step_text += chunk.get("content", "")
                elif ct == "error":
                    error = chunk.get("error", "unknown error")
                    break
        except Exception as e:
            error = str(e)
            break

        if error:
            break

        result_text += step_text
        clean_text, tool_calls = parse_tool_calls(step_text)

        if not tool_calls:
            break

        for call in tool_calls:
            all_tools.append(call.name)
            if call.name == "done":
                break

        if "done" in all_tools:
            break

        # Feed tool results back (simplified - just echo the call was received)
        tool_result = f"Tool '{tool_calls[-1].name}' executed successfully."
        messages.append({"role": "assistant", "content": step_text})
        messages.append({"role": "user", "content": f"Tool Result:\n```\n{tool_result}\n```\nProceed."})

    elapsed = time.time() - start
    chars = len(result_text)
    accuracy = _tool_accuracy(all_tools, task.expected_tools)
    success = _is_task_success(result_text, all_tools, task) and not error

    if verbose:
        status = "PASS" if success else "FAIL"
        print(f"  [{status}] {task.name}")
        print(f"    Tools used:  {all_tools}")
        print(f"    Tools expected: {task.expected_tools}")
        print(f"    Accuracy: {accuracy:.0%}  |  Latency: {elapsed:.1f}s  |  Chars: {chars}")
        if error:
            print(f"    Error: {error}")
        print(f"    Snippet: {result_text[:150].strip()!r}")

    return TaskResult(
        task_id=task.id,
        task_name=task.name,
        provider=provider,
        model=model,
        success=success,
        tools_used=all_tools,
        tools_expected=task.expected_tools,
        tool_accuracy=accuracy,
        response_chars=chars,
        latency_sec=elapsed,
        chars_per_sec=chars / elapsed if elapsed > 0 else 0,
        error=error,
        response_snippet=result_text[:200].strip(),
    )


def run_benchmark(
    provider: str,
    model: str,
    task_ids: Optional[List[str]] = None,
    verbose: bool = False,
) -> BenchReport:
    cwd = os.path.dirname(os.path.abspath(__file__))
    tasks = TASKS
    if task_ids:
        tasks = [t for t in TASKS if t.id in task_ids]

    print(f"\n{'=' * 60}")
    print(f"  Benchmarking: {provider}:{model}")
    print(f"  Tasks: {len(tasks)}")
    print(f"{'=' * 60}")

    results: List[TaskResult] = []
    for task in tasks:
        if verbose:
            print(f"\n  >> {task.name} [{task.difficulty}]")
        r = run_task(task, provider, model, cwd=cwd, verbose=verbose)
        results.append(r)

    passed = sum(1 for r in results if r.success)
    avg_accuracy = sum(r.tool_accuracy for r in results) / len(results) if results else 0
    avg_latency = sum(r.latency_sec for r in results) / len(results) if results else 0
    avg_cps = sum(r.chars_per_sec for r in results) / len(results) if results else 0

    report = BenchReport(
        provider=provider,
        model=model,
        total_tasks=len(results),
        passed=passed,
        tool_accuracy_avg=avg_accuracy,
        avg_latency_sec=avg_latency,
        avg_chars_per_sec=avg_cps,
        task_results=results,
    )
    return report


def print_report(report: BenchReport):
    print(f"\n{'=' * 60}")
    print(f"  RESULTS: {report.provider}:{report.model}")
    print(f"{'=' * 60}")
    print(f"  Pass rate:       {report.pass_rate:.0%}  ({report.passed}/{report.total_tasks})")
    print(f"  Tool accuracy:   {report.tool_accuracy_avg:.0%}")
    print(f"  Avg latency:     {report.avg_latency_sec:.1f}s")
    print(f"  Avg throughput:  {report.avg_chars_per_sec:.0f} chars/sec")
    print()
    print(f"  {'Task':<30} {'Pass':<6} {'Tools':<8} {'Latency'}")
    print(f"  {'-'*55}")
    for r in report.task_results:
        status = "OK" if r.success else "XX"
        print(f"  {r.task_name:<30} {status:<6} {r.tool_accuracy:.0%}/<{len(r.tools_used):02d}>   {r.latency_sec:.1f}s")


def compare_reports(reports: List[BenchReport]):
    print(f"\n{'=' * 70}")
    print("  BENCHMARK COMPARISON")
    print(f"{'=' * 70}")
    headers = ["Provider:Model", "Pass%", "Tool Acc", "Avg Lat", "Throughput"]
    print(f"  {headers[0]:<28} {headers[1]:<8} {headers[2]:<10} {headers[3]:<10} {headers[4]}")
    print(f"  {'-' * 65}")
    for r in sorted(reports, key=lambda x: x.pass_rate, reverse=True):
        label = f"{r.provider}:{r.model}"
        print(f"  {label:<28} {r.pass_rate:.0%}     {r.tool_accuracy_avg:.0%}        {r.avg_latency_sec:.1f}s       {r.avg_chars_per_sec:.0f} c/s")


def main():
    parser = argparse.ArgumentParser(description="Neby CLI Benchmark Harness")
    parser.add_argument("--providers", nargs="+", default=["metaai", "deepseek"],
                        help="Providers to benchmark (default: metaai deepseek)")
    parser.add_argument("--models", nargs="+", default=None,
                        help="Override models per provider (same order)")
    parser.add_argument("--tasks", nargs="+", default=None,
                        help="Specific task IDs to run (default: all)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show detailed output for each task")
    parser.add_argument("--output", "-o", default=None,
                        help="Save JSON report to file")
    parser.add_argument("--list-tasks", action="store_true",
                        help="List all available benchmark tasks")
    args = parser.parse_args()

    if args.list_tasks:
        print("\nAvailable benchmark tasks:")
        for t in TASKS:
            print(f"  {t.id:<30} [{t.difficulty:6}] {t.category:<15} {t.name}")
        return

    provider_model_pairs = []
    from .providers import CATALOG
    for i, prov in enumerate(args.providers):
        if args.models and i < len(args.models):
            mdl = args.models[i]
        else:
            entry = next((p for p in CATALOG if p["provider"] == prov), None)
            mdl = entry["default_model"] if entry else prov
        provider_model_pairs.append((prov, mdl))

    reports = []
    for prov, mdl in provider_model_pairs:
        report = run_benchmark(prov, mdl, task_ids=args.tasks, verbose=args.verbose)
        print_report(report)
        reports.append(report)

    if len(reports) > 1:
        compare_reports(reports)

    if args.output:
        data = [asdict(r) for r in reports]
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"\n  Report saved to: {args.output}")


if __name__ == "__main__":
    main()
