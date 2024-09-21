import pyautogui
import cv2
import time
import numpy as np
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import KeyCode
import customtkinter as ctk
import threading
from PIL import Image, ImageTk

# Variables for bot control
bot_running = False
bot_thread = None
last_i_press_time = time.time()
last_anti_ban_time = time.time()
menu_open = False
anti_ban_mode = False
fishing_mode = False

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

#function that changes the state of label for anti ban
def anti_ban_on_off():
    global anti_ban_mode
    if anti_ban_switch.get():
        anti_ban_label.configure(text="On", font=("Arial", 14, "bold"))
        anti_ban_mode = True
    else:
        anti_ban_label.configure(text="Off", font=("Arial", 14, "bold"))
        anti_ban_mode = False

#function that changes the state of label for fishing mode
def fishing_mode_on_off():
    global fishing_mode
    if fishing_mode_switch.get():
        fishing_mode_label.configure(text="On", font=("Arial", 14, "bold"))
        fishing_mode = True
    else:
        fishing_mode_label.configure(text="Off", font=("Arial", 14, "bold"))
        fishing_mode = False

#function that changes the state of label for hyper potion
def hyper_potion_on_off():
    # Check the state of the CTkSwitch widget, not the function
    if hyper_mode_switch.get():
        hyper_potion_label.configure(text="On",font=("Arial", 14, "bold"))
    else:
        hyper_potion_label.configure(text="Off",font=("Arial", 14, "bold"))

#function that changes state of label for walking mode 
def walking_mode_on_off():
    if walking_mode_switch.get():
        walking_mode_label.configure(text="On",font=("Arial", 14, "bold"))
    else:
        walking_mode_label.configure(text="Off",font=("Arial", 14, "bold"))

#logic for walking up nand down
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
    global menu_open
    keyboard = KeyboardController()
    
    # Open the menu by pressing 'i'
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
            pyautogui.click(real_x, real_y)
            time.sleep(1)
            
            # Select the first Pokémon for healing
            pokemon1_x = 455
            pokemon1_y = 173   #100 for pc
            pyautogui.moveTo(pokemon1_x, pokemon1_y)
            pyautogui.click()

    # Check if a battle started before closing the menu
    battle_image = next((img for path, img in images if path == 'battle.png'), None)
    if find_image_on_screen(battle_image):
        print("Battle detected while in the menu! Exiting menu.")
        # Close the menu by pressing 'i' to resume battle
        keyboard.press('i')
        keyboard.release('i')
        menu_open = False
    else:
        # Close the menu after using the potion
        keyboard.press('i')
        keyboard.release('i')
        menu_open = False

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

#very broken
def fishing():
    keyboard = KeyboardController()
    
    # Start fishing by pressing 'f'
    keyboard.press('f')
    keyboard.release('f')
    print("Fishing started.")
    
    # Define target color in HSV color space
    target_color_rgb = (254, 216, 108)  # RGB values for #FED86C
    target_color_hsv = cv2.cvtColor(np.uint8([[target_color_rgb]]), cv2.COLOR_RGB2HSV)[0][0]
    
    lower_color_hsv = np.array([target_color_hsv[0] - 10, target_color_hsv[1] - 50, target_color_hsv[2] - 50])
    upper_color_hsv = np.array([target_color_hsv[0] + 10, target_color_hsv[1] + 50, target_color_hsv[2] + 50])
    
    fishing_active = True  # Track if fishing is active
    fishing_done = False   # Track if fishing action is complete

    # Get screen size
    screen_width, screen_height = pyautogui.size()
    
    # Define region to capture (middle of the screen)
    region_width = screen_width // 2
    region_height = screen_height // 3
    left = screen_width // 4
    top = screen_height // 2
    region = (left, top, region_width, region_height)
    
    while True:
        # Take a screenshot of the specified region
        screenshot = pyautogui.screenshot(region=region)
        screenshot_np = np.array(screenshot)

        # Convert the screenshot to HSV color space
        screenshot_hsv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2HSV)
        
        # Create a mask for the target color
        mask = cv2.inRange(screenshot_hsv, lower_color_hsv, upper_color_hsv)
        
        # Check if there are any non-zero pixels in the mask
        if np.any(mask):
            if fishing_active:
                print("Yellow bar detected! Pressing space.")
                keyboard.press(KeyCode.from_char(' '))
                keyboard.release(KeyCode.from_char(' '))
                fishing_active = False  # Set fishing as inactive
                fishing_done = True   # Mark fishing as done
                time.sleep(5)  # Delay to ensure the action completes (adjust as needed)
        else:
            fishing_active = True  # Reset fishing to active if yellow bar is not detected

        if fishing_done:
            print("Fishing action completed. Exiting fishing loop.")
            break  # Exit the loop after completing the fishing action
        
        # Wait a bit before checking again
        time.sleep(0.5)  # Increase sleep time to reduce spamming

