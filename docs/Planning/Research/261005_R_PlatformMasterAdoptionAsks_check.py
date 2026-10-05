"""A TEST FIXTURE, NOT UNREAL. The check behind `261005_R_PlatformMasterAdoptionAsks.md` Pass 4.

It runs `unreal/MatterRuntime/Scripts/build_masters.py` against a stand-in ``unreal`` module that
records every call the script makes (nodes, properties, links, assets, log lines), and compares
the builder as it is now against the builder before the consumer switches (`BASELINE`), with no
switch set and under each switch in turn.

It proves what the SCRIPT asks the engine for. It proves nothing about what the engine compiles
or draws: every property and enum name here is taken on trust from the script.

    python3 docs/Planning/Research/261005_R_PlatformMasterAdoptionAsks_check.py

It is a record of the check made on 2026-10-05. A later change to the masters themselves makes
its first line fail by design: the baseline is a fixed commit, not the last one.
"""
import collections
import json
import os
import runpy
import subprocess
import sys
import tempfile
import types
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
BUILDER = "unreal/MatterRuntime/Scripts/build_masters.py"
BASELINE = "228bb2f"     # the builder before the switches
SWITCHES = ["MATTER_MASTERS_ROOT", "MATTER_MASTERS_SKINNED", "MATTER_MASTERS_MESH_V", "MATTER_MASTERS_MESH_BINORMAL",
            "MATTER_MASTERS_SKY", "MATTER_MASTERS_COLOUR_SAMPLER", "MATTER_MASTERS_REFRACTION"]

# ---------------------------------------------------------------- the stand-in (--record)

# Epic's two OpenPBR functions as the library's learnings record them (Learnings Unreal U1): the
# inputs the builder feeds, and the outputs (Translucent adds the refraction one).
INPUTS = [
    "base_color", "base_metalness", "specular_roughness", "geometry_normal", "geometry_opacity",
    "geometry_thin_walled", "base_weight", "base_diffuse_roughness", "specular_weight", "specular_color",
    "specular_ior", "specular_roughness_anisotropy", "coat_weight", "coat_color", "coat_roughness",
    "coat_ior", "fuzz_weight", "fuzz_color", "fuzz_roughness", "emission_luminance", "emission_color",
    "subsurface_weight", "subsurface_color", "subsurface_radius", "subsurface_radius_scale",
    "subsurface_scatter_anisotropy", "transmission_weight", "transmission_color", "transmission_depth",
]


