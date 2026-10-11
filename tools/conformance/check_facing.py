#!/usr/bin/env python3
"""Does every face of an asset look outward?  (Creator Asset Profile, rule 10)

    <pxr-python> tools/conformance/check_facing.py <an asset's root .usda / .usdc>

A DATED COPY, taken 2026-10-11 from IMRSV's asset tooling, where this check is defined and tested
(research 261011_R_AssetToolingAsks.md, AT-F5 and its Pass 4). That project is private for now;
when it is public this file gives way to a pinned version of its check. Change the check there,
and bring a new copy here: do not let the two drift.

Why it is asked: a material on a one-sided master (Opaque, TwoLayer, Emissive, Subsurface) is
drawn from the FRONT of each face only, in Unreal and so in Studio. A face wound the wrong way
round is then not drawn at all: the part is missing from the front and there from behind. Every
other look this repo has hides it (Cycles, Storm, and Blender's viewport with Backface Culling off).

For each mesh the points are welded by position and the mesh is split into pieces (faces joined
through a shared edge). Each CLOSED piece (every edge shared by exactly two faces) is asked which
way round each face would have to run for the whole piece to be wound one way AND enclose a
positive volume. That is USD's rightHanded rule, counter-clockwise seen from outside; a
leftHanded mesh and a mirroring transform are allowed for. A face that runs the other way looks
inward.

A piece that is not closed cannot be asked: a sheet has no outside. It is counted and named,
never passed, because on a one-sided master a sheet is seen from one side only.

It also prints what the file says of each mesh (doubleSided), which never makes a face show.
An unresolved material reference warns on stderr and does not matter here.

Exit 0 only when no face of a closed piece looks inward. Needs OpenUSD's Python and nothing else.
Self-test: test_check_facing.py.
"""
import sys
from collections import defaultdict, deque

from pxr import Gf, Usd, UsdGeom

WELD = 1e-5      # metres: two points closer than this are one point
FLAT = 1e-12     # cubic metres: a closed piece smaller than this has no inside to speak of


