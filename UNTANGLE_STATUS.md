# Untangle status

Goal: the `untangle-codebase` skill applied to the repo, end to end, with behaviour unchanged. Scope chosen without asking (the owner said go with the recommendation): structure first; comments that only restate the code (the repo rule is already "no comments"); tests only where they cannot fail or repeat the implementation.

Work in `backend_python/` first (largest, most tested). Check `--stat` of the `untangle:` commits before starting; do not redo anything listed under Done.

Verify: `cd backend_python && export DEBUG=True DB_ENGINE=sqlite SECRET_KEY=x && python3 manage.py test` (656 tests green before any change; the count only goes up through `api.test_arena_simple_providers`).

## Done

- Arena chat helpers (`require_user`, `get_owned_session`, `sse_format`, `sse_done_marker`, `sse_response`) live once in `api/arena_common.py`; `arena_views`, `arena_qwen_views`, `arena_deepai_views`, `arena_agent_views` import them (each had a private copy, with two spellings of the same error text).
- K2 Horizon, Poolside and Inception arena views were three 235-line copies of one flow. They are now rows in `SIMPLE_PROVIDERS` (`api/arena_simple_providers.py`); default model and "thinking" come from the proxy's `MODELS[0]`, `arena_urls` builds the routes from the list. URL names and paths unchanged. Add a guest-site provider = one proxy module plus one row.
- Dead modules removed (nothing imported or routed them): `chat2api_proxy`, `code_agent_prompt`, `code_agent_providers`, `consica_bridge_views`/`consica_bridge_urls` (never mounted; `CONSICA_BRIDGE_KEY` stays, the Astroweb bridge uses it), `llm/provider_store`, `llm/runtime`.

## Open (ordered by leverage)

See the decision log below; items move to Done as they land.
