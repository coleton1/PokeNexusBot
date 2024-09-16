import pyautogui
import cv2
import time
import numpy as np
from pynput.keyboard import Controller as KeyboardController

# Load the reference image(s)
image_paths = ['fight.png', 'shadow.png', 'battle.png','hyper.png','bug.png','crunch.png']  # Paths to your target images here
images = []

# Load all images
for image_path in image_paths:
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not load {image_path}")
    else:
        images.append((image_path, image))  # Store both the image path and the image itself
        print(f"{image_path} loaded successfully.")

def find_image_on_screen(image):
    # Take a screenshot of the current screen
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)

    # Convert both screenshot and image to grayscale
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use OpenCV to search for the image within the screenshot
    result = cv2.matchTemplate(screenshot, image_gray, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # Adjust as needed for accuracy
    loc = np.where(result >= threshold)

    if len(loc[0]) > 0:
        # Get the coordinates of the match
        pt = loc[::-1]  # Reverse the array to get (x, y)
        return pt[0][0], pt[1][0]  # x, y
    return None

def walking():
    keyboard = KeyboardController()
    keyboard.press('a')
    time.sleep(1)
    keyboard.release('a')
    keyboard.press('d')
    time.sleep(1)
    keyboard.release('d')

def click_i():
    keyboard = KeyboardController()
    keyboard.press('i')
    keyboard.release('i')
    time.sleep(2)
    hyper_image = next((img for path, img in images if path == 'hyper.png'), None)
    if hyper_image is not None:
        hyper_position = find_image_on_screen(hyper_image)
        if hyper_position:
            print("I see the potion!")
            x, y = hyper_position

            # Debugging: Print the coordinates
            print(f"Potion coordinates: x={x}, y={y}")

            # Calculate the click position
            potion_x = x + hyper_image.shape[1] // 2
            potion_y = y + hyper_image.shape[0] // 2

            # Debugging: Print the adjusted click coordinates
            print(f"Clicking at: x={potion_x}, y={potion_y}")

            # Move to the potion and click
            pyautogui.moveTo(potion_x, potion_y, duration=0.2)  # Smooth movement
            time.sleep(3)
            real_x = potion_x + 50
            real_y = potion_y
            pokemon1_x = 455
            pokemon1_y = 195 
            print("clicking")
            pyautogui.click(real_x,real_y)
            time.sleep(2)
            print("clicked!")
            time.sleep(2)
            pyautogui.moveTo(pokemon1_x,pokemon1_y)
            time.sleep(1)
            pyautogui.click(pokemon1_x,pokemon1_y)

            #sometimes it will run this function when in battle so this prevents it from getting stuck in potion menu
            bug = next((img for path, img in images if path == 'bug.png'), None)
            if bug is not None:
                bug_is_there = find_image_on_screen(bug)
                if bug_is_there:
                    pyautogui.click([pokemon1_x,pokemon1_y])

            
             # Exit the function after clicking the potion
        else:
            print("Potion not found.")
    else:
        print("No potion image loaded.")
            
    time.sleep(1.5)
    keyboard.press('i')
    keyboard.release('i')

def click_image(image, image_path):
    # Find the image on the screen
    position = find_image_on_screen(image)
    if position:
        # Move the mouse to the position and click
        x, y = position
        pyautogui.moveTo(x + image.shape[1] // 2, y + image.shape[0] // 2)
        pyautogui.click()
        print(x + image.shape[1] // 2, y + image.shape[0] // 2)

        # Move the mouse back to the center of the screen
        screen_width, screen_height = pyautogui.size()
        pyautogui.moveTo(screen_width // 2, screen_height // 2)

# Initialize variables
walking_enabled = True
menu_open = False  # Track if the 'i' menu is open
last_i_press_time = time.time()  # Track the time for 'i' press

# Continuously search for the images and click if found
while True:
    battle_detected = False

    # Check for battle images
    for image_path, image in images:
        if find_image_on_screen(image):
            if image_path == 'battle.png':
                # If battle.png is detected, set battle_detected to True
                battle_detected = True
                print("it has indeed seen that its in a battle!")
                break
            else:
                # If not battle.png but fight.png or shadow.png, it means we are in a battle state
                battle_detected = True
                click_image(image, image_path)
                print("it has no fucking idea that its in a battle ")
                break  # Exit the loop if any battle image is found

    if not battle_detected:
        if walking_enabled:
            walking()

        # Check if it's time to press 'i'
        current_time = time.time()
        if current_time - last_i_press_time >= 15:  # 60 seconds passed
            if not menu_open:  # If menu is closed, open it
                click_i()
                menu_open = True
            else:  # If menu is open, close it
                click_i()
                menu_open = False

            last_i_press_time = current_time  # Update last press time

    time.sleep(1)  # Adjust the delay to suit your needs (1 second in this case)

