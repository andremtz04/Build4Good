from ultralytics import YOLO
import torch
from roboflow import Roboflow
import os
from dotenv import load_dotenv

rf = Roboflow(api_key=os.getenv("ROBOFLOW_API_KEY"))
project = rf.workspace("leo-ueno").project("people-detection-o4rdr")
dataset = project.version(8).download("yolov8")

if __name__ == '__main__':
    model = YOLO("yolov8n.pt")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    model.train(data="C:\\Users\\Alejandro Garza\\Documents\\GitHub\\KEW\\People-Detection-8\\data.yaml",
                epochs=50, imgsz=640, device=device)
    model.save("C:\\Users\\Alejandro Garza\\Documents\\GitHub\\KEW\\back_end\\models\\best.pt")