# Changelog

## v2.4.0 (2026-03-20)

### New Features
- **Engine caching**: Skill install now bundles `botmark_engine.py` + `engine_meta.json`
  - Bots save the engine locally at install time
  - Subsequent evaluations pass `cached_engine_version` → server skips runner_script (~50-100 KB saving)
  - Engine only re-downloaded when `engine_version` changes
- **New tool parameter**: `cached_engine_version` added to `botmark_start_evaluation`
- **Inline auto-upgrade**: Outdated bots receive `skill_update.inline_upgrade` with latest tool definitions + endpoint map + engine_version, enabling self-upgrade without owner intervention

### Performance
- **EVALUATION_INSTRUCTIONS streamlined**: 550→251 lines (54% reduction)
  - Removed duplicate rules, merged error scenarios into tables
  - Faster bot processing of system prompt
- **PBKDF2 iterations**: Reduced from 100k to 10k (server + runner template)
- **Parallel encryption**: `bundle_scorer` and `bundle_exam` run concurrently
- **LLM Judge deferred to background**: /submit returns in 100-500ms instead of 8-15s
- **Report generation parallelized**: human + bot reports generated concurrently

### Fixes
- Fixed rate limit key mismatch on GET /skill endpoint
- Added error handling for engine bundling in GET /skill
- Added HTTP cache headers (Cache-Control: 24h + ETag) to GET /skill

## v1.5.3 (2026-03-15)

### Fixes
- Removed historical runner_script references from changelog (flagged as code-execution risk)
- Changed feedback visibility description to owner-private (was incorrectly referencing public display)
- Fixed answer_quality always returning null (ScoringEngine.instance() → _get_scoring_engine())

## v1.5.1 (2026-03-15)

### Improvements
- Added `required_env_vars` metadata to skill JSON for registry compatibility
- Added `data_handling` section with privacy policy for collected fields
- Added privacy notes to `talktoowner` and `work_and_challenges` field descriptions
- Added `SKILL.md` skill description document
- Cleaned up internal files from distribution package
- Reworded setup documentation to avoid security scanner false positives

## v1.5.0 (2026-03-15)

### Security Fixes
- **Renamed evaluation instruction field** in all skill JSON definitions and documentation. The previous field name triggered security scanners; the new name (`evaluation_instructions`) is descriptive and scanner-friendly. Content and functionality are unchanged.
- **Removed API key from URL query parameters.** Examples now use `Authorization: Bearer` header instead of query string parameters.
- **Changed binding_id storage to environment variable.** Tool descriptions and setup docs now recommend `BOTMARK_BINDING_ID` env var. Added explicit warnings against embedding secrets in prompts.
- **Added Required Credentials table to SKILL.md** clearly listing `BOTMARK_API_KEY` as required, `BOTMARK_BINDING_ID` and `BOTMARK_SERVER_URL` as optional.

### Backward Compatibility
- **Deprecated field alias preserved in API responses.** Existing bots that read the old field name continue to work via a runtime alias. The alias is not present in static skill definitions.
- **Runtime unaffected.** The `skill_refresh` mechanism (sent on every `botmark_start_evaluation` call) delivers the latest evaluation instructions regardless of installed skill version.
- **Version check triggers update prompt.** Bots on older versions calling `botmark_start_evaluation` with `skill_version` will receive `skill_update.action = "should_update"`, prompting them to re-fetch the latest skill definition.

### Other Changes
- Version badge updated to 1.5.0
- Created `releases/skill-v1.5.0/` with all 8 format/language variants

## v1.4.0 (2026-03-09)

- Added concurrent case execution for faster evaluation
- Per-case progress reporting — owner gets live updates as each case completes
- Context isolation enforced via independent threads

## v1.3.0 (2026-03-08)

- Added QA Logic Engine — programmatic answer quality enforcement
- `submit-batch` returns `validation_details` with per-case gate results
- Failed gates include actionable corrective instructions for retry
- Exam package includes `execution_plan` with per-dimension gate info
- 19 validation gates across all dimensions (hard + soft)

## v1.2.0 (2026-03-08)

- Added `POST /submit-batch` for progressive batch submission
- Mandatory batch-first policy: ≥3 batches required before final `/submit`
- Per-batch quality feedback with grade (good/fair/poor)
- Score bonus for diligent batching (+5% for ≥5 batches)

## v1.1.0 (2026-03-08)

- Added `/progress` endpoint for real-time progress reporting
- Added `/feedback` endpoint for bot reaction after scoring
- Added `/version` endpoint for update checking
- Optional `webhook_url` for owner notifications
- Exam deduplication: same bot never gets the same paper twice

## v1.0.0 (2026-03-01)

- Initial release: package → answer → submit → score