def record(script, out, saved):
    trace, count, loaded = [], {}, {}

    def rep(v):
        if isinstance(v, (Obj, Sym)):
            return repr(v)
        if isinstance(v, float):
            return round(v, 9)
        if isinstance(v, (list, tuple)):
            return [rep(x) for x in v]
        return v

    class Obj:
        """An engine object: a node, a material, a texture, an import task."""

        def __init__(self, kind, mat=None):
            count[kind] = count.get(kind, 0) + 1
            self.kind, self.id, self.mat = kind, f"{kind}#{count[kind]}", mat
            self.props, self.fn, self.params = {}, None, {"scalar": [], "vector": []}

        def __repr__(self):
            return self.id

        def get_name(self):
            return self.id

        def set_editor_property(self, k, v):
            self.props[k] = v
            trace.append(["set", self.id, k, rep(v)])
            if k == "parameter_name" and self.mat is not None:
                which = "scalar" if "Scalar" in self.kind else "vector" if "Vector" in self.kind else None
                if which:
                    self.mat.params[which].append(v)

        def set_material_function(self, fn):
            self.fn = fn
            trace.append(["function", self.id, rep(fn)])

    class Sym:
        """Any other name in the module: a class, an enum and its members, a factory."""

        def __init__(self, name):
            self._name = name

        def __repr__(self):
            return self._name

        def __getattr__(self, attr):
            if attr.startswith("__"):
                raise AttributeError(attr)
            return Sym(f"{self._name}.{attr}")

        def __call__(self, *a, **k):
            return Obj(self._name)

    class MEL:
        @staticmethod
        def create_material_expression(mat, cls, x, y):
            n = Obj(repr(cls), mat)
            trace.append(["node", n.id, repr(mat), x, y])
            return n

        @staticmethod
        def connect_material_expressions(src, src_out, dst, dst_in):
            trace.append(["link", repr(src), src_out, repr(dst), dst_in])
            return True

        @staticmethod
        def connect_material_property(src, src_out, prop):
            trace.append(["property", repr(src), src_out, repr(prop)])
            return True

        @staticmethod
        def get_material_expression_input_names(call):
            return list(INPUTS)

        @staticmethod
        def get_material_expression_output_names(call):
            outs = ["OpenPBR_FrontMaterial", "OpacityMask"]
            return outs + (["Refraction (IOR)"] if "Translucent" in repr(call.fn) else [])

        @staticmethod
        def recompile_material(mat):
            trace.append(["recompile", repr(mat)])

        @staticmethod
        def get_scalar_parameter_names(mat):
            return list(mat.params["scalar"])

        @staticmethod
        def get_vector_parameter_names(mat):
            return list(mat.params["vector"])

    class EAL:
        @staticmethod
        def does_asset_exist(path):
            return False

        @staticmethod
        def delete_asset(path):
            trace.append(["delete", path])

        @staticmethod
        def save_loaded_asset(asset):
            trace.append(["save", repr(asset)])
            return True

    class Tools:
        def create_asset(self, name, root, cls, factory):
            trace.append(["asset", root, name, repr(cls)])
            return Obj(f"asset:{root}/{name}")

        def import_asset_tasks(self, tasks):
            trace.append(["import", [{k: rep(v) for k, v in t.props.items() if k != "filename"} for t in tasks]])

    class Paths:
        @staticmethod
        def project_saved_dir():
            return saved.rstrip("/") + "/"

        @staticmethod
        def convert_relative_path_to_full(p):
            return p

    def load_asset(path):
        if path not in loaded:
            loaded[path] = Obj(f"loaded:{path}")
        return loaded[path]

    stub = types.ModuleType("unreal")
    stub.MaterialEditingLibrary = MEL
    stub.EditorAssetLibrary = EAL
    stub.AssetToolsHelpers = types.SimpleNamespace(get_asset_tools=lambda: Tools())
    stub.Paths = Paths
    stub.load_asset = load_asset
    stub.LinearColor = lambda r, g, b, a: ("LinearColor", round(r, 9), round(g, 9), round(b, 9), round(a, 9))
    stub.log = lambda msg: trace.append(["log", msg])
    stub.__getattr__ = lambda name: Sym(name)
    sys.modules["unreal"] = stub
    try:
        runpy.run_path(script, run_name="__main__")
        trace.append(["exit", "ok"])
    except Exception as e:      # a refused switch is a result too
        trace.append(["exit", f"{type(e).__name__}: {e}"])
    Path(out).write_text(json.dumps(trace))


# ---------------------------------------------------------------- the check

