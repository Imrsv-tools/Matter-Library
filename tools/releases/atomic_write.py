"""Writing a file whole (2026-11-15): into a temp file beside it, then one rename onto it, so no
reader (another session, the dev server, Stage) ever sees half a file.

The temp's name is its writer's own (process and thread), so two sessions, or two of the dev
server's encode threads, never write into one temp; it starts with a dot and ends ``.tmp``, so a
glob for the real files never sees it. It is removed whatever happens.
"""

from __future__ import annotations

import os
import threading
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def replacing(dest: Path):
    """Yield the temp path to write; when the block ends without an error, it becomes ``dest``."""
    tmp = dest.with_name(f".{dest.name}.{os.getpid()}-{threading.get_ident()}.tmp")
    try:
        yield tmp
        os.replace(tmp, dest)
    finally:
        tmp.unlink(missing_ok=True)


def write_bytes(dest: Path, data: bytes) -> None:
    with replacing(dest) as tmp:
        tmp.write_bytes(data)
