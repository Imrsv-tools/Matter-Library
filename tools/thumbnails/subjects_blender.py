"""The thumbnail subjects the rig does not have, built in code (Phase17 17.2; Blender side).

Each builder returns ``(subjects, props)``: the meshes the article goes on, and the furniture that
shows it off (a patterned card behind glass, a dark ball under lace). Sizes are metres in the rig's
space (Y up), turned into Blender's by ``v``. Every subject mesh carries ONE UV map, ``st``, in
metres divided by the article's ``meters_per_tile``, as the rig's subjects do, so an article shows
at its recorded real size. See-through subjects are closed meshes (Learnings B4).
"""

from __future__ import annotations

import math

import bmesh
import bpy
from mathutils import Matrix, Vector

Y_UP = Matrix.Rotation(math.radians(90.0), 4, "X")      # the rig's space -> Blender's


def v(p) -> Vector:
    """A point in the rig's space, in Blender's."""
    return Y_UP @ Vector(p)


def place(p, origin=(0.0, 0.0, 0.0), yaw=0.0, pitch=0.0):
    """Rotate a local point by ``pitch`` about X, then ``yaw`` about Y (degrees), then move it."""
    x, y, z = p
    a, b = math.radians(pitch), math.radians(yaw)
    y, z = y * math.cos(a) - z * math.sin(a), y * math.sin(a) + z * math.cos(a)
    x, z = x * math.cos(b) + z * math.sin(b), -x * math.sin(b) + z * math.cos(b)
    return (x + origin[0], y + origin[1], z + origin[2])


def make_mesh(name, verts, faces, uvs, mpt, smooth=True, closed=False):
    """A mesh from rig-space points; ``uvs`` per point, in metres; its one UV map is ``st``."""
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v(p)) for p in verts], [], faces)
    uv = me.uv_layers.new(name="st")
    for poly in me.polygons:
        poly.use_smooth = smooth
        for li in poly.loop_indices:
            s, t = uvs[me.loops[li].vertex_index]
            uv.data[li].uv = (s / mpt, t / mpt)
    me.validate()
    me.update()
    if closed:                      # outward normals, whatever the winding was
        bm = bmesh.new()
        bm.from_mesh(me)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(me)
        bm.free()
    obj = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def flat_material(name, rgb, roughness=0.6):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*rgb, 1.0)
    b.inputs["Roughness"].default_value = roughness
    return m


def give(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def box(name, size, mpt, origin=(0, 0, 0), yaw=0.0, pitch=0.0, bevel=0.0):
    """A box resting on y = 0 (before ``pitch``), each face mapped in metres."""
    sx, sy, sz = size
    hx, hz = sx / 2, sz / 2
    verts, faces, uvs = [], [], []

    def quad(corners, st):
        b = len(verts)
        verts.extend(place(c, origin, yaw, pitch) for c in corners)
        uvs.extend(st)
        faces.append((b, b + 1, b + 2, b + 3))

    for sg in (1, -1):
        z = sg * hz
        quad([(-hx, 0, z), (hx, 0, z), (hx, sy, z), (-hx, sy, z)], [(0, 0), (sx, 0), (sx, sy), (0, sy)])
        x = sg * hx
        quad([(x, 0, -hz), (x, 0, hz), (x, sy, hz), (x, sy, -hz)], [(0, 0), (sz, 0), (sz, sy), (0, sy)])
        y = sy if sg > 0 else 0.0
        quad([(-hx, y, -hz), (hx, y, -hz), (hx, y, hz), (-hx, y, hz)], [(0, 0), (sx, 0), (sx, sz), (0, sz)])
    obj = make_mesh(name, verts, faces, uvs, mpt, smooth=False, closed=True)
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)      # weld the faces' corners
    if bevel:
        bmesh.ops.bevel(bm, geom=list(bm.edges), offset=bevel, segments=3, affect="EDGES",
                        profile=0.5)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    return obj


# ------------------------------------------------------------------ the subjects

def wall(mpt, props):
    """A wall section 1.0 x 0.8 x 0.12 m, turned so its end shows."""
    return [box("ML_Wall", (1.0, 0.8, 0.12), mpt, origin=(0.0, 0.0, -0.10), yaw=-25.0)], []


