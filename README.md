PokePlayer Bot
Overview
PokePlayer is a versatile automation bot designed to streamline gameplay in Pokémon-themed games. With features like automated battling, fishing, and anti-ban safeguards, it offers a more seamless and efficient gaming experience. The bot utilizes image recognition and keyboard automation to interact with the game in real time.

Features
Automated Battling
Detects battles, uses potions when needed, and selects moves automatically.
Fishing Mode
Initiates fishing actions, increasing opportunities for encounters and gameplay progress.
Anti-Ban Mode
Periodically pauses activity to reduce the risk of detection.
Walking Simulation
Simulates character movement to explore the game environment naturally.
Screen Size Detection
Automatically adjusts settings based on detected screen resolution for optimized gameplay.
Customizable Settings
Easily toggle features like anti-ban, fishing mode, and potion usage.
Installation
Clone the Repository

bash
Copy code
git clone https://github.com/yourusername/PokePlayer.git
cd PokePlayer
Install Dependencies
Ensure you have Python 3.9 installed. Install the required packages:

bash
Copy code
pip install -r requirements.txt
Tesseract OCR
Download and install Tesseract OCR, and update the path in the script:

python
Copy code
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
Image Assets
Place required images (e.g., fight.png, battle.png, etc.) in the same directory as the bot script.

Usage
Run the Bot

bash
Copy code
python pokeplayer.py
Login
Use the login screen to access the control panel. Default credentials are admin/admin.

Control Panel

Start/Stop Bot: Start or stop the bot as needed.
Feature Toggles: Switches for anti-ban, fishing mode, and potion usage.
Screen Size Detection: Automatically configures settings based on your screen resolution.
How to Use
Access the "How to Use" section for a detailed guide on each feature and customization option.

Known Issues
Fishing Mode: Currently in beta; further testing required for stability.
Immune Move Detection: Unable to detect if moves are ineffective due to type immunity.
Pokémon Fainting: Logic for handling fainted Pokémon is still in development.
Contributing
Contributions are welcome! Please fork this repository and submit a pull request with your enhancements or fixes.

License
This project is licensed under the MIT License. For more information, see the LICENSE file.

Contact
For support or inquiries, please reach out to Coleton Boutilier at [your-email@example.com].

Note: This bot is designed for educational and personal use only. Please use responsibly and in accordance with the game’s terms of service.
