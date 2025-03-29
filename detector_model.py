from ultralytics import YOLO
import torch

if __name__ == '__main__':
    model = YOLO("yolov8n.pt")
    device = "cuda"
    print(f"Using device: {device}")
    model.train(data="C:\\Users\\alexd\\Documents\\Datasets\\People Detection.v8i.yolov8\\data.yaml",
                epochs=5, imgsz=640, device=device)
    model.save("C:\\Users\\alexd\\Documents\\GitHub\\Build4Good\\best.pt")

#trained_model = YOLO("best.pt")



#from roboflow import Roboflow
#from constants import ROBOFLOW_API_KEY, HUMAN_DATASET_PATH

#rf = Roboflow(api_key=ROBOFLOW_API_KEY)
#project = rf.workspace().project(HUMAN_DATASET_PATH)
#dataset = project.version(8).download("yolov8")