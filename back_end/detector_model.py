from ultralytics import YOLO
import torch

if __name__ == '__main__':
    model = YOLO("yolov8n.pt")
    device = "cuda"
    print(f"Using device: {device}")
    model.train(data="C:\\Users\\alexd\\Documents\\Datasets\\People Detection.v8i.yolov8\\data.yaml",
                epochs=5, imgsz=640, device=device)
    model.save("C:\\Users\\alexd\\Documents\\GitHub\\Build4Good\\best.pt")