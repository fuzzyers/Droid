import cv2
import subprocess
import serial
import time

# Constants
SERIAL_PORT = 'COM4'
BAUD_RATE = 9600
FACIAL_SCRIPT = "./facialDistancing.py"
OBJECT_DETECTION_SCRIPT = "./objectDetection.py"
PYTHON_INTERPRETER = "C:/Users/jacki/anaconda3/python"
DEPTH_SCRIPT = "./depthmeasuiring.py"
KNOWN_IMAGE_PATH = "me.jpg"
IMAGE_PATH = "./group.jpg"
MISSION = [{
    "PERSON": "Jackson",
    "PERSON_IMG": "me.jpg",
    "GOAL": "bottle",
    "GOAL_COMPLETED": False,
    "MISSION_COMPLETED": False
}]

# Initialize serial communication
found_twice = 0
i = 0

class StateMachine:
    def __init__(self):
        self.state = self.STATE_IDLE
        self.missions = MISSION
        self.last_known_position = None
        self.found_twice = 0
        self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
        time.sleep(2)

    def STATE_IDLE(self):
        print("State: Idle")
        
        # While missions exist
        if self.missions and not all(mission["MISSION_COMPLETED"] for mission in self.missions):
            self.transition_start()
        else:
            print("All missions completed.")
            self.stop()

    def STATE_TAKE_PHOTO(self):
        if self.take_photo():
            self.transition_process()
        else:
            self.STATE_IDLE()

    def STATE_PROCESS_PHOTO(self):
        if MISSION[0]["GOAL_COMPLETED"] == False:
            print("GOALY")
            self.process_photo_object()
        else:
            print("PERSON")
            found, position = self.process_photo()
            
            if position != None:
                self.last_known_position = position
                
            if found:
                if found_twice == 2:
                    self.transition_mission()
                else:
                    print(position, "Testing")
                    self.transition_move_towards()
            else:
                self.transition_search()
            

    def STATE_MOVE_TOWARDS(self):
        print("Moving Forward")
        self.ser.write(b'w')
        self.transition_take_photo()

    def STATE_MOVE_TOWARDS_LEFT(self):
        print("Strafing Left")
        self.ser.write(b'a')
        self.transition_take_photo()

    def STATE_MOVE_TOWARDS_RIGHT(self):
        print("Strafing Right")
        self.ser.write(b'd')
        self.transition_take_photo()
        
    def STATE_SEARCH(self):
        print("Searching...", self.last_known_position)
        
        if self.last_known_position == "left":
            self.ser.write(b'q')
            print("Turning: Left") #R2D2 Will rotate his head
            #Take Another photo then turn head back
        elif self.last_known_position == "right":
            self.ser.write(b'e')
            print("Turning: Right")
        elif self.last_known_position == "center":
            print("Send It forward")
            self.ser.write(b'w')
        else:
            print("Process Mapping")
            self.process_mapping()
            
        self.last_known_position = None
        self.transition_take_photo()

    def STATE_MISSION(self):
        print("Mission:")
        
        self.mission_task()
        self.STATE_IDLE()

    

    #Transitions
    def transition_start(self):
        self.state = self.STATE_TAKE_PHOTO
        self.state()

    def transition_process(self):
        self.state = self.STATE_PROCESS_PHOTO
        self.state()

    def transition_move_towards(self):
        print("lastknown", self.last_known_position)
        if self.last_known_position == "left":
            print("Moving: Left")
            self.state = self.STATE_MOVE_TOWARDS_LEFT
        elif self.last_known_position == "right":
            print("Moving: Right")
            self.state = self.STATE_MOVE_TOWARDS_RIGHT
        else:
            print("Moving: Straight Forward")
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


    #Helper Functions
    def take_photo(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open webcam.")
            return False
    
        ret, frame = cap.read()
        cap.release()
        cv2.destroyAllWindows()
    
        self.ser.write(b'r')
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

    def process_photo_object(self):
        try:
            IMAGE_PATH = "./bottle.jpg"
            result = subprocess.run([PYTHON_INTERPRETER, OBJECT_DETECTION_SCRIPT, IMAGE_PATH, "bottle"], check=True, capture_output=True, text=True)
            output = result.stdout.strip()
            last_word = output.split()[-1] if output.split() else None
            print(last_word)
            if last_word == MISSION[0]["GOAL"]:
                self.ser.write(b'u')
                MISSION[0]["GOAL_COMPLETED"] = True
                print(MISSION[0]["GOAL_COMPLETED"])
        except subprocess.CalledProcessError as e:
            print(f"Error during subprocess call: {e}")

    def process_mapping(self):
        try:
            result = subprocess.run([PYTHON_INTERPRETER, DEPTH_SCRIPT], check=True, capture_output=True, text=True)
            output = result.stdout.strip()
            print(output)
            if output == "forward":
                self.state = self.STATE_MOVE_TOWARDS
            elif output == "left":
                self.state = self.STATE_MOVE_TOWARDS_LEFT()
            elif output == "right":
                self.state = self.STATE_MOVE_TOWARDS_RIGHT()

            
        except subprocess.CalledProcessError as e:
            print(f"Error during subprocess call: {e}")   

    def mission_task(self):
        self.ser.write(b"o")
        MISSION[0]["MISSION_COMPLETED"] = True


    #Run Loop
    def run(self):
        while True:
            if not self.missions or all(mission["MISSION_COMPLETED"] for mission in self.missions):
                print("All missions completed. Exiting...")
                self.ser.close()
                break
            self.state()

    def stop(self):
        self.state = self.STATE_IDLE

machine = StateMachine()
machine.run()
