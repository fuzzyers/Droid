import cv2
import subprocess

facial_script = "./FacialRecognition/facialrecognition.py"
python_interpreter = "C:/Users/jacki/anaconda3/python"  # Replace with the correct path for your system

def takephoto():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return None

    # Capture a single frame
    ret, frame = cap.read()

    # Release the webcam
    cap.release()
    cv2.destroyAllWindows()

    if ret:
        return frame
    else:
        print("Error: Could not capture image.")
        return None


def processphoto():
    #Processes the photo with the depth map script and the facial recognition script
    try:
        subprocess.run([python_interpreter, facial_script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during subprocess call: {e}")
    
    
#def movement(direction):
    #If it sees person in facial recognition it will move towards them
    #If the depth mapping says the road is blocked it will take a detour then it will repeat photo
    
takephoto()
processphoto()