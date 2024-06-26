from transformers import pipeline
from helper import load_image_from_url, render_results_in_image
from transformers import pipeline
from transformers.utils import logging
from helper import ignore_warnings
from PIL import Image
import matplotlib.pyplot as plt

mission_label = "bottle"
logging.set_verbosity_error()

clf = pipeline("image-classification", model="google/vit-base-patch16-224")
clf("./img1.jpg")

ignore_warnings()
od_pipe = pipeline("object-detection")

raw_image = Image.open('./bottle.jpg')

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
rgb_image.save('processed.jpg')

label_found = False
for detected_object in pipeline_output:
    detected_label = detected_object['label']
    if detected_label == mission_label:
        label_found = True
        print(f"Label found: {detected_label}")
        break

if not label_found:
    print("Label not found for the given variable.")