def pieces_of(faces):
    """Split welded faces into pieces. Returns [(face ids, closed?)] and each edge's users."""
    edges = defaultdict(list)                       # (low, high) -> [(face, +1 runs low to high | -1)]
    for f, vs in enumerate(faces):
        for a, b in zip(vs, vs[1:] + vs[:1]):
            edges[(min(a, b), max(a, b))].append((f, 1 if a < b else -1))
    parent = list(range(len(faces)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for users in edges.values():
        for f, _ in users[1:]:
            parent[find(f)] = find(users[0][0])
    groups = defaultdict(list)
    for f in range(len(faces)):
        groups[find(f)].append(f)
    open_faces = {f for users in edges.values() if len(users) != 2 for f, _ in users}
    return [(fs, not any(f in open_faces for f in fs)) for fs in groups.values()], edges


def inward_faces(fs, faces, edges, pts, handed):
    """The faces of one closed piece that look inward, or None when it cannot be told."""
    near = defaultdict(list)                        # face -> [(neighbour, True when the two disagree)]
    for (a, b), users in edges.items():
        (f, df), (g, dg) = users if len(users) == 2 else ((None, 0), (None, 0))
        if f is not None and f != g:
            near[f].append((g, df == dg))           # the same direction along a shared edge: they disagree
            near[g].append((f, df == dg))
    turned = {fs[0]: False}
    todo = deque([fs[0]])
    while todo:
        f = todo.popleft()
        for g, disagree in near[f]:
            want = turned[f] != disagree
            if g not in turned:
                turned[g] = want
                todo.append(g)
            elif turned[g] != want:
                return None                         # a surface with one side, like a Moebius strip
    volume = 0.0
    for f in fs:
        vs = faces[f]
        v = sum(Gf.Dot(pts[vs[0]], Gf.Cross(pts[a], pts[b])) for a, b in zip(vs[1:], vs[2:])) / 6.0
        volume += -v if turned[f] else v
    if abs(volume) < FLAT:
        return None
    wrong_way = volume * handed < 0                 # the faces NOT turned are then the inward ones
    return [f for f in fs if turned[f] != wrong_way]


def side_of(face, piece_points, pts):
    """Where on its piece a face sits, as the axis it should look along: '+Z' is the top."""
    centre = sum(piece_points, Gf.Vec3d(0)) / len(piece_points)
    out = sum((pts[v] for v in face), Gf.Vec3d(0)) / len(face) - centre
    a, b, c = (pts[v] for v in face[:3])
    normal = Gf.Cross(b - a, c - a)                 # which way it runs is not trusted; its axis is
    axis = max(range(3), key=lambda k: abs(normal[k]))
    return ("+" if out[axis] > 0 else "-") + "XYZ"[axis]


def main(path):
    stage = Usd.Stage.Open(path)
    if not stage:
        print(f"could not open {path}")
        return 2
    scale = UsdGeom.GetStageMetersPerUnit(stage)
    cache = UsdGeom.XformCache()
    rows, totals = [], defaultdict(int)
    for prim in Usd.PrimRange(stage.GetPseudoRoot(), Usd.TraverseInstanceProxies()):
        if not prim.IsA(UsdGeom.Mesh):
            continue
        mesh = UsdGeom.Mesh(prim)
        points, counts, index = (mesh.GetPointsAttr().Get(), mesh.GetFaceVertexCountsAttr().Get(),
                                 mesh.GetFaceVertexIndicesAttr().Get())
        if not points or not counts:
            continue
        to_world = cache.GetLocalToWorldTransform(prim)
        handed = 1.0
        if to_world.GetDeterminant() < 0:
            handed = -handed
        if mesh.GetOrientationAttr().Get() == UsdGeom.Tokens.leftHanded:
            handed = -handed
        ids, pts, weld = {}, {}, []
        for p in points:
            w = to_world.Transform(Gf.Vec3d(*p)) * scale
            key = tuple(round(c / WELD) for c in w)
            weld.append(ids.setdefault(key, len(ids)))
            pts[weld[-1]] = w
        faces, at = [], 0
        for c in counts:
            vs = [weld[i] for i in index[at:at + c]]
            at += c
            if len(set(vs)) >= 3:                   # a face squeezed to a line or a point is no face
                faces.append(vs)
        pieces, edges = pieces_of(faces)
        inward, unasked, sides = 0, 0, defaultdict(int)
        for fs, closed in pieces:
            wrong = inward_faces(fs, faces, edges, pts, handed) if closed else None
            if wrong is None:
                unasked += 1
                continue
            inward += len(wrong)
            piece_points = [pts[v] for v in {v for f in fs for v in faces[f]}]
            for f in wrong:
                sides[side_of(faces[f], piece_points, pts)] += 1
        double = bool(mesh.GetDoubleSidedAttr().Get())
        rows.append((prim.GetName(), len(faces), len(pieces), inward, unasked, double, dict(sorted(sides.items()))))
        totals["faces"] += len(faces)
        totals["inward"] += inward
        totals["unasked"] += unasked
        totals["double"] += double
        totals["bad"] += bool(inward)
    print(f"{'mesh':<22}{'faces':>6}{'pieces':>7}{'inward':>7}{'not asked':>10}  doubleSided")
    for name, n, p, bad, skip, double, sides in rows:
        where = f"   inside out on: {sides}" if bad else ""
        print(f"{name:<22}{n:>6}{p:>7}{bad:>7}{skip:>10}  {'yes' if double else 'no':<11}{where}")
    print(f"\n{len(rows)} meshes, {totals['faces']} faces · {totals['inward']} look inward, in {totals['bad']} meshes · "
          f"{totals['unasked']} pieces not closed, so not asked · {totals['double']} meshes marked doubleSided")
    print("FAIL: faces look inward" if totals["inward"] else "pass: no face of a closed piece looks inward")
    return 1 if totals["inward"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