# Function to start/stop the bot
def toggle_bot():
    global bot_running, bot_thread, anti_ban_sleep

    if bot_running:
        bot_running = False
        if start_button is not None:
            start_button.configure(text="Start Bot")
        print("Bot stopped.")
    else:
        bot_running = True
        anti_ban_sleep = False  # Reset the anti-ban sleep flag
        bot_thread = threading.Thread(target=run_bot)
        bot_thread.start()
        if start_button is not None:
            start_button.configure(text="Stop Bot")
        print("Bot started.")

#makes bot sleep every 5 minutes for so often to help ban evasion NEEDS TESTING!!!!!!!!!!!!!!!!!!!!!!!
def anti_ban_task():
    global bot_running, last_anti_ban_time, anti_ban_sleep
    while bot_running:
        current_time = time.time()
        if current_time - last_anti_ban_time >= 5 * 60:  # 5 minutes
            if anti_ban_mode:
                print("Anti-ban mode active. Sleeping for 2 minutes.")
                anti_ban_sleep = True  # Set flag to indicate sleep mode
                time.sleep(2 * 60)  # Sleep for 2 minutes
                anti_ban_sleep = False  # Reset the sleep flag after sleeping
            last_anti_ban_time = current_time
        else:
            print("anti_ban time check!")
            time.sleep(10)  # Check every 10 seconds

# Bot's main loop
def run_bot():
    global bot_running, last_i_press_time, menu_open, last_anti_ban_time

    time.sleep(3)
    last_anti_ban_time = time.time()  # Allow user time to switch to the game window
    anti_ban_thread = threading.Thread(target=anti_ban_task)
    anti_ban_thread.start()

    while bot_running:
        if anti_ban_sleep:
            # Skip actions if bot is in anti-ban sleep mode
            time.sleep(1)
            continue

        if fishing_mode:
            # Only perform fishing actions
            fishing()
        else:
            # Regular bot actions (walking and battling)
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

            # Check if it's time to press 'i' (use hyper potion)
            if not battle_detected:
                if hyper_mode_switch is not None and hyper_mode_switch.get():
                    current_time = time.time()
                    if current_time - last_i_press_time >= 20:
                        if not menu_open:
                            print("menu detected open!")
                            click_i()
                            menu_open = False
                        else:
                            click_i()
                            print("menu detected closed!")
                            menu_open = True
                        last_i_press_time = current_time

        time.sleep(1)  # Adjust delay if needed

#this will contain how to use bot and all info on bot 
def howto_gui():
    root2 = ctk.CTk()
    root2.geometry("500x500")
    print("jack is cooking.....")
    root2.resizable(False,False)
    root2.title("Information")
    info_title = ctk.CTkLabel(root2,text="NexusBot Infomation",font=("Arial",24,"bold"))
    info_title.place(y=7,x=130)
    scrollable_frame = ctk.CTkScrollableFrame(root2, width=400, height=400)
    scrollable_frame.place(y=50,x=40)
    scroll_label = ctk.CTkLabel(scrollable_frame,font=("Arial",18,"bold"),text="Features")
    scroll_label.pack(pady=3)
    scroll_label2 = ctk.CTkLabel(scrollable_frame,font=("Arial",12),text="Anti Ban:\nStops the bot every so often to take a break incase admins are watching")
    scroll_label2.pack(pady=3)
    scroll_label3 = ctk.CTkLabel(scrollable_frame,font=("Arial",12),text="Hyper Potion Check: \nTrys to heal pokemon every so often")
    scroll_label3.pack(pady=3)
    root2.mainloop()

