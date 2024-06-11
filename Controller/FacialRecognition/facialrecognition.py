import cv2
import face_recognition

# Load a sample picture and learn how to recognize it.
your_image = face_recognition.load_image_file("me.jpg")
your_face_encoding = face_recognition.face_encodings(your_image)[0]

known_face_encodings = [
    your_face_encoding
]
known_face_names = [
    "Jackson"
]

# I will want this to be the imported image from script
test_image = face_recognition.load_image_file("me3.jpg")

max_width = 800
max_height = 600

height, width = test_image.shape[:2]
if width > max_width or height > max_height:
    scaling_factor = min(max_width / width, max_height / height)
    test_image = cv2.resize(test_image, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

face_locations = face_recognition.face_locations(test_image)
face_encodings = face_recognition.face_encodings(test_image, face_locations)

face_names = []
for face_encoding in face_encodings:
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    name = "Unknown"

    if True in matches:
        first_match_index = matches.index(True)
        name = known_face_names[first_match_index]

    face_names.append(name)

test_image = cv2.cvtColor(test_image, cv2.COLOR_RGB2BGR)

# Display the results
for (top, right, bottom, left), name in zip(face_locations, face_names):
    cv2.rectangle(test_image, (left, top), (right, bottom), (0, 0, 255), 2)

    # Draw a label with a name below the face
    cv2.rectangle(test_image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(test_image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

cv2.imshow('Test Image', test_image)
cv2.waitKey(0)  # Wait until a key is pressed

# Close the display window
cv2.destroyAllWindows()
