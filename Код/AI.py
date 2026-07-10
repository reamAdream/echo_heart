import os.path
from ultralytics import YOLO
import sys, os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

model = YOLO(resource_path('best.pt'))

def Naming(name):
    results = model.predict(source=name, conf=0.5, save=True, exist_ok=True, name="ECG_Results")
    counts = {'acute_mi': 0, 'anomaly': 0, 'normal': 0}

    for r in results:
        for box in r.boxes:
            class_id = int(box.cls[0])
            label = model.names[class_id]
            counts[label] += 1
    return counts
