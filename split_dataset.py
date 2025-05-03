import os
import shutil
import random
from tqdm import tqdm

# Paths
dataset_dir = "C:/Users/Zaid Chikte/Downloads/archive"
img_dir = os.path.join(dataset_dir, 'images')
xml_dir = os.path.join(dataset_dir, 'annotations')
train_dir = os.path.join(dataset_dir, 'images/train')
val_dir = os.path.join(dataset_dir, 'images/val')
train_labels_dir = os.path.join(dataset_dir, 'labels/train')
val_labels_dir = os.path.join(dataset_dir, 'labels/val')

# Create directories if they don't exist
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)
os.makedirs(train_labels_dir, exist_ok=True)
os.makedirs(val_labels_dir, exist_ok=True)

# List all images (in this case, all images are in the 'images' folder)
all_images = [f for f in os.listdir(img_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]

# Shuffle images for random splitting
random.shuffle(all_images)

# Split dataset (80% train, 20% val)
split_idx = int(len(all_images) * 0.8)
train_images = all_images[:split_idx]
val_images = all_images[split_idx:]

# Move images and labels to their respective directories
for img in tqdm(train_images, desc="Moving train images and labels"):
    # Move image file
    shutil.move(os.path.join(img_dir, img), os.path.join(train_dir, img))
    
    # Move corresponding label file (if exists)
    label_file = os.path.splitext(img)[0] + '.txt'
    if os.path.exists(os.path.join(dataset_dir, 'labels', label_file)):
        shutil.move(os.path.join(dataset_dir, 'labels', label_file), os.path.join(train_labels_dir, label_file))

for img in tqdm(val_images, desc="Moving val images and labels"):
    # Move image file
    shutil.move(os.path.join(img_dir, img), os.path.join(val_dir, img))

    # Move corresponding label file (if exists)
    label_file = os.path.splitext(img)[0] + '.txt'
    if os.path.exists(os.path.join(dataset_dir, 'labels', label_file)):
        shutil.move(os.path.join(dataset_dir, 'labels', label_file), os.path.join(val_labels_dir, label_file))

print("✅ Dataset split into train and val successfully.")