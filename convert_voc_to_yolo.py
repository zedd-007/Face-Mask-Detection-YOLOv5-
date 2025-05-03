import os
import xml.etree.ElementTree as ET
from tqdm import tqdm

# Your class names must match data.yaml
classes = ['with_mask', 'without_mask', 'mask_weared_incorrect']

# Paths
dataset_dir = "C:/Users/Zaid Chikte/Downloads/archive"
xml_dir = os.path.join(dataset_dir, 'annotations')
img_train_dir = os.path.join(dataset_dir, 'images/train')
img_val_dir = os.path.join(dataset_dir, 'images/val')
lbl_train_dir = os.path.join(dataset_dir, 'labels/train')
lbl_val_dir = os.path.join(dataset_dir, 'labels/val')

os.makedirs(lbl_train_dir, exist_ok=True)
os.makedirs(lbl_val_dir, exist_ok=True)

def convert(xml_file, img_folder, label_folder):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    img_filename = root.find('filename').text
    img_path = os.path.join(img_folder, img_filename)
    label_path = os.path.join(label_folder, os.path.splitext(img_filename)[0] + '.txt')

    size = root.find('size')
    img_w, img_h = int(size.find('width').text), int(size.find('height').text)

    with open(label_path, 'w') as f:
        for obj in root.findall('object'):
            cls = obj.find('name').text
            if cls not in classes:
                continue
            cls_id = classes.index(cls)

            bbox = obj.find('bndbox')
            xmin = int(bbox.find('xmin').text)
            ymin = int(bbox.find('ymin').text)
            xmax = int(bbox.find('xmax').text)
            ymax = int(bbox.find('ymax').text)

            # Convert to YOLO format
            x_center = ((xmin + xmax) / 2) / img_w
            y_center = ((ymin + ymax) / 2) / img_h
            width = (xmax - xmin) / img_w
            height = (ymax - ymin) / img_h

            f.write(f"{cls_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

# Split: e.g., 80% train, 20% val
all_xml = sorted(os.listdir(xml_dir))
split_idx = int(len(all_xml) * 0.8)
train_xml = all_xml[:split_idx]
val_xml = all_xml[split_idx:]

# Convert each
print("Converting training annotations...")
for xml in tqdm(train_xml):
    convert(os.path.join(xml_dir, xml), img_train_dir, lbl_train_dir)

print("Converting validation annotations...")
for xml in tqdm(val_xml):
    convert(os.path.join(xml_dir, xml), img_val_dir, lbl_val_dir)

print("✅ VOC to YOLO conversion complete.")