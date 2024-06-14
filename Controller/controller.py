import cv2
import subprocess
from pyftdi.i2c import I2cController
from pyftdi.ftdi import Ftdi
import serial
import time

ser = serial.Serial('COM5', 9600)
time.sleep(2)  

facial_script = "./FacialRecognition/facialrecognition.py"
python_interpreter = "C:/Users/jacki/anaconda3/python"  #This uses the anaconda interpter as it has access to all my modules
mission = "Jackson"
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
        image_path = "./captured_image.jpg"
        cv2.imwrite(image_path, frame)
        print(f"Image saved as {image_path}")

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
    
 
def mission():
    #if Jackson is Close turn 90deg then project.
    
#def movement(direction):
    #If it sees person in facial recognition it will move towards them
    #If the depth mapping says the road is blocked it will take a detour then it will repeat photo
    

#takephoto()
#processphoto()

ser.write(b'F')  # Send character 'F' f is for forwards
print("Sent 'F' to the Arduino")

time.sleep(0.1)  
while ser.in_waiting > 0:
    response = ser.readline().decode('utf-8').strip()
    print("Arduino responded:", response)

ser.close()
