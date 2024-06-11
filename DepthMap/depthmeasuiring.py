# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 15:50:23 2024

@author: jacki
"""

import torch
from transformers import pipeline
from PIL import Image
from transformers.utils import logging
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

logging.set_verbosity_error()

# Depth Estimation Pipeline
depth_estimator = pipeline(task="depth-estimation")

# Load and display raw image
raw_image = Image.open('./me.jpg')
raw_image = raw_image.convert('RGB')  # Ensure it's in RGB mode

plt.imshow(raw_image)
plt.title("Raw Image")
plt.axis('off')
plt.show()

# Get depth estimation
output = depth_estimator(raw_image)

# Interpolate depth to match the original image size
prediction = torch.nn.functional.interpolate(
    output["predicted_depth"].unsqueeze(1),
    size=raw_image.size[::-1],
    mode="bicubic",
    align_corners=False,
)

# Convert to numpy array and normalize
output = prediction.squeeze().numpy()
formatted = (output * 255 / np.max(output)).astype("uint8")
depth = Image.fromarray(formatted)

# Display depth map
plt.imshow(depth, cmap='gray')
plt.title("Depth Map")
plt.axis('off')
plt.show()

# Save depth map
depth.save('depth_map.png')

# Depth values for analysis
depth_values = output

min_depth = np.min(depth_values)
max_depth = np.max(depth_values)
print(f"Minimum depth (closer objects): {min_depth}")
print(f"Maximum depth (farther objects): {max_depth}")

# Threshold to identify close regions
threshold = (max_depth - min_depth) / 2
close_regions = depth_values < threshold

plt.imshow(close_regions, cmap='gray')
plt.title("Close Regions")
plt.axis('off')
plt.show()

# Find contours of close regions using ndimage
labeled, num_features = ndimage.label(close_regions)
slices = ndimage.find_objects(labeled)

# Draw bounding boxes around contours using Matplotlib
fig, ax = plt.subplots()
ax.imshow(raw_image)

for slice_ in slices:
    y, x = slice_
    rect = plt.Rectangle((x.start, y.start), x.stop - x.start, y.stop - y.start, 
                         edgecolor='red', facecolor='none', linewidth=2)
    ax.add_patch(rect)

plt.title("Detected Close Objects")
plt.axis('off')
plt.show()
