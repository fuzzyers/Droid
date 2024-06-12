import cv2
import face_recognition
import sys
import json
import os

# Load a sample picture and learn how to recognize it.
def recognize_faces_and_positions(known_image_path, test_image_path):
    your_image = face_recognition.load_image_file("me.jpg")
    your_face_encoding = face_recognition.face_encodings(your_image)[0]
    
    known_face_encodings = [
        your_face_encoding
    ]
    known_face_names = [
        "Jackson"
    ]
    
    face_names = []
    face_positions = []
    results = []
    
    # I will want this to be the imported image from script
    test_image = face_recognition.load_image_file("captured_image.jpg")
    
    max_width = 800
    max_height = 600
    
    height, width = test_image.shape[:2]
    if width > max_width or height > max_height:
        scaling_factor = min(max_width / width, max_height / height)
        test_image = cv2.resize(test_image, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
    
    face_locations = face_recognition.face_locations(test_image)
    face_encodings = face_recognition.face_encodings(test_image, face_locations)
    
    face_names = []
    for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
    
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
    
        face_names.append(name)
        
        face_center_x = (left + right) / 2
        if face_center_x < width / 3:
            position = "left"
        elif face_center_x < 2 * width / 3:
            position = "center"
        else:
            position = "right"
        
        results.append({
            "name": name,
            "position": position
        })
    
    
    test_image = cv2.cvtColor(test_image, cv2.COLOR_RGB2BGR)
    
    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        cv2.rectangle(test_image, (left, top), (right, bottom), (0, 0, 255), 2)
    
        # Draw a label with a name below the face
        cv2.rectangle(test_image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(test_image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    
    cv2.imshow('Test Image', test_image)
    cv2.waitKey(0)

    cv2.destroyAllWindows()
    
    return results

results = recognize_faces_and_positions("me.jpg", "captured_image.jpg")

file_path = "controls.json"

if not os.path.exists(file_path):
    with open(file_path, "w") as json_file:
        json.dump([], json_file)  # Initialize with an empty list

with open(file_path, "w") as json_file:
    json.dump(results, json_file, indent=4)

for result in results:
    print(f"{result['name']} is in the {result['position']} of the screen.")

