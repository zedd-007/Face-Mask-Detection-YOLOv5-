# detector.py
import torch
import streamlit as st
import numpy as np
from PIL import Image
from utils_local import draw_boxes

@st.cache_resource
def load_model(model_path):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=False)
    return model

def detect_faces(model, image):
    results = model(image)
    results.render()  # In-place rendering
    return Image.fromarray(results.ims[0])