# GUI function
def gui():
    global start_button, walking_mode_switch, hyper_mode_switch,hyper_potion_label,walking_mode_label,anti_ban_switch,anti_ban_label,fishing_mode_switch,fishing_mode_label

    root = ctk.CTk()
    root.geometry("350x500")
    root.resizable(False,False)
    ctk.set_appearance_mode("dark")
    title_frame = ctk.CTkFrame(root,width=300,height=45,fg_color="#21201E",border_width=2,border_color="red")
    title_frame.place(y=22,x=25)
    ctk.CTkLabel(title_frame, text="NexusBot Control Panel", font=("Roboto", 24, "bold")).place(y=7,x=10)
    root.title("NexusBot")
    
    pil_image = Image.open("pokeball.png")
    resized_image = pil_image.resize((150, 150))  # Resize to 150x150 pixels
    pokeball_image = ImageTk.PhotoImage(resized_image)

    # Create and display the label with the pokeball image at the bottom
    pokeball_label = ctk.CTkLabel(root, image=pokeball_image, text="")
    pokeball_label.image = pokeball_image  # Keep a reference to avoid garbage collection
    pokeball_label.place(y=100,x=100)

    frame = ctk.CTkFrame(root,width=260,height=178,fg_color="#21201E",border_width=2,border_color="red")
    frame.place(y=315,x=45)

    anti_ban_switch = ctk.CTkSwitch(root,text="Anti Ban                      ",font=("Arial", 12, "bold"),bg_color="#21201E",progress_color="#FF0000", fg_color="#FF0000",command=anti_ban_on_off)
    anti_ban_switch.place(y=336,x=80)
    anti_ban_label = ctk.CTkLabel(root,bg_color="#21201E",text="Off",font=("Arial",14,"bold"))
    anti_ban_label.place(y=334,x=50)
    
    walking_mode_switch = ctk.CTkSwitch(root, text="Walking Up/Down     ",bg_color="#21201E", font=("Arial", 12, "bold"),progress_color="#FF0000", fg_color="#FF0000",command=walking_mode_on_off)
    walking_mode_switch.place(y=364,x=80)
    walking_mode_label= ctk.CTkLabel(root, text="Off",bg_color="#21201E", font=("Arial", 14, "bold"))
    walking_mode_label.place(y=362, x=50)

    hyper_mode_switch = ctk.CTkSwitch(root, text="Hyper Potion Check",bg_color="#21201E",progress_color="#FF0000", font=("Arial", 12, "bold"), fg_color="#FF0000",command=hyper_potion_on_off)
    hyper_mode_switch.place(y=392,x=80)
    hyper_potion_label = ctk.CTkLabel(root, text="Off",bg_color="#21201E", font=("Arial", 14, "bold"))
    hyper_potion_label.place(y=390,x=50)

    fishing_mode_switch = ctk.CTkSwitch(root, text="Fishing (EXTREMLY BUGGED)",bg_color="#21201E",progress_color="#FF0000", font=("Arial", 12, "bold"), fg_color="#FF0000", command=fishing_mode_on_off)
    fishing_mode_switch.place(y=420,x=80)
    fishing_mode_label = ctk.CTkLabel(root, text="Off ",bg_color="#21201E", font=("Arial", 14, "bold"))
    fishing_mode_label.place(y=417, x=50) #PUT ON 140 WHEN FIXXED 

    howto_button = ctk.CTkButton(root,text="How to use",font=("Arial",14,"bold"),fg_color="#FF0000",hover_color="darkred",command=howto_gui)
    howto_button.place(y=283,x=105)

    start_button = ctk.CTkButton(root, text="Start Bot", font=("Arial", 14, "bold"), command=toggle_bot, fg_color="#FF0000",hover_color="darkred")
    start_button.place(y=455,x=105)

    root.mainloop()

# Call the GUI function to start the interface
gui()


#MUST MAKE FIX FOR WHEN POKEMON DIE WHAT TO DO TO CONTINUE!
#FIX FISHING MODE
