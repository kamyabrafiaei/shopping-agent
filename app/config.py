import os


def getenv(key: str, default: str | None = None) -> str | None:
    v = os.getenv(key)
    return v if v is not None and v != "" else default


BASIC_AUTH_USER = "user"
BASIC_AUTH_PASS = "pass"

BASES_DUCKDB_PATH = getenv("BASES_DUCKDB_PATH", "artifacts/bases.duckdb")

ENABLE_SQLITE_LOGS = True
LOG_DB_PATH = "data/logs.db"


