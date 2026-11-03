"""look.py with the skin article drawn as committed at 3d594fb (the pinned runtime refuses the tree's;
Phase25 25.1.15, Phase27 F-P27-6). Its default column is that OLD map: what ships is the T candidate."""
import sys
import tempfile
from pathlib import Path
REPO = Path(__file__).resolve().parents[4]   # docs/Planning/Research/<probe>/ -> the repo
sys.path.insert(0, str(REPO / "tools/parity"))
import look  # noqa: E402

_read = look.jobmod.Article.read
_folder = Path(tempfile.mkdtemp(prefix="look3d594fb_"))


def read(path, *a, **k):
    art = _read(path, *a, **k)
    if "Skin_Tone34" in str(path) and str(Path(path).resolve()).startswith(str(look.jobmod.REPO)):
        return look.today_article(art, "3d594fb", _folder)
    return art


look.jobmod.Article.read = staticmethod(read)
sys.exit(look.main(sys.argv[1:]))
