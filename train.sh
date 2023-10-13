#!/bin/sh
yolo segment train \
data=data.yaml \
model=yolov8s-seg \
# model=../yolov8s-seg-solar-panels/best.pt \
batch=32 \
epochs=500 \
imgsz=1500 \
workers=100 \
visualize=true \
name=train_new \
cache=True \
