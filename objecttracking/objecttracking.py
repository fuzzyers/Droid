import cv2
import numpy as np

# Load YOLO weights and configuration
yolo_net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
# Load YOLO classes
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Open the default camera (usually the built-in webcam)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open the camera.")
    exit()

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read a frame.")
        break

    # Get the blob from the frame and set it as the input to the YOLO network
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    yolo_net.setInput(blob)

    # Get the output layer names
    layer_names = yolo_net.getUnconnectedOutLayersNames()

    # Run forward pass
    outputs = yolo_net.forward(layer_names)

    class_ids = []
    confidences = []
    boxes = []

    # Post-process the outputs
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x, center_y, width, height = map(int, detection[0:4] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]]))
                x = int(center_x - width / 2)
                y = int(center_y - height / 2)
                boxes.append([x, y, width, height])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            color = (0, 255, 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, f"{label} {confidence:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Display the frame with object detection
    cv2.imshow("Object Detection", frame)

    # Press 'q' to exit the loop and close the window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
