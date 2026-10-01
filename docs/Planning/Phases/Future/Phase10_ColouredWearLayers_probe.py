"""Phase10 discovery Pass 2 — the dust probe. Disposable: nothing in the library uses it.

    uv run docs/Planning/Phases/Future/Phase10_ColouredWearLayers_probe.py [out_dir]

Writes scratch copies of two articles (texture paths made absolute) with the dust layer drawn
four ways, renders each through the rig's own job writer and Storm driver at dust 0, 0.5 and 1,
and composes ``probe.jpg`` (close-up view) in ``out_dir`` (default ``/tmp/p10probe``):

  Oak (Dust01 = overlay 3)            Glass_Clear (Dust01 = overlay 1)
    today          roughness + bump      today
    fuzz           + fuzz in the colour  cover          + base colour mixed to the colour
    cover          + base colour mixed   cover, opaque  + transmission mixed to 0 as well
    fuzz + cover   both

Each change is driven by the overlay's existing effect (density x alpha x gate); the colour is a
declared value, never the layer's packed channels.
"""
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "tools/parity"))
sys.path.insert(0, str(REPO / "tools/parity/drivers"))
import job as jobmod  # noqa: E402
import storm  # noqa: E402

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/p10probe")
DUST = "0.35, 0.32, 0.27"          # linear; a probe value, not a grounded one
MAT = REPO / "MatterLibrary/materials"
CASES = {
    "Oak": (MAT / "natural/wood/Oak_Natural_Clean_Base_s1_v01.mtlx", 3,
            [("today", 0, 0, 0), ("fuzz", 1, 0, 0), ("cover", 0, 1, 0), ("fuzz + cover", 1, 1, 0)]),
    "Glass_Clear": (MAT / "engineered/glass/Glass_Clear_Clean_Base_s01_v01.mtlx", 1,
                    [("today", 0, 0, 0), ("cover", 0, 1, 0), ("cover, opaque", 0, 1, 1)]),
}


def _sub(parent, tag, name, typ, **inputs):
    n = ET.SubElement(parent, tag, name=name, type=typ)
    for k, (t, kind, v) in inputs.items():
        ET.SubElement(n, "input", {"name": k, "type": t, kind: v})


def variant(src: Path, slot: int, fuzz: int, cover: int, opaque: int, dest: Path) -> Path:
    tree = ET.parse(src)
    root = tree.getroot()
    for f in root.iter("input"):
        if f.get("type") == "filename" and f.get("value"):
            f.set("value", str((src.parent / f.get("value")).resolve()))
    ng, sr, eff = root.find("nodegraph"), root.find("open_pbr_surface"), f"overlay{slot}_effect"
    if ng.find(f"*[@name='{eff}']") is None:
        eff = f"overlay{slot}_effect_raw"              # no maskset: the ungated effect
    if cover:
        out = ng.find("output[@name='base_color_out']")
        _sub(ng, "mix", "dust_cover", "color3", bg=("color3", "nodename", out.get("nodename")),
             fg=("color3", "value", DUST), mix=("float", "nodename", eff))
        out.set("nodename", "dust_cover")
    if opaque:
        tw = sr.find("input[@name='transmission_weight']")
        _sub(ng, "mix", "dust_transmission", "float", bg=("float", "value", tw.get("value")),
             fg=("float", "value", "0.0"), mix=("float", "nodename", eff))
        ET.SubElement(ng, "output", name="transmission_out", type="float", nodename="dust_transmission")
        del tw.attrib["value"]
        tw.set("nodegraph", ng.get("name"))
        tw.set("output", "transmission_out")
    if fuzz:
        ET.SubElement(ng, "output", name="dust_fuzz_out", type="float", nodename=eff)
        ET.SubElement(sr, "input", {"name": "fuzz_weight", "type": "float",
                                    "nodegraph": ng.get("name"), "output": "dust_fuzz_out"})
        ET.SubElement(sr, "input", {"name": "fuzz_color", "type": "color3", "value": DUST})
        ET.SubElement(sr, "input", {"name": "fuzz_roughness", "type": "float", "value": "0.8"})
    p = dest / src.name
    p.parent.mkdir(parents=True, exist_ok=True)
    tree.write(p, xml_declaration=True, encoding="utf-8")
    return p


def main() -> None:
    cell, rows = 300, []
    for case, (src, slot, variants) in CASES.items():
        port = f"overlay{slot}_density"
        settings = [{"id": f"d{i}", "label": f"dust {v}", "port": port, "set": {port: v}}
                    for i, v in enumerate((0.0, 0.5, 1.0))]
        settings[0]["id"] = "defaults"
        for label, fz, cv, op in variants:
            d = OUT / case / label.replace(" ", "").replace(",", "_").replace("+", "_")
            art = jobmod.Article.read(variant(src, slot, fz, cv, op, d))
            storm.run(jobmod.write_job(art, settings, d / "render", 512, 64))
            pics = [d / "render/storm" / f"{s['id']}__close.png" for s in settings]
            a = np.asarray(Image.open(pics[0]).convert("RGB")).astype(float)
            b = np.asarray(Image.open(pics[2]).convert("RGB")).astype(float)
            moved = np.abs(a - b).sum(-1) > 3
            delta = float(np.abs(a - b)[moved].mean()) if moved.any() else 0.0
            print(f"{case:12s} {label:14s} dust 1 vs 0: moved {moved.mean() * 100:3.0f}% "
                  f"of the picture, mean change {delta:4.1f} levels")
            rows.append((f"{case}: {label}", pics))
    sheet = Image.new("RGB", (170 + cell * 3, 24 + cell * len(rows)), "white")
    draw = ImageDraw.Draw(sheet)
    for j, s in enumerate(("dust 0", "dust 0.5", "dust 1")):
        draw.text((180 + j * cell, 6), s, fill="black")
    for i, (label, pics) in enumerate(rows):
        draw.text((8, 24 + i * cell + cell // 2), label, fill="black")
        for j, p in enumerate(pics):
            sheet.paste(Image.open(p).convert("RGB").resize((cell, cell)), (170 + j * cell, 24 + i * cell))
    sheet.save(OUT / "probe.jpg", quality=82)
    print("sheet", OUT / "probe.jpg")


if __name__ == "__main__":
    main()
