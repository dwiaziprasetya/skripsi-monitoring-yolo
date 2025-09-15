import cv2
from ultralytics import YOLO
import os
import random

model_path = os.path.join("model", "model.pt")
model = YOLO(model_path)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Kamera tidak bisa dibuka")
    exit()

class_colors = {}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    for result in results:
        boxes = result.boxes.xyxy
        classes = result.boxes.cls
        names = result.names

        for box, cls in zip(boxes, classes):
            x1, y1, x2, y2 = map(int, box)
            cls = int(cls)

            if cls not in class_colors:
                class_colors[cls] = tuple(random.choices(range(50, 256), k=3))
            color = class_colors[cls]

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            label = names[cls]
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.6
            thickness = 2

            (w, h), _ = cv2.getTextSize(label, font, font_scale, thickness)
            cv2.rectangle(frame, (x1, y1 - h - 5), (x1 + w, y1), color, -1)
            cv2.putText(frame, label, (x1, y1 - 5), font, font_scale, (255, 255, 255), thickness)

    cv2.imshow("YOLO Detection - Label Background", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
