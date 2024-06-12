import cv2
import subprocess
from pyftdi.i2c import I2cController
from pyftdi.ftdi import Ftdi
import serial
import time
ser = serial.Serial('COM4', 9600)  # For Windows
time.sleep(2)  

facial_script = "./FacialRecognition/facialrecognition.py"
python_interpreter = "C:/Users/jacki/anaconda3/python"  #This uses the anaconda interpter as it has access to all my modules

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
    
 
# Function to read from the I2C slave
def read_i2c(address):
    ser.write(b'R')
    ser.write(bytes([address]))
    time.sleep(0.1)
    response = ser.read(1)
    return response

# Function to write to the I2C slave
def write_i2c(address, data):
    ser.write(b'W')
    ser.write(bytes([address]))
    ser.write(bytes([data]))
    time.sleep(0.1)
#def movement(direction):
    #If it sees person in facial recognition it will move towards them
    #If the depth mapping says the road is blocked it will take a detour then it will repeat photo
    
#write_i2c(0x04, ord('A'))  # Write 'A' to the I2C slave at address 0x04
#response = read_i2c(0x04)  # Read from the I2C slave at address 0x04
#print("Received:", response.decode('utf-8'))

takephoto()
processphoto()
ser.close()
