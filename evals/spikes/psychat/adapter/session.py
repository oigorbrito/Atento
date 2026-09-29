from __future__ import annotations

from copy import deepcopy
from threading import RLock
from typing import Any, Mapping


class InMemorySessionStore:
    """Spike store proving state ownership can live outside the donor.

    Production Atento must replace this with an appropriate persistent store.
    """

    def __init__(self) -> None:
        self._lock = RLock()
        self._states: dict[str, dict[str, Any]] = {}

    def load(self, session_id: str) -> Mapping[str, Any]:
        with self._lock:
            return deepcopy(self._states.get(session_id, {}))

    def save(self, session_id: str, state: Mapping[str, Any]) -> None:
        with self._lock:
            self._states[session_id] = deepcopy(dict(state))
