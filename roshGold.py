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

# Define labels for the classification
object_labels = ["*Not Found*", "*Found Satchel*"]

# Load the pre-trained machine learning model
model_path = "path/to/saved_model"
model = tf.keras.models.load_model(model_path)

# Print summary of the loaded model
print("Loaded Machine Learning Model Summary:")
print(model.summary())

# List to store window handles and titles
window_list = []

class ScreenCapture:
    def __init__(self):
        # Define the area of the screen to capture
        capture_area = (620, 300, 950, 775)  # Format: (left, upper, right, lower)
        
        # Define the name of the window to capture
        window_name = 'Window Title Here'
        
        # Get list of specific window - windows[0][0] - is the window that was specified
        windows = self.find_windows(window_name)
        
        # Counter for image naming
        image_counter = 0
        
        # Print available windows
        print("Available Windows:")
        print(windows)
        
        # Main loop for capturing and analyzing screens
        while True:
            try:
                # Set the target window as the foreground window
                win32gui.SetForegroundWindow(windows[0][0])
                
                # Capture the screen within the defined area
                original_image = ImageGrab.grab(bbox=capture_area)
                
                # Preprocess the image for analysis
                grayscale_image = ImageOps.grayscale(original_image)
                resized_image = grayscale_image.resize((224, 224))
                input_image = img_to_array(resized_image).reshape(-1, 224, 224, 1)
                
                # Make a prediction using the machine learning model
                predictions = model.predict(input_image)
                confidence = 100 * np.max(tf.nn.softmax(predictions))
                predicted_label = object_labels[np.argmax(predictions)]
                
                # Print the prediction result
                print("Predicted Object:", predicted_label)
                print("Confidence:", confidence, "%")
                
                # Save the original image if a satchel is found
                if predicted_label == "*Found Satchel*":
                    original_image.save('path/to/save/satchel_images/%s.png' % image_counter)
                    time.sleep(3)  # Pause for 3 seconds to prevent rapid image saving
                
                # Increment the image counter
                image_counter += 1
            
            except pywintypes.error:
                print("Error: Wrong window selected or window closed.")
                break
            
            # Pause for 1 second before the next iteration
            time.sleep(1)
            
    def find_windows(self, window_name):
        # Function to find windows with the specified name
        win32gui.EnumWindows(self.enum_windows_callback, window_list)
        matching_windows = [(hwnd, title) for hwnd, title in window_list if window_name in title]
        while not matching_windows:
            win32gui.EnumWindows(self.enum_windows_callback, window_list)
            matching_windows = [(hwnd, title) for hwnd, title in window_list if window_name in title]
        return matching_windows

    def enum_windows_callback(self, hwnd, results):
        # Callback function to enumerate windows
        results.append((hwnd, win32gui.GetWindowText(hwnd)))

# Initialize the ScreenCapture class to start capturing screens
ScreenCapture()
