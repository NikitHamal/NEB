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

- Resource catalog (`api/resource_catalog.py`), one resource-form flow for web (`web/resource_upload.py`), Study Lab JSON guard (`web/json_endpoint.py`): see their commits.
- API resource forms: `api/resource_form.py` owns listing fields, link and cover cleaning (`InvalidInput`, `read_thumbnail`) and `discard_saved_files` for the API, the owner edit and the web forms; signed-in and anonymous upload and request create are one function each (`_create_pending_resource`, `_save_resource_request`); the 55-line sort ladder in `resources_list` is `_SORT_ORDERS`; web uses `parse_paid_fields` (the second price parser is gone). Tests: `api.test_resource_api`.

- Dead code with no reader removed by a repo-wide reference scan (name appears nowhere but its definition; signal receivers, template tags registered under another name, routed views and test-only helpers kept): 62 functions/classes in `api/` (`counters`, `realtime`, `views_feed`, `qwen_utils/prompts`, `metaai_proxy`, `agent_social`, `llm`), `web/` (`toolstore`, `lazypdf/build`, template filters, `ajax_convert_credits`), `services/result_scraper.NtcSEEAdapter`; the unused imports they left behind; empty re-export facades `api/llm/__init__` and `api/qwen_utils/__init__` (every reader imports the submodule). `nebians/analytics/__init__` stays: middleware and views read `analytics.submit` / `event_from_request` through it.

## Parallel sessions

Two sessions have pushed to `main` at the same time on this task (the Turn refactor landed twice). Run `git fetch && git log HEAD..origin/main` before choosing the next item and again before every push; push small.

## Open (ordered by leverage)

Decision log: problem list above its fix; a fix moves to Done when it lands.
