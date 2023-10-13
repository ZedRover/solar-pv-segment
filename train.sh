#!/bin/sh
yolo segment train \
data=data.yaml \
model=pretrained/best.pt \
epochs=1 \
imgsz=1024 \
workers=36 \
visualize=true \
name=train 