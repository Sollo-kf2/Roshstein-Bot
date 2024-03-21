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

y_labels = ["*Not Found*", "*Found Satchel*"]
model = tf.keras.models.load_model("C:/Users/Pika/Desktop/Saved A.I")   
print(model.summary())

winlist = []
#hwnd = pywintypes.HANDLE()

class ScreenCapture:
    def __init__(self):
        Bbox = (620, 300, 950, 775) # Format : (left, upper, right, lower)
        
        screen_name = 'ROSHTEIN - Twitch - Google Chrome'
        screens = self.get_screens(screen_name)
        i = 5330
        print(screens)
        print(win32gui.GetWindowRect(screens[0][0]))
        cont = True
        while cont:
            window = screens[0][0]
            img = None
            org_img = None
            try:
                    win32gui.SetForegroundWindow(window)
                    org_img = ImageGrab.grab(bbox=Bbox)
                    if i < 5:
                        org_img.show()
                        org_img.save('C:/Users/Pika/Desktop/Additional Screenshots/%s.png' %i)
                    img = ImageOps.grayscale(org_img)
                    img = img.resize((224, 224))
                    img = img_to_array(img) 
                    img = img.reshape(-1,224,224,1)
                    predictions = model.predict(img)
                    score = tf.nn.softmax(predictions)
                    print("This image most likely belongs to ",y_labels[np.argmax(score)],  " with a ", 100 * np.max(score), " percent confidence.")
                    if y_labels[np.argmax(score)] == "*Found Satchel*":
                        #self.enter_text()
                        org_img.save('C:/Users/Pika/Desktop/Additional Screenshots/false_positives-%s.png' %i)
                        time.sleep(3)
            except:
                print(window)
                print("There was an error...Wrong Window selected")
            
            time.sleep(1)
            i += 1
            
    def enter_text(self):
      pyautogui.moveTo(1645, 965)
      pyautogui.click()
      pyautogui.write("roshGold", interval=0.1)
      pyautogui.press('enter')
      #pyautogui.write("roshSatchel", interval=0.1)
      #pyautogui.press('enter')
    
    def get_screens(self, screen_name):
        win32gui.EnumWindows(enum_cb, winlist)
        screens = [(hwnd, title) for hwnd, title in winlist if screen_name in title]
        while len(screens) == 0:
            screens = [(hwnd, title) for hwnd, title in winlist if screen_name in title]
            win32gui.EnumWindows(enum_cb, winlist)

        return screens

def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
    

ScreenCapture()
