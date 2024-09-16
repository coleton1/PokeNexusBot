import pyautogui
import cv2
import time
import numpy as np
from pynput.keyboard import Controller as KeyboardController
import customtkinter as ctk 

#load images
image_paths = ['fight.png', 'battle.png','hyper.png','bug.png']#slowly removing these because cords are easier to use and more reliable 
images = []

#Load all images
for image_path in image_paths:
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not load {image_path}")
    else:
        images.append((image_path, image))  # Store both the image path and the image itself
        print(f"{image_path} loaded successfully.")
        print("**********************************")
        print("NexusBot is trying to start!")
        print("**********************************")

    print("==================================")
    print("NexusBot has successfully started!")
    print("==================================")
    
#this was mostly made by chatgpt but it somehow works 
def find_image_on_screen(image):
    #Take a screenshot of the current screen
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)

    #Convert both screenshot and image to grayscale for easier matchability i think
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #Use OpenCV to search for the image within the screenshot
    result = cv2.matchTemplate(screenshot, image_gray, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # Adjust as needed for accuracy DONT TOUCH FFS
    loc = np.where(result >= threshold)
    
    #do not edit this or else everything will crumble into pieces 
    if len(loc[0]) > 0:
        #Get the coordinates of the match DONT TOUCH
        pt = loc[::-1]  #Reverse the array to get (x, y)
        return pt[0][0], pt[1][0]  #x & y
    return None

#simple logic to make character walk right to left to get battles started
def walking():
    keyboard = KeyboardController()
    keyboard.press('a')
    time.sleep(1)
    keyboard.release('a')
    keyboard.press('d')
    time.sleep(1)
    keyboard.release('d')

#function that will click 'i' to open bag and use potion if able to 
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

            #Debugging: Print the coordinates incase bug
            print(f"Potion coordinates: x={x}, y={y}")

            #Calculate the click position DNT
            potion_x = x + hyper_image.shape[1] // 2
            potion_y = y + hyper_image.shape[0] // 2

            # Debugging: Print the adjusted click coordinates disable when building
            print(f"Clicking at: x={potion_x}, y={potion_y}")

            # Move to the potion and click
            pyautogui.moveTo(potion_x, potion_y, duration=0.2)  # Smooth movement
            time.sleep(3)
            real_x = potion_x + 50
            real_y = potion_y
            pokemon1_x = 455
            pokemon1_y = 195 
            print("clicking")
            pyautogui.click(real_x, real_y)
            time.sleep(2)
            print("clicked!")
            time.sleep(2)
            pyautogui.moveTo(pokemon1_x, pokemon1_y)
            time.sleep(1)
            pyautogui.click(pokemon1_x, pokemon1_y)

            # Sometimes it will run this function when in battle so this prevents it from getting stuck in potion menu
            bug = next((img for path, img in images if path == 'bug.png'), None)
            if bug is not None:
                bug_is_there = find_image_on_screen(bug)
                if bug_is_there:
                    pyautogui.click([pokemon1_x, pokemon1_y])

        else:
            print("Potion not found.")
    else:
        print("No potion image loaded.")
            
    time.sleep(1.5)
    keyboard.press('i')
    keyboard.release('i')

#function used to click images found such as fight.png
def click_image(image, image_path):
    #Find image on the screen
    position = find_image_on_screen(image)
    if position:
        #Move the mouse to the position and click
        x, y = position
        pyautogui.moveTo(x + image.shape[1] // 2, y + image.shape[0] // 2)
        pyautogui.click()

        #Debugging, not really needed anymore but can come in handy
        print(f"Clicked {image_path} at {x + image.shape[1] // 2}, {y + image.shape[0] // 2}")

        #Move to the specific coordinates after clicking fight.png
        if image_path == 'fight.png':
            time.sleep(1) #Add a slight delay before clicking the second position
            print("Clicking specific coordinates after fight.png")
            #changed this to just auto click first move slot which can be found with the cords below
            pyautogui.moveTo(840, 758) # Cords of first move slot on every pokemon 
            pyautogui.click()

        #  ESENTIAL Move the mouse back to the center of the screen, bot will bug out if this isnt here
        screen_width, screen_height = pyautogui.size()
        pyautogui.moveTo(screen_width // 2, screen_height // 2)

#gui function that will eventually by the menu that will make it easier for users to use that arnt me lol but for now this isnt used.
def gui():
    
    root = ctk.CTk()
    root.geometry("500x500")
    label = ctk.CTkLabel(root,text="this is a test").pack()
    
    root.mainloop()

#Initialize variables bc chatgpt told me i have to :(
walking_enabled = True
menu_open = False #Track if the 'i' menu is open (pretty sure bot ignores menu_open variable but bot works so this stays )
last_i_press_time = time.time()  #Track the time for 'i' press(60 second clock)

#Continuously search for the images and click if found
while True:
    battle_detected = False

    #Check for battle images
    for image_path, image in images:
        if find_image_on_screen(image):
            if image_path == 'battle.png':
                #If battle.png is detected, set battle_detected to True
                battle_detected = True
                print("Battle detected!")
                break
            elif image_path == 'fight.png':
                #If fight.png is detected, it will also change battle_detected to true just incase doesnt pick up battle.png
                battle_detected = True
                click_image(image, image_path)
                print("Fight action triggered")
                break  #Exit the loop if any battle image is found
    
    #pretty much english just read it lol
    if not battle_detected:
        if walking_enabled:
            walking()

        #Check if it's time to press 'i'
        current_time = time.time()
        if current_time - last_i_press_time >= 30:  #set interger to whatever seconds u want it to check to open bag
            if not menu_open:  #If menu is closed, open it
                click_i()
                menu_open = True
            else:  #If menu is open, close it
                click_i()
                menu_open = False

            last_i_press_time = current_time #Update last press time

    time.sleep(1)  # Adjust the delay to suit your needs (1 second in this case)



"""SO FAR BOT WILL

- walk left to right when started to look for a battle

- will check every 60 seconds to try to use a hyper potion on the pokemon in use incase it is missing health

- there is a bug that happens rarely when the bot clicks 'i' to open the bag a second before the battle starts so the menu opens up when the battle opens up
- temp fix was to enter an image called bug.png which is an image of the bug happening so when the bot sees that the bug happened it will close the window that is bugged making the bot continue 

- Bot now has cords set to first move so it now will always pick the first move slot instead of trying to look for a certain picture
- that means you can now use whatever pokemon you want and the bot will attack with it when before you had to manualy enter a picture of the move into the code which was not ideal.

- this bot is held together by tape and will probably break once i try this code on my windows machine. 

"""


"""
THINGS TO IMPROVE!!!!!!!!!!!!!!!!

Walking logic.
GUI
logic that checks if pokemon is low health which currently bot does not know if pokemon is low health .
clean code up a bit for easier readability 
make discord for bot and possibly sell it once gui works and i can hammer out more bugs"""






