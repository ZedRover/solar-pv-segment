import cv2
import os
from tqdm import tqdm
import numpy as np

def draw_boxes(images_dir, labels_dir, output_dir):
    for year in tqdm(range(2011, 2022)):
        year_str = str(year)
        img_year_dir = os.path.join(images_dir, year_str)
        label_year_dir = os.path.join(labels_dir, year_str)
        output_year_dir = os.path.join(output_dir, year_str)
        os.makedirs(output_year_dir, exist_ok=True)
        
        for label_file in os.listdir(label_year_dir):
            if not label_file.endswith('.txt'):
                continue  # Skip non-txt files
            
            label_path = os.path.join(label_year_dir, label_file)
            img_path = os.path.join(img_year_dir, label_file.replace('.txt', '.tif'))
            output_path = os.path.join(output_year_dir, label_file.replace('.txt', '.tif'))
            
            if not os.path.exists(img_path):
                print(f"Image file not found: {img_path}")
                continue 
            
            img = cv2.imread(img_path, cv2.IMREAD_COLOR)
            if img is None:
                print(f"Failed to read image: {img_path}")
                continue
            
            h, w = img.shape[:2]
            
            with open(label_path, 'r') as file:
                lines = file.readlines()
            
            for line in lines:
                try:
                    coordinates = [float(coord) for coord in line.strip().split()[1:]]
                    xy_coordinates = [(int(coordinates[i] * w), int(coordinates[i + 1] * h)) for i in range(0, len(coordinates), 2)]
                except ValueError as e:
                    print(f"Failed to parse coordinates in {label_path}: {e}")
                    continue
                
                pts = np.array(xy_coordinates, np.int32)
                pts = pts.reshape((-1,1,2))
                cv2.polylines(img, [pts], isClosed=True, color=(0,0,255), thickness=2)
            
            if not cv2.imwrite(output_path, img):
                print(f"Failed to save image: {output_path}")

# Specify directories
original_dir = '/dat/datasets'
output_dir = '/dat/annotated_images'

# Call the function
images_dir = os.path.join(original_dir, 'images')
labels_dir = os.path.join(original_dir, 'labels')
draw_boxes(images_dir, labels_dir, output_dir)
