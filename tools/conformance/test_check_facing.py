#!/usr/bin/env python3
"""Self-test for check_facing.py: it must refuse a face wound the wrong way round before it is
trusted to pass anything (Creator Asset Profile, rule 10).

Each case is a small mesh written to a temporary USD file and asked through the check's own
`main`, as the command line asks it:
  * a box wound outward passes; the same box with ONE face turned round is refused, and so is
    the box with EVERY face turned (inside out);
  * a left-handed mesh is read by its own rule: the inside-out box marked leftHanded passes, and
    the outward box marked leftHanded is refused;
  * a box mirrored by its transform is read by USD's rule, under which a mirroring transform
    turns the winding round with it: the outward box, mirrored, still passes, and the
    inside-out box, mirrored, is still refused (whether a given consumer honours that is its own);
  * a sheet (one square) cannot be asked and is not refused: it has no outside;
  * the profile's own golden passes.

Run under the USD toolchain python (pxr):
    <pxr-python> tools/conformance/test_check_facing.py
Exit 0 = all pass.
"""
import contextlib
import io
import sys
import tempfile
from pathlib import Path

from pxr import Gf, Usd, UsdGeom

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_facing as C  # noqa: E402

GOLDEN = Path(__file__).resolve().parent / "golden" / "creator_table_lightweight.usda"
POINTS = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]          # index = 4x + 2y + z
OUTWARD = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
SHEET = [(0, 4, 6, 2)]


def asset(folder, name, faces, left=False, mirror=False):
    path = str(Path(folder) / f"{name}.usda")
    stage = Usd.Stage.CreateNew(path)
    UsdGeom.SetStageMetersPerUnit(stage, 1.0)
    xf = UsdGeom.Xform.Define(stage, "/root")
    if mirror:
        xf.AddScaleOp().Set(Gf.Vec3f(-1, 1, 1))
    mesh = UsdGeom.Mesh.Define(stage, "/root/Box")
    mesh.CreatePointsAttr(POINTS)
    mesh.CreateFaceVertexCountsAttr([len(f) for f in faces])
    mesh.CreateFaceVertexIndicesAttr([i for f in faces for i in f])
    if left:
        mesh.CreateOrientationAttr(UsdGeom.Tokens.leftHanded)
    stage.GetRootLayer().Save()
    return path


def ask(path):
    said = io.StringIO()
    with contextlib.redirect_stdout(said):
        code = C.main(path)
    return code, said.getvalue()


def main():
    turned = [tuple(reversed(f)) for f in OUTWARD]
    one = [turned[0]] + OUTWARD[1:]
    failed = 0
    with tempfile.TemporaryDirectory() as folder:
        cases = [
            ("a box wound outward", asset(folder, "outward", OUTWARD), 0, "0 look inward"),
            ("one face turned round", asset(folder, "one", one), 1, "1 look inward"),
            ("every face turned (inside out)", asset(folder, "inside_out", turned), 1, "6 look inward"),
            ("inside out, marked leftHanded", asset(folder, "left_ok", turned, left=True), 0, "0 look inward"),
            ("outward, marked leftHanded", asset(folder, "left_bad", OUTWARD, left=True), 1, "6 look inward"),
            ("outward, mirrored by its transform", asset(folder, "mirror", OUTWARD, mirror=True), 0, "0 look inward"),
            ("inside out, mirrored by its transform", asset(folder, "mirror_bad", turned, mirror=True), 1, "6 look inward"),
            ("a sheet: not asked, not refused", asset(folder, "sheet", SHEET), 0, "1 pieces not closed"),
            ("the profile's golden", str(GOLDEN), 0, "0 look inward"),
        ]
        for name, path, want, phrase in cases:
            code, said = ask(path)
            ok = code == want and phrase in said
            failed += not ok
            print(f"  [{'PASS' if ok else 'FAIL'}] {name}: exit {code} (want {want}), says '{phrase}': {phrase in said}")
    print(f"=> check_facing self-test: {'ALL PASS' if not failed else f'{failed} FAILED'}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
