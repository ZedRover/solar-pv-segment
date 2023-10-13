import os
import shutil
import random
from tqdm import tqdm

# 指定原始目录和新目录
original_dir = '/dat/datasets'
new_dir = '/dat/new_datasets'

# 创建新目录结构
os.makedirs(new_dir, exist_ok=True)
os.makedirs(os.path.join(new_dir, 'images'), exist_ok=True)
os.makedirs(os.path.join(new_dir, 'labels'), exist_ok=True)

# 初始化正样本列表
positive_samples = []

# 遍历原始标签目录收集正样本
for year in range(2011, 2022):
    label_year_dir = os.path.join(original_dir, 'labels', str(year))
    if not os.path.exists(label_year_dir):
        continue  # 如果年份目录不存在，则跳过
    for label_file in os.listdir(label_year_dir):
        positive_samples.append((year, label_file))

# 确定需要选择的正样本数量，以达到正负样本比例为0.8
total_samples = len(positive_samples) / 0.8
negative_samples_count = int(total_samples - len(positive_samples))

# 从所有可用的正样本中随机选择一些样本
selected_positive_samples = random.sample(positive_samples, int(len(positive_samples)))

# 复制选定的正样本到新目录
for year, label_file in tqdm(selected_positive_samples, desc='Copying positive samples'):
    # 复制标签文件
    src_label_path = os.path.join(original_dir, 'labels', str(year), label_file)
    dst_label_path = os.path.join(new_dir, 'labels', label_file)
    shutil.copy(src_label_path, dst_label_path)
    
    # 复制图像文件
    image_file = label_file.replace('.txt', '.tif')
    src_image_path = os.path.join(original_dir, 'images', str(year), image_file)
    dst_image_path = os.path.join(new_dir, 'images', image_file)
    shutil.copy(src_image_path, dst_image_path)

# 找到没有对应标签的图像文件，即负样本
all_years = [str(year) for year in range(2011, 2022)]
all_images = [os.path.join(original_dir, 'images', str(year), image_file) 
              for year in all_years 
              for image_file in os.listdir(os.path.join(original_dir, 'images', str(year))) 
              if os.path.exists(os.path.join(original_dir, 'images', str(year)))]

all_labels = [os.path.join(original_dir, 'labels', str(year), label_file.replace('.tif', '.txt')) 
              for year, label_file in [(str(year), image_file) for image_file in os.listdir(os.path.join(new_dir, 'images'))]]

negative_samples = [image for image in all_images if image.replace('.tif', '.txt') not in all_labels]

# 从所有可用的负样本中随机选择一些样本
selected_negative_samples = random.sample(negative_samples, negative_samples_count)

# 复制选定的负样本到新目录
for src_image_path in tqdm(selected_negative_samples, desc='Copying negative samples'):
    dst_image_path = os.path.join(new_dir, 'images', os.path.basename(src_image_path))
    shutil.copy(src_image_path, dst_image_path)

print('Resampling completed!')
