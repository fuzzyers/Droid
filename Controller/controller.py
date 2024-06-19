import cv2
import subprocess
import serial
import time

# Constants
SERIAL_PORT = 'COM5'
BAUD_RATE = 9600
FACIAL_SCRIPT = "./facialDistancing.py"
PYTHON_INTERPRETER = "C:/Users/jacki/anaconda3/python"
KNOWN_IMAGE_PATH = "me.jpg"
IMAGE_PATH = "./group.jpg"
MISSION = [{
    "PERSON": "Jackson",
    "PERSON_IMG": "me.jpg",
    "GOAL": "FIND"
}]

# States
STATE_IDLE = 'IDLE'
STATE_TAKE_PHOTO = 'TAKE_PHOTO'
STATE_PROCESS_PHOTO = 'PROCESS_PHOTO'
STATE_MOVE_TOWARDS = 'MOVE_TOWARDS'
STATE_MOVE_TOWARDS_RIGHT = "MOVE_TOWARDS_RIGHT"
STATE_MOVE_TOWARDS_LEFT = "MOVE_TOWARDS_LEFT"
STATE_MISSION = 'MISSION'
STATE_SEARCH = 'SEARCH'

# Initialize serial communication
# ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)
last_known_position = ""
found_twice = 0

def move_forward():
    # ser.write(b'F')
    # print("Sent 'F' to the Arduino")
    time.sleep(0.1)
    # while ser.in_waiting > 0:
    #     response = ser.readline().decode('utf-8').strip()
    #     print("Arduino responded:", response)

class StateMachine:
    def __init__(self):
        self.state = self.STATE_IDLE
        self.missions = [MISSION]  # Example missions list
        self.last_known_position = None

    def STATE_IDLE(self):
        print("State: Idle")
        
        # While missions exist
        if self.missions:
            self.transition_start()
        else:
            print("No missions left.")

    def STATE_TAKE_PHOTO(self):
        if self.take_photo():
            self.transition_process()
        else:
            self.STATE_IDLE()

    def STATE_PROCESS_PHOTO(self):
        found, position = self.process_photo()
        self.last_known_position = position
        if found:
            if found_twice == 2:
                self.transition_mission()
            else:
                self.transition_move_towards()
        else:
            self.transition_search()

    def STATE_MOVE_TOWARDS(self):
        move_forward()
        self.transition_take_photo()

    def STATE_SEARCH(self):
        # Implement your search logic here
        print("Searching...")
        self.transition_take_photo()

    def STATE_MISSION(self):
        self.mission_task()
        self.STATE_IDLE()

    def transition_start(self):
        self.state = self.STATE_TAKE_PHOTO
        self.state()

    def transition_process(self):
        self.state = self.STATE_PROCESS_PHOTO
        self.state()

    def transition_move_towards(self):
        if self.last_known_position == "left":
            self.state = self.STATE_MOVE_TOWARDS_LEFT
        elif self.last_known_position == "right":
            self.state = self.STATE_MOVE_TOWARDS_RIGHT
        else:
            self.state = self.STATE_MOVE_TOWARDS
        self.state()

    def transition_take_photo(self):
        self.state = self.STATE_TAKE_PHOTO
        self.state()

    def transition_search(self):
        self.state = self.STATE_SEARCH
        self.state()

    def transition_mission(self):
        self.state = self.STATE_MISSION
        self.state()

    def take_photo(self):
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

    def process_photo(self):
        global found_twice
        try:
            result = subprocess.run([PYTHON_INTERPRETER, FACIAL_SCRIPT, MISSION[0]["PERSON"], MISSION[0]["PERSON_IMG"], IMAGE_PATH], check=True, capture_output=True, text=True)
            output = result.stdout.strip()
            print(output)
            if MISSION[0]["PERSON"] in output:
                found_twice += 1
                for line in output.splitlines():
                    if MISSION[0]["PERSON"] in line:
                        position = line.split()[-1]  # Will take the last word which is set for the location on screen
                        return True, position
            else:
                if found_twice != 0:
                    found_twice -= 1
            return False, None
        except subprocess.CalledProcessError as e:
            print(f"Error during subprocess call: {e}")
            return False, None

    def mission_task(self):
        # Example mission task: Turn 90 degrees and project if Jackson is close
        pass

    def run(self):
        while True:
            self.state()

# Example usage
machine = StateMachine()
machine.run()
