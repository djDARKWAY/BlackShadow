import subprocess
import re
import itertools
import threading
import time
import sys
import os

def loading_animation(stop_event):
    for char in itertools.cycle(["|", "/", "-", "\\"]):
        if stop_event.is_set():
            break
        sys.stdout.write(f"\rLoading system details... {char}")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\rSystem details loaded successfully ☑️   \n")
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')

def getDirectXVersion():
    try:
        # Start the loading animation in a separate thread
        stop_event = threading.Event()
        loader_thread = threading.Thread(target=loading_animation, args=(stop_event,))
        loader_thread.start()

        # Execute the command to get DirectX information
        subprocess.check_output("dxdiag /t dxdiag_output.txt", shell=True, text=True)
        
        with open("dxdiag_output.txt", "r") as file:
            dxdiag_data = file.read()

        match = re.search(r"DirectX Version:\s*(DirectX\s*\d+)", dxdiag_data)

        subprocess.run("del dxdiag_output.txt", shell=True)

        # Stop the loading animation
        stop_event.set()
        loader_thread.join()

        # Return the found DirectX version
        if match:
            return match.group(1).replace("DirectX ", "")
        else:
            return "Unknown"
    except Exception as e:
        return str(e)
