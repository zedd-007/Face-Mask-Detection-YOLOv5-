# utils.py
# Currently unused but available for future bounding box drawing, etc.

import cv2
import numpy as np
from PIL import Image, ImageDraw

def draw_boxes(image: Image, boxes, labels):
    draw = ImageDraw.Draw(image)
    for box, label in zip(boxes, labels):
        x1, y1, x2, y2 = map(int, box)
        draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
        draw.text((x1, y1 - 10), label, fill="white")
    return image