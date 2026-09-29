"""Probe 1: list Epic's MX_OpenPBR_Opaque inputs, build an Opaque master that wraps it, and a constant dome cubemap.

Run as a commandlet (no GPU):
  UnrealEditor-Cmd MatterProbe.uproject -run=pythonscript -script=<this> -EnablePlugins=PythonScriptPlugin,EditorScriptingUtilities -unattended -nullrhi
"""
import math
import os
import struct

import unreal

MEL = unreal.MaterialEditingLibrary
EAL = unreal.EditorAssetLibrary
TOOLS = unreal.AssetToolsHelpers.get_asset_tools()
PROJECT = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())

# OpenPBR defaults (Interchange's MaterialX definitions, 5.8) for the inputs the probe exposes.
DEFAULTS = {
    "base_weight": 1.0, "base_color": (0.8, 0.8, 0.8), "base_diffuse_roughness": 0.0, "base_metalness": 0.0,
    "specular_weight": 1.0, "specular_color": (1, 1, 1), "specular_roughness": 0.3, "specular_ior": 1.5,
    "specular_roughness_anisotropy": 0.0, "coat_weight": 0.0, "coat_color": (1, 1, 1), "coat_roughness": 0.0,
    "coat_ior": 1.6, "fuzz_weight": 0.0, "fuzz_color": (1, 1, 1), "fuzz_roughness": 0.5,
    "subsurface_weight": 0.0, "subsurface_color": (0.8, 0.8, 0.8), "emission_luminance": 0.0,
    "emission_color": (1, 1, 1), "geometry_opacity": 1.0,
}


def log(msg):
    unreal.log("MATTERPROBE " + msg)


def describe(fn_path):
    """List a function's inputs and outputs by calling it from a throwaway material (not saved)."""
    fn = unreal.load_asset(fn_path)
    if fn is None:
        log(f"describe {fn_path}: not found")
        return
    tmp = unreal.Material()
    call = MEL.create_material_expression(tmp, unreal.MaterialExpressionMaterialFunctionCall, 0, 0)
    call.set_material_function(fn)
    ins = MEL.get_material_expression_input_names(call)
    types = MEL.get_material_expression_input_types(call)
    log(f"describe {fn_path}: inputs({len(ins)})=" + ",".join(f"{n}:{t}" for n, t in zip(ins, types)))
    log(f"describe {fn_path}: outputs={list(MEL.get_material_expression_output_names(call))}")


def build_master():
    fn = unreal.load_asset("/Engine/Functions/Substrate/MF_Substrate_OpenPBR_Opaque")
    log(f"function={fn}")
    if fn is None:
        return False
    path, name = "/Game/Masters", "M_Matter_Opaque"
    if EAL.does_asset_exist(f"{path}/{name}"):
        log("master exists; delete Content/Masters and rerun for a fresh build")
        return True
    mat = TOOLS.create_asset(name, path, unreal.Material, unreal.MaterialFactoryNew())
    call = MEL.create_material_expression(mat, unreal.MaterialExpressionMaterialFunctionCall, -400, 0)
    call.set_material_function(fn)
    ins = MEL.get_material_expression_input_names(call)
    types = MEL.get_material_expression_input_types(call)
    outs = MEL.get_material_expression_output_names(call)
    log(f"inputs({len(ins)})=" + ",".join(f"{n}:{t}" for n, t in zip(ins, types)))
    log(f"outputs={list(outs)}")

    y = 0
    wired = []
    for n in ins:
        if n not in DEFAULTS:
            continue
        d = DEFAULTS[n]
        if isinstance(d, tuple):
            p = MEL.create_material_expression(mat, unreal.MaterialExpressionVectorParameter, -900, y)
            p.set_editor_property("parameter_name", n)
            p.set_editor_property("default_value", unreal.LinearColor(d[0], d[1], d[2], 1.0))
        else:
            p = MEL.create_material_expression(mat, unreal.MaterialExpressionScalarParameter, -900, y)
            p.set_editor_property("parameter_name", n)
            p.set_editor_property("default_value", float(d))
        if MEL.connect_material_expressions(p, "", call, n):
            wired.append(n)
        y += 90
    log(f"wired({len(wired)})=" + ",".join(wired))

    front = next((o for o in outs if "front" in o.lower()), outs[0] if outs else "")
    ok = MEL.connect_material_property(call, front, unreal.MaterialProperty.MP_FRONT_MATERIAL)
    log(f"front_output={front!r} connected={ok}")
    MEL.recompile_material(mat)
    saved = EAL.save_loaded_asset(mat)
    log(f"master saved={saved} scalars={list(MEL.get_scalar_parameter_names(mat))} vectors={list(MEL.get_vector_parameter_names(mat))}")
    return ok and saved


def write_constant_hdr(path, value=0.503, w=64, h=32):
    m, e = math.frexp(value)
    b = int(m * 256.0)
    pixel = bytes([b, b, b, e + 128])
    with open(path, "wb") as f:
        f.write(b"#?RADIANCE\nFORMAT=32-bit_rle_rgbe\n\n")
        f.write(f"-Y {h} +X {w}\n".encode())
        f.write(pixel * (w * h))


def build_dome():
    if EAL.does_asset_exist("/Game/Env/T_Dome"):
        log("dome exists")
        return True
    src = os.path.join(PROJECT, "Scripts", "dome_0503.hdr")
    write_constant_hdr(src)
    task = unreal.AssetImportTask()
    task.set_editor_property("filename", src)
    task.set_editor_property("destination_path", "/Game/Env")
    task.set_editor_property("destination_name", "T_Dome")
    task.set_editor_property("automated", True)
    task.set_editor_property("save", True)
    TOOLS.import_asset_tasks([task])
    objs = list(task.get_editor_property("imported_object_paths"))
    asset = unreal.load_asset("/Game/Env/T_Dome")
    log(f"dome imported={objs} class={asset.get_class().get_name() if asset else None}")
    return asset is not None


for f in ("/Engine/Functions/Substrate/MF_Substrate_OpenPBR_Translucent", "/InterchangeAssets/Functions/MX_OpenPBR_Translucent"):
    describe(f)
ok_m = build_master()
ok_d = build_dome()
log(f"RESULT master={ok_m} dome={ok_d}")
