import torch
from transformers import pipeline
from PIL import Image
from transformers.utils import logging
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

logging.set_verbosity_error()

depth_estimator = pipeline(task="depth-estimation")

raw_image = Image.open('./group.jpg')
raw_image = raw_image.convert('RGB')

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

output = prediction.squeeze().numpy()
formatted = (output * 255 / np.max(output)).astype("uint8")
depth = Image.fromarray(formatted)

# Display depth map
plt.imshow(depth, cmap='gray')
plt.title("Depth Map")
plt.axis('off')
plt.show()

depth.save('depth_map.png')

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

def determine_movement_direction(depth_values, threshold):
    """
    Determines the best direction for the robot to move based on depth values.

    Parameters:
    - depth_values (numpy array): The depth values from the depth estimation.
    - threshold (float): The depth threshold for deciding if an object is close.

    Returns:
    - str: The direction the robot should move ("forward", "left", "right").
    """
    # Define regions of interest
    height, width = depth_values.shape
    center_region = depth_values[:, width//3:2*width//3]
    left_region = depth_values[:, :width//3]
    right_region = depth_values[:, 2*width//3:]

    # Calculate the mean depth in each region
    mean_center_depth = np.mean(center_region)
    mean_left_depth = np.mean(left_region)
    mean_right_depth = np.mean(right_region)

    # Decision logic
    if mean_center_depth > threshold:
        return "forward"
    elif mean_left_depth > threshold and mean_right_depth < threshold:
        return "left"
    elif mean_right_depth > threshold and mean_left_depth < threshold:
        return "right"
    else:
        #If we see no desirable way to go we can turn 
        return "turn left"


if __name__ == "__main__":
    direction = determine_movement_direction(depth_values, threshold)
    print(f"Recommended direction for the robot: {direction}")
