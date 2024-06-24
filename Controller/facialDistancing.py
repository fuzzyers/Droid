# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 17:37:37 2024

@author: jacki
"""

import cv2
import face_recognition
import json
import os
import torch
from transformers import pipeline
from PIL import Image
from transformers.utils import logging
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import sys

# Suppress warnings
logging.set_verbosity_error()

depth_estimator = pipeline(task="depth-estimation")

def recognize_faces_and_positions(known_image_path, test_image_path, known_face_encodings, known_face_names):
    MAX_WIDTH = 1920
    MAX_HEIGHT = 1080
    results = []
    
    test_image = face_recognition.load_image_file(test_image_path)
    
    
    # This will check the size of the img and resize it if necessary
    original_height, original_width = test_image.shape[:2]
    
    if original_width > MAX_WIDTH or original_height > MAX_HEIGHT:
        scaling_factor = min(MAX_WIDTH / original_width, MAX_HEIGHT / original_height)
        test_image = cv2.resize(test_image, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
    
    height, width = test_image.shape[:2]
    
    face_locations = face_recognition.face_locations(test_image)
    face_encodings = face_recognition.face_encodings(test_image, face_locations)
    
    for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
    
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
    
        face_center_x = (left + right) / 2
        if face_center_x < width / 3:
            position = "left"
        elif face_center_x < 2 * width / 3:
            position = "center"
        else:
            position = "right"
        
        results.append({
            "name": name,
            "position": position,
            "bounding_box": (top, right, bottom, left)
        })
    
    test_image = cv2.cvtColor(test_image, cv2.COLOR_RGB2BGR)
    
    # For use in testing.
    for (top, right, bottom, left), name in zip(face_locations, [result['name'] for result in results]):
        cv2.rectangle(test_image, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(test_image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(test_image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    cv2.imshow('Test Image', test_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return results, test_image

def estimate_depth(image_path, face_positions):
    raw_image = Image.open(image_path)
    raw_image = raw_image.convert('RGB')

    # Get depth estimation
    output = depth_estimator(raw_image)

    # Interpolate depth to match the original image size
    prediction = torch.nn.functional.interpolate(
        output["predicted_depth"].unsqueeze(1),
        size=raw_image.size[::-1],
        mode="bicubic",
        align_corners=False,
    )

    # Convert to numpy array
    output = prediction.squeeze().numpy()
    formatted = (output * 255 / np.max(output)).astype("uint8")
    depth = Image.fromarray(formatted)

    # Depth values for analysis
    depth_values = output

    min_depth = np.min(depth_values)
    max_depth = np.max(depth_values)
    print(f"Minimum depth (closer objects): {min_depth}")
    print(f"Maximum depth (farther objects): {max_depth}")

    # Distancing numbers change to get desired result
    depth_min_meters = 0.5  
    depth_max_meters = 2.0  

    for position in face_positions:
        top, right, bottom, left = position['bounding_box']
        face_depth_region = depth_values[top:bottom, left:right]
        mean_face_depth = np.mean(face_depth_region)

        estimated_distance = depth_min_meters + (depth_max_meters - depth_min_meters) * ((mean_face_depth - min_depth) / (max_depth - min_depth))

        if mean_face_depth < (min_depth + max_depth) / 2:
            proximity = "close"
        else:
            proximity = "far away"
        
        position['proximity'] = proximity
        position['estimated_distance_meters'] = estimated_distance
        
        print(f"{position['name']} is {proximity} and approximately {estimated_distance:.2f} meters away.")
        return proximity

# Recognize faces and get their positions




if __name__ == "__main__":
    # Command line arguments for known and test image paths
    KNOWN_FACE_NAMES = [sys.argv[1]]
    KNOWN_FACE_PATH = sys.argv[2]
    TEST_IMAGE_PATH = sys.argv[3]
    TEST_IMAGE_PATH = "./me.jpg"
    
    known_image = face_recognition.load_image_file(KNOWN_FACE_PATH)
    known_face_encoding = face_recognition.face_encodings(known_image)[0]
    KNOWN_FACE_ENCODINGS = [known_face_encoding]
        
    face_positions, _ = recognize_faces_and_positions(KNOWN_FACE_PATH, TEST_IMAGE_PATH, KNOWN_FACE_ENCODINGS, KNOWN_FACE_NAMES)
    depth = estimate_depth(TEST_IMAGE_PATH, face_positions)
    print(depth)
    for result in face_positions:
        if result["name"] in KNOWN_FACE_NAMES:
            print(f"{result['name']} is in the {result['position']}")



