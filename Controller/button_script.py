import serial
import subprocess

PYTHON_INTERPRETER = "C:/Users/jacki/anaconda3/python"
CONTROLLER_SCRIPT = "./controller.py"
ser = serial.Serial('COM4', 9600, timeout=1)

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        if line == "RUN_SCRIPT":
            ser.close()
            try:
                result = subprocess.run(
                    [PYTHON_INTERPRETER, CONTROLLER_SCRIPT],
                    check=True,
                    capture_output=True,
                    text=True
                )
                print("Script output:", result.stdout)
                print("Script errors:", result.stderr)
            except subprocess.CalledProcessError as e:
                print("Error running script:", e)
                print("Script output:", e.stdout)
                print("Script errors:", e.stderr)

            print("TEST")
            
