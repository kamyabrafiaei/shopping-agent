from typing import Optional, List, Tuple
import duckdb
from rapidfuzz import fuzz, process

from .config import BASES_DUCKDB_PATH


class BaseRetrieval:
    def __init__(self, db_path: str = BASES_DUCKDB_PATH):
        self._con = duckdb.connect(db_path, read_only=True)
        self._load()

    def _load(self):
        self._con.execute(
            """
            PRAGMA disable_progress_bar;
            """
        )
        self._con.execute(
            """
            SELECT random_key, coalesce(persian_name, '') AS name, coalesce(english_name, '') AS en
            FROM bases_core
            """
        )
        rows = self._con.fetchall()
        self._items: List[Tuple[str, str]] = []
        for rk, name, en in rows:
            text = f"{name} {en}".strip()
            self._items.append((rk, text))

    def search_one(self, query: str) -> Optional[str]:
        choices = {rk: text for rk, text in self._items}
        if not choices:
            return None
        best = process.extractOne(query, choices, scorer=fuzz.WRatio)
        if not best:
            return None
        match_text, score, rk = best
        if score < 75:
            return None
        return rk


