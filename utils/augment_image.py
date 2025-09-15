import os
import cv2
import numpy as np
from PIL import Image
import imgaug.augmenters as iaa

input_image_path = "tumbler.jpg"

output_dir = "data/personal/bottle"  
os.makedirs(output_dir, exist_ok=True)

image = np.array(Image.open(input_image_path))

augmenter = iaa.Sequential([
    iaa.Fliplr(0.5),
    iaa.Affine(rotate=(-15, 15)),
    iaa.Multiply((0.9, 1.1)),
    iaa.GaussianBlur(sigma=(0.0, 0.5)),
], random_order=True)

for i in range(5):
    aug_img = augmenter(image=image)
    out_path = os.path.join(output_dir, f"tumbler_aug_{i+1}.jpg")
    cv2.imwrite(out_path, cv2.cvtColor(aug_img, cv2.COLOR_RGB2BGR))
    print(f"Saved: {out_path}")
