# Torob Turbo Assistant — Stage 0

Run locally:
```
python -m venv .venv && .venv\Scripts\pip install -r requirements.txt
.venv\Scripts\uvicorn app.main:app --reload --port 8000
```

Docker:
```
docker build -t torob-assistant:stage0 .
docker run -p 8000:8000 torob-assistant:stage0
```

Endpoints:
- POST `/chat`
- GET `/health`
- GET `/metrics`

Stage 0 inputs:
```
{ "chat_id": "sanity-check-ping", "messages": [ { "type": "text", "content": "ping" } ] }
{ "chat_id": "sanity-check-base-key", "messages": [ { "type": "text", "content": "return base random key: 123" } ] }
{ "chat_id": "sanity-check-member-key", "messages": [ { "type": "text", "content": "return member random key: abc" } ] }
```


