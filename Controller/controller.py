import cv2
import subprocess
import serial
import time

# Constants
SERIAL_PORT = 'COM5'
BAUD_RATE = 9600
FACIAL_SCRIPT = "./FacialRecognition/facialrecognition.py"
PYTHON_INTERPRETER = "C:/Users/jacki/anaconda3/python"
KNOWN_IMAGE_PATH = "me.jpg"
IMAGE_PATH = "./me3.jpg"
MISSION = "Jackson"

# States
STATE_IDLE = 'IDLE'
STATE_TAKE_PHOTO = 'TAKE_PHOTO'
STATE_PROCESS_PHOTO = 'PROCESS_PHOTO'
STATE_MOVE_TOWARDS = 'MOVE_TOWARDS'
STATE_MISSION = 'MISSION'
STATE_SEARCH = 'SEARCH'

# Initialize serial communication
#ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)
mission_location = ""

# Helper functions
def take_photo():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return False

    ret, frame = cap.read()
    cap.release()
    cv2.destroyAllWindows()

    if ret:
        cv2.imwrite(IMAGE_PATH, frame)
        print(f"Image saved as {IMAGE_PATH}")
        return True
    else:
        print("Error: Could not capture image.")
        return False

def process_photo():
    try:
        result = subprocess.run([PYTHON_INTERPRETER, FACIAL_SCRIPT, KNOWN_IMAGE_PATH, IMAGE_PATH], check=True, capture_output=True, text=True)
        output = result.stdout.strip()
        print(output)
        if MISSION in output:
            
            return True
        else:
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error during subprocess call: {e}")
        return False

def move_forward():
    #ser.write(b'F')
    #print("Sent 'F' to the Arduino")
    time.sleep(0.1)
    #while ser.in_waiting > 0:
     #   response = ser.readline().decode('utf-8').strip()
      #  print("Arduino responded:", response)

def search():
    # Search behavior, for example, turning to find Jackson
    #ser.write(b'S')
    #print("Sent 'S' to the Arduino to search")
    time.sleep(0.1)
    #while ser.in_waiting > 0:
     #   response = ser.readline().decode('utf-8').strip()
      #  print("Arduino responded:", response)

def mission_task():
    # Example mission task: Turn 90 degrees and project if Jackson is close
    pass

# Main state machine loop
state = STATE_IDLE

while True:
    if state == STATE_IDLE:
        # Perform idle actions
        state = STATE_TAKE_PHOTO

    elif state == STATE_TAKE_PHOTO:
        if take_photo():
            state = STATE_PROCESS_PHOTO
    elif state == STATE_PROCESS_PHOTO:
        if process_photo():
            
            
            
            state = STATE_MOVE_TOWARDS
        else:
            state = STATE_SEARCH

    elif state == STATE_MOVE_TOWARDS:
        move_forward()
        state = STATE_MISSION

    elif state == STATE_SEARCH:
        search()
        state = STATE_TAKE_PHOTO

    elif state == STATE_MISSION:
        mission_task()
        state = STATE_IDLE

    else:
        print("Unknown state!")
        state = STATE_IDLE

#ser.close()
