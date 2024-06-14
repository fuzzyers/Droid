# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 00:29:16 2024

@author: jacki
"""

from transformers import pipeline
from helper import load_image_from_url, render_results_in_image
from transformers import pipeline
from transformers.utils import logging
from helper import ignore_warnings
from PIL import Image
import matplotlib.pyplot as plt

logging.set_verbosity_error()

clf = pipeline("image-classification", model="google/vit-base-patch16-224")
clf("./img1.jpg")

ignore_warnings()
od_pipe = pipeline("object-detection")

raw_image = Image.open('./me.jpg')

plt.imshow(raw_image)
plt.title("Raw Image")
plt.axis('off')
plt.show()

pipeline_output = od_pipe(raw_image)

processed_image = render_results_in_image(
    raw_image, 
    pipeline_output)

plt.imshow(processed_image)
plt.title("Processed Image")
plt.axis('off')
plt.show()

# Convert the processed image to RGB
rgb_image = processed_image.convert('RGB')

# Save the processed image as JPEG
rgb_image.save('processed_street.jpg')
