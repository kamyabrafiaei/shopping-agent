# Torob Turbo Assistant — Stage 1

Run locally:
```
python -m venv .venv
.venv\\Scripts\\pip install -r requirements.txt
.venv\\Scripts\\uvicorn app.main:app --reload --port 8000
```

Docker:
```
docker build -t omegakam/torob-assistant:stage1 .
docker run --rm -p 8000:8000 \
  -e ENABLE_SQLITE_LOGS=true \
  -e BASES_DUCKDB_PATH=/app/artifacts/bases.duckdb \
  omegakam/torob-assistant:stage1
```

Endpoints:
- POST `/chat`
- GET `/health`
- GET `/metrics`

Basic Auth (optional via env):
```
BASIC_AUTH_ENABLE=true
BASIC_AUTH_USER=user
BASIC_AUTH_PASS=pass
```
Then request with header:
```
Authorization: Basic base64(user:pass)
```

Stage 0 inputs:
```
{ "chat_id": "sanity-check-ping", "messages": [ { "type": "text", "content": "ping" } ] }
{ "chat_id": "sanity-check-base-key", "messages": [ { "type": "text", "content": "return base random key: 123" } ] }
{ "chat_id": "sanity-check-member-key", "messages": [ { "type": "text", "content": "return member random key: abc" } ] }
```

Build artifacts for Stage 1 (once):
```
python scripts/build_artifacts.py --data_dir torob-turbo-stage2 --out artifacts/bases.duckdb
```

Stage 1 mapping:
- Retrieval uses DuckDB artifact `artifacts/bases.duckdb` (table `bases_core`) and RapidFuzz fuzzy match on normalized Persian/English names.
- Thresholds tuned for single, high-confidence mapping; only one `base_random_key` is returned.
- Logs of request/response with meta are stored in SQLite at `data/logs.db` (set `ENABLE_SQLITE_LOGS=true`).

Darkube deployment (Docker Image):
- Reference: https://docs.hamravesh.com/darkube/create/docker-image/intro
- Image: `omegakam/torob-assistant:stage1`
- Container port: 8000, Readiness: `/health`
- Env in app settings:
  - `ENABLE_SQLITE_LOGS=true`
  - `BASES_DUCKDB_PATH=/app/artifacts/bases.duckdb`
  - `BASIC_AUTH_ENABLE=false` (for judge), or true with headers when private
  - `TOROB_PROXY_BASE_URL=https://turbo.torob.com/v1` (future stages)
  - `OPENAI_API_KEY=trb-...` (future stages)



