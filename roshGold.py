import time
import numpy as np
import pyautogui
import win32gui
import pywintypes
import tensorflow as tf
from ctypes.wintypes import HWND
import PIL.ImageGrab as ImageGrab
from PIL import Image, ImageOps
from tensorflow.keras.utils import img_to_array 

# Labels for classification
y_labels = ["*Not Found*", "*Found Satchel*"]

# Load the trained model
model = tf.keras.models.load_model("path/to/saved_model")

# Print model summary
print(model.summary())

winlist = []

class ScreenCapture:
    def __init__(self):
        # Define bounding box for screen capture
        Bbox = (620, 300, 950, 775)  # Format: (left, upper, right, lower)
        
        # Name of the target window
        screen_name = 'ROSHTEIN - Twitch - Google Chrome'
        
        # Get list of available screens
        screens = self.get_screens(screen_name)
        
        # Counter for file naming
        i = 5330
        
        # Print available screens
        print(screens)
        
        # Print dimensions of the target window
        print(win32gui.GetWindowRect(screens[0][0]))
        
        # Main loop for screen capturing and prediction
        cont = True
        while cont:
            window = screens[0][0]
            img = None
            org_img = None
            try:
                win32gui.SetForegroundWindow(window)
                org_img = ImageGrab.grab(bbox=Bbox)
                
                # Preprocess image for model input
                img = ImageOps.grayscale(org_img)
                img = img.resize((224, 224))
                img = img_to_array(img) 
                img = img.reshape(-1, 224, 224, 1)
                
                # Make prediction
                predictions = model.predict(img)
                score = tf.nn.softmax(predictions)
                
                # Print prediction result
                print("This image most likely belongs to", y_labels[np.argmax(score)], "with a confidence of", 100 * np.max(score), "percent.")
                
                # Save image if satchel is found
                # (Or do whatever you need if the snachet is found)
                if y_labels[np.argmax(score)] == "*Found Satchel*":
                    org_img.save('path/to/save/false_positives/%s.png' % i)
                    time.sleep(3)
            except:
                print(window)
                print("There was an error... Wrong window selected")
            
            # Pause before next iteration
            time.sleep(1)
            i += 1
            
    def enter_text(self):
        # Function to enter text
        pyautogui.moveTo(1645, 965)
        pyautogui.click()
        pyautogui.write("roshGold", interval=0.1)
        pyautogui.press('enter')
    
    def get_screens(self, screen_name):
        # Function to get available screens
        win32gui.EnumWindows(enum_cb, winlist)
        screens = [(hwnd, title) for hwnd, title in winlist if screen_name in title]
        while len(screens) == 0:
            screens = [(hwnd, title) for hwnd, title in winlist if screen_name in title]
            win32gui.EnumWindows(enum_cb, winlist)

        return screens

def enum_cb(hwnd, results):
    # Callback function for enumerating windows
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
    
# Initialize ScreenCapture object
ScreenCapture()

