import sys, time, pickle
import numpy as np
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import headrender as hr
OUT = __import__("os").environ.get("PROBE_OUT", "/tmp/skinprobe")
YAWS = [0, -40, 40, -80, 80]
P, vt, T, vn = hr.head_mesh()
print("head tris", len(T))
alb, c = hr.albedo("", "III")
views = {}
for y in YAWS:
    t = time.time()
    cam = hr.camera(y)
    r = hr.render(cam, P, vt, T, vn)
    views[y] = (cam, r)
    hr.save(f"{OUT}/view_{y:+04d}_skin.png", hr.picture(cam, r, alb))
    zf = r["z"][r["mask"]]
    print(y, "cover", round(r["mask"].mean(), 3), "z", round(zf.min(), 3), round(zf.max(), 3), round(time.time() - t, 1), "s")
pickle.dump(views, open(f"{OUT}/views.pkl", "wb"))