def pane(mpt, props):
    """A pane, 0.45 x 0.60 m, standing in front of a patterned card. ONE sheet: the TranslucentThin
    master is a thin wall, so a single surface is the whole pane (a closed box drew it twice, front
    face and back, and read frosted and doubly tinted, 17.2)."""
    w, h = 0.45, 0.60
    corners = [(-w / 2, 0.0, 0.0), (w / 2, 0.0, 0.0), (w / 2, h, 0.0), (-w / 2, h, 0.0)]
    glass = make_mesh("ML_Pane", [place(c, (0.0, 0.0, 0.10), -20.0) for c in corners], [(0, 1, 2, 3)],
                      [(c[0] + w / 2, c[1]) for c in corners], mpt, smooth=False)
    card = box("ML_PatternCard", (0.9, 0.9, 0.01), 1.0, origin=(0.05, 0.0, -0.35), yaw=-10.0)
    m = bpy.data.materials.new("ML_Checker")
    m.use_nodes = True
    nt = m.node_tree
    chk = nt.nodes.new("ShaderNodeTexChecker")
    chk.inputs["Scale"].default_value = 12.0
    chk.inputs["Color1"].default_value = (0.75, 0.75, 0.75, 1.0)
    chk.inputs["Color2"].default_value = (0.03, 0.03, 0.03, 1.0)
    nt.links.new(nt.nodes.new("ShaderNodeTexCoord").outputs["Generated"], chk.inputs["Vector"])
    nt.links.new(chk.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
    give(card, m)
    return [glass], [card]


def gem(mpt, props):
    """A round brilliant 25 mm across (57 % table, 34.5 deg crown, 40.75 deg pavilion), lying tilted
    towards the camera, and a 35 mm block beside it."""
    d = 0.025
    r, rt, girdle = d / 2, 0.285 * d, 0.012 * d
    crown = (r - rt) * math.tan(math.radians(34.5))
    pav = r * math.tan(math.radians(40.75))
    pts = []
    table = [(rt * math.cos(math.radians(45 * i + 22.5)), girdle + crown, rt * math.sin(math.radians(45 * i + 22.5)))
             for i in range(8)]
    top = [(r * math.cos(math.radians(22.5 * j)), girdle, r * math.sin(math.radians(22.5 * j))) for j in range(16)]
    bot = [(x, 0.0, z) for x, _, z in top]
    culet = (0.0, -pav, 0.0)
    pts = table + top + bot + [culet]
    T, G, B, C = 0, 8, 24, 40
    faces = [tuple(T + i for i in range(8))]
    for i in range(8):
        g0, g1, g2 = G + (2 * i) % 16, G + (2 * i + 1) % 16, G + (2 * i + 2) % 16
        faces += [(T + i, g0, g1), (T + i, g1, T + (i + 1) % 8), (T + (i + 1) % 8, g1, g2)]
    for j in range(16):
        faces.append((G + j, G + (j + 1) % 16, B + (j + 1) % 16, B + j))
        faces.append((B + j, B + (j + 1) % 16, C))
    # lie it tilted 60 degrees towards the camera, resting on the floor
    tilted = [place(p, pitch=60.0) for p in pts]
    lo = min(p[1] for p in tilted)
    placed = [(x - 0.022, y - lo, z) for x, y, z in tilted]
    uvs = [(p[0] + r, p[2] + r) for p in pts]
    stone = make_mesh("ML_Gem", placed, faces, uvs, mpt, smooth=False, closed=True)
    block = box("ML_Block", (0.035, 0.035, 0.035), mpt, origin=(0.028, 0.0, -0.012), yaw=30.0, bevel=0.0015)
    return [stone, block], []


FRAMES = 90          # the cloth's fall, in frames at 24 fps


def ball(name, r, seg=48):
    """A UV sphere of radius ``r`` resting on the floor at the origin (a closed mesh)."""
    verts, faces, uvs = [], [], []
    for j in range(seg + 1):
        ph = math.pi * j / seg
        for i in range(seg):
            th = 2 * math.pi * i / seg
            verts.append((r * math.sin(ph) * math.cos(th), r + r * math.cos(ph), r * math.sin(ph) * math.sin(th)))
            uvs.append((th * r, ph * r))
    for j in range(seg):
        for i in range(seg):
            a, b = j * seg + i, j * seg + (i + 1) % seg
            faces.append((a, b, b + seg, a + seg))
    obj = make_mesh(name, verts, faces, uvs, 1.0, closed=True)
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-7)      # the poles
    bm.to_mesh(obj.data)
    bm.free()
    return obj


