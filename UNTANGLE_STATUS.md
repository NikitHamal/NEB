# Untangle status

Goal: the `untangle-codebase` skill applied to the repo, end to end, with behaviour unchanged. Scope chosen without asking (the owner said go with the recommendation): structure first; comments that only restate the code (the repo rule is already "no comments"); tests only where they cannot fail or repeat the implementation.

Work in `backend_python/` first (largest, most tested). Check `--stat` of the `untangle:` commits before starting; do not redo anything listed under Done.

Verify: `cd backend_python && export DEBUG=True DB_ENGINE=sqlite SECRET_KEY=x && python3 manage.py test` (the count only goes up; 663 at the start of the third session).

## Done

- Arena chat helpers (`require_user`, `get_owned_session`, `sse_format`, `sse_done_marker`, `sse_response`) live once in `api/arena_common.py`; `arena_views`, `arena_qwen_views`, `arena_deepai_views`, `arena_agent_views` import them (each had a private copy, with two spellings of the same error text).
- K2 Horizon, Poolside and Inception arena views were three 235-line copies of one flow. They are now rows in `SIMPLE_PROVIDERS` (`api/arena_simple_providers.py`); default model and "thinking" come from the proxy's `MODELS[0]`, `arena_urls` builds the routes from the list. URL names and paths unchanged. Add a guest-site provider = one proxy module plus one row.
- Dead modules removed (nothing imported or routed them): `chat2api_proxy`, `code_agent_prompt`, `code_agent_providers`, `consica_bridge_views`/`consica_bridge_urls` (never mounted; `CONSICA_BRIDGE_KEY` stays, the Astroweb bridge uses it), `llm/provider_store`, `llm/runtime`.

- Star-import facades (`web/views.py`, `api/views.py`) gone; urls name the module that defines each view; view modules import what they use (this fixed latent NameErrors).
- One chat turn: `arena_common.Turn` (user row, assistant row, header, finalize, counters, closing events) for qwen, deepai, simple-provider and community streams; multipart and JSON send views share one flow. The browser endpoints (`web/views_arena.py`) only identify the session user and call `qwen_turn_response`, `deepai_turn_response`, `create_*_chat_session`, `upload_named_files`/`upload_attachments`; they had their own copies of all of it (and a stale `bx-v` header). Tests: `api.test_arena_turns`.
- Forum posts and comments share `ForumContentMixin` in `api/serializers.py`.

- Repo debris with no reader removed: flat `neby_cli/*.py` (stale older copies; the package and the `neby` entry point are `neby_cli/neby_cli/`), tracked `neby_cli.egg-info`, empty root `needle_*.mjs` (the real ones are `backend_python/benchmarks/`), root `ws_*.py` probes of the production socket (hard-coded tunnel URL), root `scratch/` outputs, `.cs12prev/` previews, `bca/.probe.txt`, and one-off debug scripts in `backend_python/scratch/` (ops scripts there stay: `deploy.ps1` is wired into the deploy workflow).

## Parallel sessions

Two sessions have pushed to `main` at the same time on this task (the Turn refactor landed twice). Run `git fetch && git log HEAD..origin/main` before choosing the next item and again before every push; push small.

## Open (ordered by leverage)

Decision log: problem list above its fix; a fix moves to Done when it lands.