def main():
    tmp = Path(tempfile.mkdtemp(prefix="matter-masters-check-"))
    old = tmp / "build_masters_baseline.py"
    old.write_text(subprocess.run(["git", "-C", str(REPO), "show", f"{BASELINE}:{BUILDER}"],
                                  check=True, capture_output=True, text=True).stdout)
    new = REPO / BUILDER
    fails = []

    def run(script, tag, **env):
        e = {k: v for k, v in os.environ.items() if k not in SWITCHES}
        e.update(env)
        out = tmp / f"trace_{tag}.json"
        subprocess.run([sys.executable, __file__, "--record", str(script), str(out), str(tmp / "Saved")],
                       env=e, check=True)
        return json.loads(out.read_text())

    def check(name, ok, detail=""):
        print(("PASS  " if ok else "FAIL  ") + name + (f"  [{detail}]" if detail else ""))
        if not ok:
            fails.append(name)

    def nodes(t, cls):
        return [x for x in t if x[0] == "node" and x[1].split("#")[0] == "MaterialExpression" + cls]

    def by_kind(t):
        return collections.Counter(x[1].split("#")[0].replace("MaterialExpression", "")
                                   for x in t if x[0] == "node")

    head = run(old, "baseline")
    dflt = run(new, "default")

    # 1. no switch set: call for call the baseline, plus one log line saying what it was told
    told = [x for x in dflt if x[0] == "log" and x[1].startswith("MATTER told ")]
    rest = [x for x in dflt if not (x[0] == "log" and x[1].startswith("MATTER told "))]
    check("no switch: identical to the builder before the switches, call for call", rest == head,
          f"{len(rest)} calls vs {len(head)}")
    check("no switch: one line says what the build was told", len(told) == 1, told[0][1] if told else "")

    # 2. the destination
    t = run(new, "root", MATTER_MASTERS_ROOT="/Game/Matter/Masters")
    roots = {x[1] for x in t if x[0] == "asset"} | {x[1][0]["destination_path"] for x in t if x[0] == "import"}
    check("root: every master and default texture goes to the told path", roots == {"/Game/Matter/Masters"}, str(roots))
    check("root: nothing else differs", json.loads(json.dumps(t).replace("/Game/Matter/Masters", "/Game/Masters")) == dflt)

    # 3. skinned
    t = run(new, "skinned", MATTER_MASTERS_SKINNED="1")
    usage = collections.Counter(x[2] for x in t if x[0] == "set" and x[2].startswith("used_with_") and x[3] is True)
    check("skinned: both usages set on the eight masters, not on the Sky",
          usage == {"used_with_skeletal_mesh": 8, "used_with_morph_targets": 8}
          and not any(x[0] == "set" and "Sky" in x[1] and x[2].startswith("used_with_") for x in t), str(dict(usage)))
    check("skinned: no node added or removed", by_kind(t) == by_kind(dflt))

    # 4. the mesh's V: every mesh coordinate is turned back before anything reads it
    t = run(new, "meshv", MATTER_MASTERS_MESH_V="unreal")
    coords = [x[1] for x in nodes(t, "TextureCoordinate")]
    ok = True
    for c in coords:
        outs = [x for x in t if x[0] == "link" and x[1] == c]
        if len(outs) != 1 or not outs[0][3].startswith("MaterialExpressionMultiply"):
            ok = False
            continue
        mul = outs[0][3]
        other = [x[1] for x in t if x[0] == "link" and x[3] == mul and x[1] != c]
        k = {x[2]: x[3] for x in t if x[0] == "set" and other and x[1] == other[0]}
        add = [x[3] for x in t if x[0] == "link" and x[1] == mul]
        k2 = {}
        if len(add) == 1 and add[0].startswith("MaterialExpressionAdd"):
            o2 = [x[1] for x in t if x[0] == "link" and x[3] == add[0] and x[1] != mul]
            k2 = {x[2]: x[3] for x in t if x[0] == "set" and o2 and x[1] == o2[0]}
        ok = ok and k == {"r": 1.0, "g": -1.0} and k2 == {"r": 0.0, "g": 1.0}
    check("mesh V: each mesh coordinate is turned to (u, 1 - v) before anything reads it", ok and len(coords) > 0,
          f"{len(coords)} coordinates in 8 masters")
    d = by_kind(t) - by_kind(dflt)
    check("mesh V: adds only that turn",
          d == {"Multiply": len(coords), "Add": len(coords), "Constant2Vector": 2 * len(coords)}
          and not (by_kind(dflt) - by_kind(t)), str(dict(d)))
    check("mesh V: same parameters", [x for x in t if x[0] == "log"][1:] == [x for x in dflt if x[0] == "log"][1:])

    # 5. the binormal: Y negated once per master, on what the last normalise reads
    t = run(new, "binormal", MATTER_MASTERS_MESH_BINORMAL="unreal")
    c3 = nodes(t, "Constant3Vector")
    vals = {tuple(x[3]) for x in t if x[0] == "set" and x[1] in {n[1] for n in c3} and x[2] == "constant"}
    ok = len(c3) == 8 and vals == {("LinearColor", 1.0, -1.0, 1.0, 0.0)}
    for n in c3:
        mul = [x[3] for x in t if x[0] == "link" and x[1] == n[1]]
        nxt = [x[3] for x in t if x[0] == "link" and mul and x[1] == mul[0]]
        ok = ok and len(mul) == 1 and len(nxt) == 1 and nxt[0].startswith("MaterialExpressionNormalize")
    check("binormal: the summed normal's Y is negated once per master, into the last normalise", ok, f"{len(c3)} masters")
    d = by_kind(t) - by_kind(dflt)
    check("binormal: adds only that", d == {"Multiply": 8, "Constant3Vector": 8}, str(dict(d)))

    # 6. no Sky
    t = run(new, "nosky", MATTER_MASTERS_SKY="0")
    names = [x[2] for x in t if x[0] == "asset"]
    check("sky off: the eight masters and no Sky", len(names) == 8 and "M_Matter_Sky" not in names)

    # 7. candidate: the colour slots sample sRGB
    t = run(new, "colour", MATTER_MASTERS_COLOUR_SAMPLER="srgb")
    samp = {}
    for x in t:
        if x[0] == "set" and x[1].startswith("MaterialExpressionTextureSampleParameter2D"):
            samp.setdefault(x[1], {})[x[2]] = x[3]
    kinds = collections.defaultdict(set)
    for s in samp.values():
        kinds[s["parameter_name"]].add((s["sampler_type"].split(".")[-1], s["texture"]))
    colour = {k for k, v in kinds.items() if any(a == "SAMPLERTYPE_COLOR" for a, _ in v)}
    check("colour sampler: exactly the three colour slots sample sRGB",
          colour == {"base_color_tex", "layer2_base_color_tex", "base_color_map_tex"}, ", ".join(sorted(colour)))
    check("colour sampler: each takes the sRGB white default, and no slot mixes the two",
          all(len(v) == 1 for v in kinds.values())
          and all("WhiteColour" in tex for k in colour for _, tex in kinds[k])
          and not any("WhiteColour" in tex for k in kinds if k not in colour for _, tex in kinds[k]))

    # 8. candidate: refraction by the index
    t = run(new, "refraction", MATTER_MASTERS_REFRACTION="index")
    src = {}
    for x in [x for x in t if x[0] == "property" and x[3].endswith("MP_REFRACTION")]:
        p = {y[2]: y[3] for y in t if y[0] == "set" and y[1] == x[1]}
        mat = next(y[2] for y in t if y[0] == "node" and y[1] == x[1])
        src[mat.split("M_Matter_")[1].split("#")[0]] = (x[1].split("#")[0].replace("MaterialExpression", ""), p)
    check("refraction: the thin master takes the constant 1.0", src.get("TranslucentThin") == ("Constant", {"r": 1.0}))
    check("refraction: the solid master takes the article's specular_ior parameter",
          src.get("TranslucentThick", ("", {}))[0] == "ScalarParameter"
          and src["TranslucentThick"][1].get("parameter_name") == "specular_ior")
    check("refraction: the index still reaches Epic's function on both",
          sum(1 for x in t if x[0] == "link" and x[4] == "specular_ior")
          == sum(1 for x in dflt if x[0] == "link" and x[4] == "specular_ior"))

    # 9. everything at once, as a consumer would build
    t = run(new, "all", MATTER_MASTERS_ROOT="/Game/Matter/Masters", MATTER_MASTERS_SKINNED="1",
            MATTER_MASTERS_MESH_V="unreal", MATTER_MASTERS_MESH_BINORMAL="unreal", MATTER_MASTERS_SKY="0",
            MATTER_MASTERS_COLOUR_SAMPLER="srgb", MATTER_MASTERS_REFRACTION="index")
    check("all switches together: the script completes", t[-1] == ["exit", "ok"], t[-1][1])

    # 10. a value it does not know stops the build before any asset is made
    for k, v in (("MATTER_MASTERS_MESH_V", "flipped"), ("MATTER_MASTERS_SKINNED", "yes"),
                 ("MATTER_MASTERS_ROOT", "Game/Masters/")):
        t = run(new, "bad", **{k: v})
        check(f"refused: {k}={v}", t[-1][1].startswith("RuntimeError") and not any(x[0] == "asset" for x in t))

    print("\n" + ("ALL PASS" if not fails else f"{len(fails)} FAILED: {fails}"))
    return 1 if fails else 0


if __name__ == "__main__":
    if len(sys.argv) == 5 and sys.argv[1] == "--record":
        record(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        sys.exit(main())
