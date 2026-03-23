import threading
import time

_lock = threading.Lock()
_store: dict[str, tuple[float, dict]] = {}
_ttl_seconds = 300


def configure(ttl_seconds: int) -> None:
    global _ttl_seconds
    _ttl_seconds = max(0, int(ttl_seconds))


def get(key: str) -> dict | None:
    with _lock:
        entry = _store.get(key)
        if not entry:
            return None
        ts, payload = entry
        if time.time() - ts > _ttl_seconds:
            del _store[key]
            return None
        return payload


def set(key: str, payload: dict) -> None:
    with _lock:
        _store[key] = (time.time(), payload)
