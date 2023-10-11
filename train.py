import wandb
from wandb.integration.ultralytics import add_wandb_callback

from ultralytics import YOLO

model_name = "pretrained/best" #@param {type:"string"}
dataset_name = "data.yaml" #@param {type:"string"}

model = YOLO(f"{model_name}.pt")
add_wandb_callback(model, enable_model_checkpointing=True)
model.train(project="ultralytics", data=dataset_name, epochs=5, imgsz=1024,workers=36,visualize=True)
model.val(imgsz=1024)


wandb.finish()