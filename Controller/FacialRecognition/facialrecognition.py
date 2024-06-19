import cv2
import face_recognition
import json
import os
import sys

def recognize_faces_and_positions(known_image_path, test_image_path):
    your_image = face_recognition.load_image_file(known_image_path)
    your_face_encoding = face_recognition.face_encodings(your_image)[0]
    
    known_face_encodings = [your_face_encoding]
    known_face_names = ["Jackson"]
    
    results = []
    
    test_image = face_recognition.load_image_file(test_image_path)
    
    max_width = 800
    max_height = 600
    
    # Resize image if necessary
    original_height, original_width = test_image.shape[:2]
    if original_width > max_width or original_height > max_height:
        scaling_factor = min(max_width / original_width, max_height / original_height)
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
    
    #test_image = cv2.cvtColor(test_image, cv2.COLOR_RGB2BGR)
    
    # Display the results
    #for (top, right, bottom, left), name in zip(face_locations, [result['name'] for result in results]):
     #   cv2.rectangle(test_image, (left, top), (right, bottom), (0, 0, 255), 2)
      #  cv2.rectangle(test_image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
       # font = cv2.FONT_HERSHEY_DUPLEX
       # cv2.putText(test_image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    
   # cv2.imshow('Test Image', test_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return results

if __name__ == "__main__":
    # Command line arguments for known and test image paths
    known_image_path = sys.argv[1]
    test_image_path = sys.argv[2]

    results = recognize_faces_and_positions(known_image_path, test_image_path)

    # Process the results and save to a JSON file

    for result in results:
        print(f"{result['name']} is in the {result['position']}")
