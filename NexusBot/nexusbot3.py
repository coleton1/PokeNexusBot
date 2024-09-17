import pyautogui
import cv2
import time
import numpy as np
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import KeyCode
import customtkinter as ctk
import threading

# Variables for bot control
bot_running = False
bot_thread = None
last_i_press_time = time.time()
menu_open = False

# Load images
image_paths = ['fight.png', 'battle.png', 'hyper.png', 'bug.png','haunter.png']  # Images to be loaded
images = []  # List to store loaded images

for image_path in image_paths:
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not load {image_path}")
    else:
        images.append((image_path, image))
        print(f"{image_path} loaded successfully.")

# Function to find image on the screen
def find_image_on_screen(image):
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screenshot, image_gray, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(result >= threshold)

    if len(loc[0]) > 0:
        pt = loc[::-1]  # Reverse to get (x, y)
        return pt[0][0], pt[1][0]  # Return x, y
    return None

# Function to simulate walking in-game
def walking():
    keyboard = KeyboardController()
    keyboard.press('a')
    time.sleep(1)
    keyboard.release('a')
    keyboard.press('d')
    time.sleep(1)
    keyboard.release('d')
    time.sleep(2)

def hyper_potion_on_off():
    # Check the state of the CTkSwitch widget, not the function
    if hyper_potion_mode.get():
        hyper_potion_label.configure(text="On",font=("Arial", 14, "bold"))
    else:
        hyper_potion_label.configure(text="Off",font=("Arial", 14, "bold"))

def walking_mode_on_off():
    if walking_mode_switch.get():
        walking_mode_label.configure(text="On",fg_color="green",font=("Arial", 14, "bold"))
    else:
        walking_mode_label.configure(text="Off",font=("Arial", 14, "bold"))

def walking_up_and_down():
    keyboard = KeyboardController()
    keyboard.press('w')
    time.sleep(1)
    keyboard.release('w')
    keyboard.press('s')
    time.sleep(1)
    keyboard.release('s')
    time.sleep(2)

# Function to press 'i' and use a potion
def click_i():
    keyboard = KeyboardController()
    keyboard.press('i')
    keyboard.release('i')
    time.sleep(1)
    hyper_image = next((img for path, img in images if path == 'hyper.png'), None)
    if hyper_image is not None:
        hyper_position = find_image_on_screen(hyper_image)
        if hyper_position:
            print("Potion found!")
            x, y = hyper_position
            pyautogui.moveTo(x + hyper_image.shape[1] // 2, y + hyper_image.shape[0] // 2)
            potion_x = x + hyper_image.shape[1] // 2
            potion_y = y + hyper_image.shape[0] // 2
            real_x = potion_x + 50
            real_y = potion_y
            pyautogui.click(real_x,real_y)
            time.sleep(1)
            pokemon1_x = 455
            pokemon1_y = 100
            pyautogui.moveTo(pokemon1_x, pokemon1_y)
            pyautogui.click()
            keyboard.press('i')
            keyboard.release('i')

# Function to click images like 'fight.png'
def click_image(image, image_path):
    position = find_image_on_screen(image)
    if position:
        x, y = position
        pyautogui.moveTo(x + image.shape[1] // 2, y + image.shape[0] // 2)
        pyautogui.click()

        if image_path == 'fight.png':
            time.sleep(1)
            pyautogui.moveTo(x + image.shape[1] // 2, y + image.shape[0] // 2)
            pyautogui.click()

        screen_width, screen_height = pyautogui.size()
        pyautogui.moveTo(screen_width // 2, screen_height // 2)

# Function to start/stop the bot
def toggle_bot():
    global bot_running, bot_thread

    if bot_running:
        bot_running = False
        if start_button is not None:
            start_button.configure(text="Start Bot")
        print("Bot stopped.")
    else:
        bot_running = True
        bot_thread = threading.Thread(target=run_bot)
        bot_thread.start()
        if start_button is not None:
            start_button.configure(text="Stop Bot")
        print("Bot started.")


# Bot's main loop
def run_bot():
    global bot_running, last_i_press_time, menu_open

    time.sleep(3)  # Allow user time to switch to the game window
    while bot_running:
        battle_detected = False

        # Check for battle images
        for image_path, image in images:
            if find_image_on_screen(image):
                if image_path == 'battle.png':
                    battle_detected = True
                    print("Battle detected!")
                    break
                elif image_path == 'fight.png':
                    battle_detected = True
                    click_image(image, image_path)
                    print("Fight action triggered")
                    break
                    #DOESNT SEE HAUNTER IMAGE FIXXXXXXXXXXXXXXX!!!
                elif image_path == 'haunter.png':
                    x, y = find_image_on_screen(image)
                    if x is not None and y is not None:
                        print("Seen haunter!")
                    else:
                        print("No haunter found")
                    break

        if not battle_detected:
            if walking_mode_switch is not None and walking_mode_switch.get():
                walking_up_and_down()
            else:
                walking()

        # Check if it's time to press 'i'
        if not battle_detected:
            if hyper_potion_mode is not None and hyper_potion_mode.get():
                current_time = time.time()
                if current_time - last_i_press_time >= 200:
                    if not menu_open:
                        click_i()
                        menu_open = True
                    else:
                        click_i()
                        menu_open = False
                    last_i_press_time = current_time

        time.sleep(1)  # Adjust delay if needed


# GUI function
def gui():
    global start_button, walking_mode_switch, hyper_potion_mode,hyper_potion_label,walking_mode_label

    root = ctk.CTk()
    root.geometry("500x500")
    ctk.set_appearance_mode("dark")
    #ctk.set_default_color_theme("")

    ctk.CTkLabel(root, text="NexusBot Control Panel", font=("Roboto", 26, "bold")).pack(pady=20)


    walking_mode_switch = ctk.CTkSwitch(root, text="Walking Up/Down     ", font=("Arial", 12, "bold"), fg_color="#FFBF00",command=walking_mode_on_off)
    walking_mode_switch.pack(pady=5)
    walking_mode_label= ctk.CTkLabel(root, text="Off", font=("Arial", 14, "bold"))
    walking_mode_label.place(y=75, x=140)

    hyper_potion_mode = ctk.CTkSwitch(root, text="Hyper Potion Check", font=("Arial", 12, "bold"), fg_color="#FFBF00",command=hyper_potion_on_off)
    hyper_potion_mode.pack(pady=5)
    hyper_potion_label = ctk.CTkLabel(root, text="Off", font=("Arial", 14, "bold"))
    hyper_potion_label.place(y=108,x=140)

    start_button = ctk.CTkButton(root, text="Start Bot", font=("Arial", 14, "bold"), command=toggle_bot, fg_color="#FFBF00")
    start_button.pack(pady=5)

    root.mainloop()


# Call the GUI function to start the interface
gui()
