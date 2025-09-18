import os


def getenv(key: str, default: str | None = None) -> str | None:
    v = os.getenv(key)
    return v if v is not None and v != "" else default


BASIC_AUTH_ENABLE = (getenv("BASIC_AUTH_ENABLE", "false") or "false").lower() == "true"
BASIC_AUTH_USER = getenv("BASIC_AUTH_USER", None)
BASIC_AUTH_PASS = getenv("BASIC_AUTH_PASS", None)

BASES_DUCKDB_PATH = getenv("BASES_DUCKDB_PATH", "artifacts/bases.duckdb")

ENABLE_SQLITE_LOGS = (getenv("ENABLE_SQLITE_LOGS", "true") or "true").lower() == "true"
LOG_DB_PATH = getenv("LOG_DB_PATH", "data/logs.db")


