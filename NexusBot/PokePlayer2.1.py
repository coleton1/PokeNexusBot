import pyautogui
import cv2
import time
import numpy as np
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import KeyCode
import customtkinter as ctk
import threading
from PIL import Image, ImageTk
import warnings
import gc
import os
import pytesseract

warnings.simplefilter("ignore", UserWarning)
#TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"     # disable this when using linux 
#pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH               # this also 


# Constants
IMAGE_PATHS = ['fight.png', 'battle.png', 'hyper.png', 'bug.png', 'haunter.png', 'death.png']

SCREEN_SIZES = {
    1080: {'pokemon1_y': 100, 'name_region': (778, 335, 100, 25)},
    1200: {'pokemon1_y': 173, 'name_region': (762, 458, 100, 20)}
}


class PokeNexusBot:
    def __init__(self):
        self.bot_running = False
        self.bot_thread = None
        self.last_i_press_time = time.time()
        self.last_anti_ban_time = time.time()
        self.menu_open = False
        self.anti_ban_mode = False
        self.fishing_mode = False
        self.pokemon1_y = None
        self.name_region = None
        self.walking_mode_switch = False
        self.hyper_mode_switch= False
        self.images = self.load_images()

    def load_images(self):
        images = []
        for image_path in IMAGE_PATHS:
            image = cv2.imread(image_path)
            if image is None:
                print(f"Error: Could not load {image_path}")
            else:
                images.append((image_path, image))
                print(f"{image_path} loaded successfully.")
            gc.collect()
        return images

    def find_image_on_screen(self, image):
        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(screenshot, image_gray, cv2.TM_CCOEFF_NORMED)
        threshold = 0.7
        loc = np.where(result >= threshold)

        if len(loc[0]) > 0:
            pt = loc[::-1]  # Reverse to get (x, y)
            return pt[0][0], pt[1][0]  # Return x, y
        return None

    def walking(self):
        keyboard = KeyboardController()
        keyboard.press('a')
        time.sleep(1)
        keyboard.release('a')
        keyboard.press('d')
        time.sleep(1)
        keyboard.release('d')
        time.sleep(4)

    def walking_up_and_down(self):
        keyboard = KeyboardController()
        keyboard.press('w')
        time.sleep(1)
        keyboard.release('w')
        keyboard.press('s')
        time.sleep(1)
        keyboard.release('s')
        time.sleep(4)

    def click_i(self):
        keyboard = KeyboardController()
        keyboard.press('i')
        keyboard.release('i')
        time.sleep(1)

        hyper_image = next((img for path, img in self.images if path == 'hyper.png'), None)
        if hyper_image is not None:
            hyper_position = self.find_image_on_screen(hyper_image)
            if hyper_position:
                print("Potion found!")
                x, y = hyper_position
                pyautogui.moveTo(x + hyper_image.shape[1] // 2, y + hyper_image.shape[0] // 2)
                potion_x = x + hyper_image.shape[1] // 2
                potion_y = y + hyper_image.shape[0] // 2
                real_x = potion_x + 50
                real_y = potion_y
                pyautogui.click(real_x, real_y)
                pyautogui.click()
                time.sleep(1)

                pokemon1_x = 455
                pyautogui.moveTo(pokemon1_x, self.pokemon1_y)
                pyautogui.click()
            else:
                print("Cannot see the potion!!!!")

        battle_image = next((img for path, img in self.images if path == 'battle.png'), None)
        if self.find_image_on_screen(battle_image):
            print("Battle detected while in the menu! Exiting menu.")
            keyboard.press('i')
            keyboard.release('i')
            self.menu_open = False
        else:
            keyboard.press('i')
            keyboard.release('i')
            self.menu_open = False

    def detect_screen_size(self):
        screen_width, screen_height = pyautogui.size()
        print(f"Screen rez: {screen_width}x{screen_height}")
        print(screen_height)

        if screen_height in SCREEN_SIZES:
            screen_info = SCREEN_SIZES[screen_height]
            self.pokemon1_y = screen_info['pokemon1_y']
            self.name_region = screen_info['name_region']
            print(f"Screen detected! pokemon1_y set to {self.pokemon1_y}")
        else:
            print("Couldn't detect screen size!")

    def click_image(self, image, image_path):
        position = self.find_image_on_screen(image)
        if position:
            x, y = position
            pyautogui.moveTo(x + image.shape[1] // 2, y + image.shape[0] // 2)
            pyautogui.click()

            if image_path == 'fight.png':
                self.check_pokemon_name()
                time.sleep(1)
                pyautogui.moveTo(x + image.shape[1] // 2, y + image.shape[0] // 2)
                pyautogui.click()

            if image_path == 'death.png':
                time.sleep(1)
                pyautogui.moveTo(x + image.shape[1] // 2, y + image.shape[0] // 2 + 72)
                pyautogui.click()
                pyautogui.moveTo(x + image.shape[1] // 2 + 100, y + image.shape[0] // 2 + 20)
                time.sleep(0.5)
                pyautogui.click()

            screen_width, screen_height = pyautogui.size()
            pyautogui.moveTo(screen_width // 2, screen_height // 2)

    def fishing(self):
        keyboard = KeyboardController()
        keyboard.press('f')
        keyboard.release('f')
        print("Fishing started.")

        target_color_rgb = (254, 216, 108)
        target_color_hsv = cv2.cvtColor(np.uint8([[target_color_rgb]]), cv2.COLOR_RGB2HSV)[0][0]
        lower_color_hsv = np.array([target_color_hsv[0] - 10, target_color_hsv[1] - 50, target_color_hsv[2] - 50])
        upper_color_hsv = np.array([target_color_hsv[0] + 10, target_color_hsv[1] + 50, target_color_hsv[2] + 50])

        fishing_active = True
        fishing_done = False

        screen_width, screen_height = pyautogui.size()
        region_width = screen_width // 2
        region_height = screen_height // 3
        left = screen_width // 4
        top = screen_height // 2
        region = (left, top, region_width, region_height)

        while True:
            screenshot = pyautogui.screenshot(region=region)
            screenshot_np = np.array(screenshot)
            screenshot_hsv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2HSV)
            mask = cv2.inRange(screenshot_hsv, lower_color_hsv, upper_color_hsv)

            if np.any(mask):
                if fishing_active:
                    print("Yellow bar detected! Pressing space.")
                    keyboard.press(KeyCode.from_char(' '))
                    keyboard.release(KeyCode.from_char(' '))
                    fishing_active = False
                    fishing_done = True
                    time.sleep(5)
            else:
                fishing_active = True

            if fishing_done:
                print("Fishing action completed. Exiting fishing loop.")
                break

            time.sleep(0.5)

    def toggle_bot(self):
        if self.bot_running:
            self.bot_running = False

            print("Bot stopped.")
        else:
            self.bot_running = True
            self.anti_ban_sleep = False
            self.bot_thread = threading.Thread(target=self.run_bot)
            self.bot_thread.start()
            print("Bot started.")

    def anti_ban_task(self):
        while self.bot_running:
            current_time = time.time()
            if current_time - self.last_anti_ban_time >= 5 * 60:    # this not working must fix
                if self.anti_ban_mode:
                    print("Anti-ban mode active. Sleeping for 2 minutes.")
                    self.anti_ban_sleep = True
                    time.sleep(2 * 60)
                    self.anti_ban_sleep = False
                self.last_anti_ban_time = current_time
            else:
                print("anti_ban time check!")
                time.sleep(10)

    def extract_pokemon_name(self):
        screenshot = pyautogui.screenshot(region=self.name_region)
        screenshot.save('test.png')
        screenshot_np = np.array(screenshot)
        screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)
        _, processed_image = cv2.threshold(screenshot_gray, 150, 255, cv2.THRESH_BINARY)
        resized_image = cv2.resize(processed_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        pokemon_name = pytesseract.image_to_string(resized_image, config=custom_config).strip()
        return pokemon_name

    def check_pokemon_name(self):
        pokemon_name = self.extract_pokemon_name()
        print(f"Detected Pokémon name: {pokemon_name}")

        if pokemon_name.startswith('IS'):
            print("Pokémon name starts with [s], stopping the bot!")
            self.stop_bot()
        elif pokemon_name.startswith('Machop'):
            print("pokemon found!")
            self.stop_bot()
        elif pokemon_name.startswith('Sudowoodo'):
            print("pokemon found!")
            self.stop_bot()
        elif pokemon_name.startswith('IE'):
            print("ELITE POKE FOUND")
            self.stop_bot()
        elif pokemon_name.startswith('JE'):
            print("ELITE")
            self.stop_bot()
        else:
            print(f"Pokémon name is: {pokemon_name}. Continuing...")

    def stop_bot(self):
        print("Bot has been stopped.")
        os._exit(0)

    def run_bot(self):
        time.sleep(3)
        self.last_anti_ban_time = time.time()
        anti_ban_thread = threading.Thread(target=self.anti_ban_task)
        anti_ban_thread.start()

        while self.bot_running:
            if self.anti_ban_sleep:
                time.sleep(1)
                continue

            if self.fishing_mode:
                self.fishing()
            else:
                battle_detected = False

                for image_path, image in self.images:
                    if self.find_image_on_screen(image):
                        if image_path == 'fight.png':
                            battle_detected = True
                            self.click_image(image, image_path)
                            print("Fight action triggered")
                        if image_path == 'battle.png':
                            battle_detected = True
                            print("Battle detected!")
                        if image_path == 'death.png':
                            battle_detected = True
                            self.click_image(image, image_path)
                            print("IT SAW THE DEATH")

                if not battle_detected:
                    if self.walking_mode_switch:
                        self.walking_up_and_down()
                    else:
                        self.walking()

                if not battle_detected:
                    #if self.hyper_mode_switch is not None:
                    if self.hyper_mode_switch:
                        current_time = time.time()
                        if current_time - self.last_i_press_time >= 40:
                            if not self.menu_open:
                                print("menu detected open!")
                                self.click_i()
                                self.menu_open = False
                            else:
                                self.click_i()
                                print("menu detected closed!")
                                self.menu_open = True
                            self.last_i_press_time = current_time

            time.sleep(1)

class PokeMMOBot:
    def __init__(self):
        # Add PokeMMO-specific logic here
        pass

    def toggle_bot(self):
        # Add PokeMMO-specific toggle logic here
        pass

    def run_bot(self):
        # Add PokeMMO-specific bot logic here
        pass

class BotController:
    def __init__(self, start_button=None, walking_mode_switch=None, hyper_mode_switch=None):
        self.start_button = start_button
        self.walking_mode_switch = walking_mode_switch
        self.hyper_mode_switch = hyper_mode_switch
        self.current_bot = PokeNexusBot()  # Default to PokeNexusBot

    def set_bot(self, bot_type):
        if bot_type == "PokeNexus":
            self.current_bot = PokeNexusBot()
        elif bot_type == "PokeMMO":
            self.current_bot = PokeMMOBot()

    def toggle_bot(self):
        self.current_bot.toggle_bot()

    def detect_screen_size(self):
        self.current_bot.detect_screen_size()

class PokePlayerApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("350x500")
        self.root.resizable(False, False)
        ctk.set_appearance_mode("dark")
        self.title_frame = ctk.CTkFrame(self.root, width=310, height=45, fg_color="#21201E", border_width=2, border_color="red")
        self.title_frame.place(y=15, x=20)
        ctk.CTkLabel(self.title_frame, text="PokePlayer Control Panel", font=("Roboto", 24, "bold")).place(y=8, x=6)
        self.root.title("PokePlayer")

        pil_image = Image.open("pokeball.png")
        resized_image = pil_image.resize((150, 150))
        self.pokeball_image = ImageTk.PhotoImage(resized_image)

        self.pokeball_label = ctk.CTkLabel(self.root, image=self.pokeball_image, text="")
        self.pokeball_label.image = self.pokeball_image
        self.pokeball_label.place(y=85, x=100)

        self.frame = ctk.CTkFrame(self.root, width=260, height=178, fg_color="#21201E", border_width=2, border_color="red")
        self.frame.place(y=315, x=45)

        self.anti_ban_switch = ctk.CTkSwitch(self.root, text="Anti Ban                      ", font=("Arial", 12, "bold"), bg_color="#21201E", progress_color="#FF0000", fg_color="#FF0000", command=self.anti_ban_on_off)
        self.anti_ban_switch.place(y=336, x=80)
        self.anti_ban_label = ctk.CTkLabel(self.root, bg_color="#21201E", text="Off", font=("Arial", 14, "bold"))
        self.anti_ban_label.place(y=334, x=50)

        self.walking_mode_switch = ctk.CTkSwitch(self.root, text="Walking Up/Down     ", bg_color="#21201E", font=("Arial", 12, "bold"), progress_color="#FF0000", fg_color="#FF0000", command=self.walking_mode_on_off)
        self.walking_mode_switch.place(y=364, x=80)
        self.walking_mode_label = ctk.CTkLabel(self.root, text="Off", bg_color="#21201E", font=("Arial", 14, "bold"))
        self.walking_mode_label.place(y=362, x=50)

        self.hyper_mode_switch = ctk.CTkSwitch(self.root, text="Hyper Potion Check", bg_color="#21201E", progress_color="#FF0000", font=("Arial", 12, "bold"), fg_color="#FF0000", command=self.hyper_potion_on_off)
        self.hyper_mode_switch.place(y=392, x=80)
        self.hyper_potion_label = ctk.CTkLabel(self.root, text="Off", bg_color="#21201E", font=("Arial", 14, "bold"))
        self.hyper_potion_label.place(y=390, x=50)

        self.fishing_mode_switch = ctk.CTkSwitch(self.root, text="Fishing Mode", bg_color="#21201E", progress_color="#FF0000", font=("Arial", 12, "bold"), fg_color="#FF0000", command=self.fishing_mode_on_off)
        self.fishing_mode_switch.place(y=420, x=80)
        self.fishing_mode_label = ctk.CTkLabel(self.root, text="Off ", bg_color="#21201E", font=("Arial", 14, "bold"))
        self.fishing_mode_label.place(y=417, x=50)

        self.pokemmo_button = ctk.CTkOptionMenu(self.root, values=["PokeNexus", "PokeMMO"], fg_color="#21201E", button_color="#FF0000", button_hover_color="darkred", command=self.set_bot_type)
        self.pokemmo_button.place(y=250, x=105)

        self.howto_button = ctk.CTkButton(self.root, text="How to use", font=("Arial", 14, "bold"), fg_color="#FF0000", hover_color="darkred", command=self.howto_gui)
        self.howto_button.place(y=283, x=105)

        self.start_button = ctk.CTkButton(self.root, text="Start Bot", font=("Arial", 14, "bold"), command=self.toggle_bot, fg_color="#FF0000", hover_color="darkred")
        self.start_button.place(y=455, x=105)

        # Initialize BotController with GUI references
        self.bot_controller = BotController(
            start_button=self.start_button,
            walking_mode_switch=self.walking_mode_switch,
            hyper_mode_switch=self.hyper_mode_switch
        )

    def set_bot_type(self, bot_type):
        self.bot_controller.set_bot(bot_type)

    def toggle_bot(self):
        self.bot_controller.toggle_bot()

    def anti_ban_on_off(self):
        self.bot_controller.current_bot.anti_ban_mode = self.anti_ban_switch.get()
        self.anti_ban_label.configure(text="On" if self.bot_controller.current_bot.anti_ban_mode else "Off", font=("Arial", 14, "bold"))

    def walking_mode_on_off(self):
        self.bot_controller.current_bot.walking_mode_switch = self.walking_mode_switch.get()
        self.walking_mode_label.configure(text="On" if self.bot_controller.current_bot.walking_mode_switch else "Off", font=("Arial", 14, "bold"))

    def hyper_potion_on_off(self):
        self.bot_controller.current_bot.hyper_mode_switch = self.hyper_mode_switch.get()
        self.hyper_potion_label.configure(text="On" if self.bot_controller.current_bot.hyper_mode_switch else "Off", font=("Arial", 14, "bold"))

    def fishing_mode_on_off(self):
        self.bot_controller.current_bot.fishing_mode = self.fishing_mode_switch.get()
        self.fishing_mode_label.configure(text="On" if self.bot_controller.current_bot.fishing_mode else "Off", font=("Arial", 14, "bold"))

    def howto_gui(self):
        root2 = ctk.CTk()
        root2.geometry("500x500")
        root2.resizable(False, False)
        root2.title("PokePlayer Information")
        info_title = ctk.CTkLabel(root2, text="PokePlayer Infomation", font=("Arial", 24, "bold"))
        info_title.place(y=7, x=130)
        scrollable_frame = ctk.CTkScrollableFrame(root2, width=400, height=400)
        scrollable_frame.place(y=50, x=40)
        scroll_label = ctk.CTkLabel(scrollable_frame, font=("Arial", 18, "bold"), text="Features")
        scroll_label.pack(pady=3)
        scroll_label2 = ctk.CTkLabel(scrollable_frame, font=("Arial", 12), text="Anti Ban:\nStops the bot every so often to take a break incase admins are watching")
        scroll_label2.pack(pady=3)
        scroll_label3 = ctk.CTkLabel(scrollable_frame, font=("Arial", 12), text="Hyper Potion Check: \nTrys to heal pokemon every so often")
        scroll_label3.pack(pady=3)
        scroll_label4 = ctk.CTkLabel(scrollable_frame, font=("Arial", 12), text="Fishing Mode: \ninstead of walking to trigger battles it will start\nfishing for battles now (very broken)")
        scroll_label4.pack(pady=3)
        scroll_label5 = ctk.CTkLabel(scrollable_frame, font=("Arial", 12), text="Walking Up/Down: \nWhen turned on just simply makes character\nwalk up and down instead of side to side")
        scroll_label5.pack(pady=3)
        scroll_label6 = ctk.CTkLabel(scrollable_frame, font=("Arial", 18, "bold"), text="How to use")
        scroll_label6.pack(pady=3)
        scroll_label7 = ctk.CTkLabel(scrollable_frame, font=("Arial", 12), text="1.Bot will only use pokemon slot 1 to battle")
        scroll_label7.pack(pady=3)
        scroll_label8 = ctk.CTkLabel(scrollable_frame, font=("Arial", 12), text="2.If using hyper potion mode\nhyper potion MUST be in top half of item bag")
        scroll_label8.pack(pady=3)
        scroll_label9 = ctk.CTkLabel(scrollable_frame, font=("Arial", 12), text="3.Currently the pokemon1_y variable is static and must be changed\n to the correct y axis to click slot1(FIXED)")
        scroll_label9.pack(pady=3)

        detect_button = ctk.CTkButton(root2, text="Detect Screen size", command=self.bot_controller.current_bot.detect_screen_size, fg_color="#FF0000", hover_color="darkred")
        detect_button.place(x=180, y=467)

        root2.mainloop()

    def run(self):
        self.bot_controller.current_bot.detect_screen_size()
        self.root.mainloop()

if __name__ == "__main__":
    app = PokePlayerApp()
    app.run()
