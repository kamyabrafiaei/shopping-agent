import os
import sqlite3
import json
import time
from typing import Any

from .config import ENABLE_SQLITE_LOGS, LOG_DB_PATH


def _ensure_db():
    if not ENABLE_SQLITE_LOGS:
        return None
    os.makedirs(os.path.dirname(LOG_DB_PATH), exist_ok=True)
    conn = sqlite3.connect(LOG_DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at REAL,
            chat_id TEXT,
            request_json TEXT,
            response_json TEXT,
            meta TEXT
        )
        """
    )
    conn.commit()
    return conn


_CONN = None


def log_chat(chat_id: str, req: Any, resp: Any, meta: dict | None = None):
    global _CONN
    if not ENABLE_SQLITE_LOGS:
        return
    if _CONN is None:
        _CONN = _ensure_db()
    if _CONN is None:
        return
    cur = _CONN.cursor()
    cur.execute(
        "INSERT INTO chat_logs (created_at, chat_id, request_json, response_json, meta) VALUES (?, ?, ?, ?, ?)",
        (
            time.time(),
            chat_id,
            json.dumps(req, ensure_ascii=False),
            json.dumps(resp, ensure_ascii=False),
            json.dumps(meta or {}, ensure_ascii=False),
        ),
    )
    _CONN.commit()


