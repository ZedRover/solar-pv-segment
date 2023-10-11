import cv2
import os
import numpy as np
from tqdm import tqdm 
def convert_yolo_to_mask(label_path, img_path, output_path):
    # 读取图像的尺寸
    img = cv2.imread(img_path)
    h, w = img.shape[:2]

    # 创建一个全0的mask
    mask = np.zeros((h, w), dtype=np.uint8)

    # 读取YOLO标注文件
    with open(label_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        class_id, x_center, y_center, width, height = map(float, line.strip().split())
        # 将相对坐标转换为绝对坐标
        x_min = int((x_center - width / 2) * w)
        y_min = int((y_center - height / 2) * h)
        x_max = int((x_center + width / 2) * w)
        y_max = int((y_center + height / 2) * h)

        # 将此对象的区域设置为1（或类别索引）
        mask[y_min:y_max, x_min:x_max] = int(class_id) + 1  # +1 如果类别索引从1开始

    # 保存mask图像
    cv2.imwrite(output_path, mask)

label_root_dir = 'datasets/data/raw_labels'
img_root_dir = 'datasets/data/images'
output_root_dir = 'datasets/data/masks'

os.makedirs(output_root_dir, exist_ok=True)

# 遍历每个年份的子目录
for year in tqdm(['2014', '2017', '2018', '2020', '2021']):
    label_year_dir = os.path.join(label_root_dir, year)
    img_year_dir = os.path.join(img_root_dir, year)
    output_year_dir = os.path.join(output_root_dir, year)
    os.makedirs(output_year_dir, exist_ok=True)  # 创建输出子目录

    for file in tqdm(os.listdir(label_year_dir)):
        if file.endswith('.txt'):
            label_path = os.path.join(label_year_dir, file)
            img_path = os.path.join(img_year_dir, file.replace('.txt', '.tif'))  # 假设图像扩展名为.jpg
            output_path = os.path.join(output_year_dir, file.replace('.txt', '.tif'))
            convert_yolo_to_mask(label_path, img_path, output_path)