def _drape(name, mpt, size, r, support_rgb, n=80):
    """A cloth ``size`` m square dropped onto a ball of radius ``r``: Blender's cloth simulation,
    run to rest and frozen into the mesh. Its st is the flat cloth's, in metres (cloth does not
    stretch). Deterministic on one Blender build, which the record names."""
    scn = bpy.context.scene
    h = size / 2
    verts, uvs, faces = [], [], []
    for j in range(n + 1):
        for i in range(n + 1):
            # a slight turn, so the folds do not line up with the camera
            verts.append(place((-h + size * i / n, 2 * r + 0.03, -h + size * j / n), yaw=17.0))
            uvs.append((size * i / n, size * j / n))
    for j in range(n):
        for i in range(n):
            a = j * (n + 1) + i
            faces.append((a, a + n + 1, a + n + 2, a + 1))      # wound so the normals face up
    cloth = make_mesh(name, verts, faces, uvs, mpt)
    support = ball(name + "Support", r)
    give(support, flat_material(name + "Support", support_rgb, 0.5))
    floor = make_mesh(name + "Floor", [(-2, 0, -2), (2, 0, -2), (2, 0, 2), (-2, 0, 2)], [(0, 3, 2, 1)],
                      [(0, 0)] * 4, 1.0)
    for o in (support, floor):
        o.modifiers.new("Collision", "COLLISION")
        o.collision.thickness_outer = 0.002
        o.collision.cloth_friction = 8.0
    mod = cloth.modifiers.new("Cloth", "CLOTH")
    st = mod.settings
    st.quality = 6
    st.mass = 0.2
    st.tension_stiffness = st.compression_stiffness = 12.0
    st.shear_stiffness = 6.0
    st.bending_stiffness = 0.6      # broad folds; softer creased into zig-zags at the mesh's size
    st.air_damping = 1.0
    mod.collision_settings.distance_min = 0.002
    # no self-collision: a cloth just big enough to reach the floor at its corners does not fold onto
    # itself much, and self-collision crumpled the spare into a heap and cost a minute (17.2)
    mod.collision_settings.use_self_collision = False
    mod.point_cache.frame_start, mod.point_cache.frame_end = 1, FRAMES
    scn.frame_start, scn.frame_end = 1, FRAMES
    for f in range(1, FRAMES + 1):
        scn.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    rest = bpy.data.meshes.new_from_object(cloth.evaluated_get(dg))
    cloth.modifiers.clear()
    old, cloth.data = cloth.data, rest
    bpy.data.meshes.remove(old)
    for p in rest.polygons:
        p.use_smooth = True
    sub = cloth.modifiers.new("Smooth", "SUBSURF")
    sub.levels = sub.render_levels = 1
    for o in (support, floor):
        o.modifiers.clear()
    bpy.data.objects.remove(floor)
    scn.frame_set(1)
    return cloth, support


def drape(mpt, props):
    """A textile: a cloth 0.5 m square dropped onto a 0.12 m ball, its corners on the floor."""
    cloth, support = _drape("ML_Cloth", mpt, 0.5, 0.12, (0.18, 0.18, 0.18))
    return [cloth], [support]


def lace(mpt, props):
    """Lace dropped onto a dark ball, so its holes read."""
    cloth, support = _drape("ML_Lace", mpt, 0.5, 0.12, (0.02, 0.018, 0.018))
    return [cloth], [support]


def tube(mpt, props):
    """An emitter: a tube 24 mm across bent into a ring 0.32 m across, standing on the floor."""
    R, rt, nu, nw = 0.16, 0.012, 192, 24
    yc = R + rt
    verts, uvs, faces = [], [], []
    for a in range(nu):
        u = 2 * math.pi * a / nu
        n1 = (math.cos(u), math.sin(u), 0.0)
        for b in range(nw):
            w = 2 * math.pi * b / nw
            verts.append((R * n1[0] + rt * math.cos(w) * n1[0], yc + R * n1[1] + rt * math.cos(w) * n1[1],
                          rt * math.sin(w)))
            uvs.append((R * u, rt * w))
    for a in range(nu):
        for b in range(nw):
            p, q = a * nw + b, ((a + 1) % nu) * nw + b
            faces.append((p, q, q - b + (b + 1) % nw, p - b + (b + 1) % nw))
    return [make_mesh("ML_Tube", verts, faces, uvs, mpt, closed=True)], []


def card(mpt, props):
    """A flat card 0.3 m square, 4 mm thick, standing and leaning back 8 degrees."""
    return [box("ML_Card", (0.30, 0.30, 0.004), mpt, pitch=-8.0)], []


def leaf(mpt, props):
    """Two leaf cards one tile across: one lying, one leaning up towards the camera."""
    s = mpt / 2

    def quad(name, corners, origin, yaw, pitch):
        pts = [place(c, origin, yaw, pitch) for c in corners]
        st = [(c[0] + s, c[2] - min(k[2] for k in corners)) for c in corners]
        return make_mesh(name, pts, [(0, 3, 2, 1)], st, mpt, smooth=False)

    lying = quad("ML_LeafLying", [(-s, 0, -s), (s, 0, -s), (s, 0, s), (-s, 0, s)],
                 (-0.045, 0.0015, 0.03), 25.0, 0.0)
    leaning = quad("ML_LeafLeaning", [(-s, 0, -2 * s), (s, 0, -2 * s), (s, 0, 0), (-s, 0, 0)],
                   (0.05, 0.0015, -0.005), -15.0, 35.0)
    return [lying, leaning], []


BUILDERS = {"wall": wall, "pane": pane, "gem": gem, "drape": drape, "lace": lace, "tube": tube,
            "card": card, "leaf": leaf}
