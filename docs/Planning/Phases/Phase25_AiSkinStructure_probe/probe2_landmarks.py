"""Run MediaPipe Face Landmarker on pictures; save (478,2) pixel landmarks as .npy and an overlay."""
import sys, numpy as np, mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
from PIL import Image, ImageDraw
model, pairs = sys.argv[1], sys.argv[2:]
opt = vision.FaceLandmarkerOptions(base_options=mpt.BaseOptions(model_asset_path=model), num_faces=2,
                                   min_face_detection_confidence=0.2, min_face_presence_confidence=0.2)
det = vision.FaceLandmarker.create_from_options(opt)
for i in range(0, len(pairs), 2):
    src, out = pairs[i], pairs[i + 1]
    im = Image.open(src).convert("RGB"); w, h = im.size
    r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.asarray(im).copy()))
    print(src.split("/")[-1], "faces:", len(r.face_landmarks))
    if not r.face_landmarks: continue
    fs = [np.array([[q.x * w, q.y * h] for q in f]) for f in r.face_landmarks]
    for f in fs: print('  face span', f.min(0).round(), f.max(0).round())
    p = max(fs, key=lambda f: np.ptp(f[:, 0]) * np.ptp(f[:, 1])); np.save(out + ".npy", p)
    d = ImageDraw.Draw(im)
    for x, y in p: d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(0, 255, 0))
    im.save(out + "_overlay.jpg", quality=90)
