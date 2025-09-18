from typing import Optional, List, Tuple
import os
import duckdb
from rapidfuzz import fuzz, process

from .config import BASES_DUCKDB_PATH
from .nlp.normalize import normalize_text


class BaseRetrieval:
    def __init__(self, db_path: str = BASES_DUCKDB_PATH):
        self._items: List[Tuple[str, str]] = []
        if not db_path or not os.path.exists(db_path):
            self._con = None
            return
        try:
            self._con = duckdb.connect(db_path, read_only=True)
            self._load()
        except Exception:
            self._con = None
            self._items = []

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
        for rk, name, en in rows:
            text = normalize_text(f"{name} {en}".strip())
            self._items.append((rk, text))

    def search_one(self, query: str) -> Optional[str]:
        qn = normalize_text(query)
        choices = {rk: text for rk, text in self._items}
        if not choices:
            return None
        best = process.extractOne(qn, choices, scorer=fuzz.WRatio)
        if not best:
            return None
        match_text, score, rk = best
        if score < 80:
            return None
        return rk


