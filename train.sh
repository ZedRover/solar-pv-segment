#!/bin/sh
yolo segment train \
data=data.yaml \
model=../yolov8s-seg-solar-panels/best.pt \
epochs=15 \
imgsz=2240 \
workers=112 \
visualize=true \
name=train \
cache=True \
