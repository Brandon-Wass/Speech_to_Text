# Speech-to-Text With Keyword Detection

This repository contains a Python script that implements a robust speech-to-text system using keyword detection. The program listens for a specific keyword and, upon detection, converts the following spoken words into text. The converted text is then programmatically input into the current active field, simulating keyboard typing.

## Features
- Keyword detection using pvporcupine.
- Speech-to-text conversion using speech_recognition.
- Automated typing using pyautogui.
- Logging system to track operations and errors.
- Configuration file support for easy setup and reuse.
- Works on Windows and Linux based systems, provided the required libraries are installed.

## PicoVoice Account Setup
- To use this script, you first need an `AccessKey` from PicoVoice. Follow these steps to set up your account and obtain the `AccessKey`:

  - Visit https://console.picovoice.ai/signup and enter your email address and chosen password to create an account.
  - Click the `Create Account` button.
  - Verify your email address by checking your email and clicking the `Verify email address` button.
  - Once your account is created and verified, navigate to https://console.picovoice.ai/login and login.
  - You will be prompted to enter your first and last name, then choose the options you wish and click the `continue` button.
  - You will be redirected to the main dashboard https://console.picovoice.ai/ where you will see your `AccessKey`.
  - Use this `AccessKey` as an argument when you first run the script in place of `<access_key>`.
    ```bash
    python stt.py <access_key> <keyword>
    ```

## Keywords
- You can choose from the following list of default `Keywords` without any additional setup
  - porcupine, terminator, bumblebee, picovoice, alexa, hey barista, pico clock, jarvis, hey google, computer, hey siri, grasshopper, ok google, blueberry, grapefruit, americano

## Installation
1. Clone the repository.
2. Install the required Python libraries:
   ```bash
   pip install pyaudio pvporcupine SpeechRecognition logging pyautogui
   ```
3. Run the script with the `access_key` from your PicoVoice account and a `keyword` from the list of default `Keywords` provided above as arguments for the first time.
   ```bash
   python stt.py <access_key> <keyword>
   ```
   Example:
   ```bash
   python stt.py 231847oijkhBEfa98734ha4qrkjqb23412345q34tga4ef5qyha35g+= listen
   ```
5. For subsequent uses if you close the program, simply run:
   ```bash
   python stt.py
   ```

## Usage
- After starting the script, it will continuously listen for the specified `keyword`.
- Once the `keyword` is detected, the script will convert the following spoken words into text and type them out wherever the cursor is focused.
- If the user says the `keyword` followed by "exit", the program will close.

## Configuration
The script uses a JSON configuration file (`config.json`) to store the `access_key` and `keyword`. This file is automatically created upon the first run of the script with provided arguments.

## Logging
All events and errors are logged into `log.json` for troubleshooting and monitoring purposes.

## Possible Issues
- If you encounter an error with your `access_key` not working even though it is correct you should:
  - Check the acceptable characters list in the `stt.py` file and add any necessary characters.
    ```python
        allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/=+")
    ```
  - Contact me so I can add the missing characters to the list and update the repo.
- For other issues causing the program to crash, contact me with the details of the error so I can fix them and update the repo:
  - You can find error details in the `log.json` file that is generated in the same directory as the program when it is run.
  - Most errors can be quickly found by searching for `ERROR` in the `log.json` file.
- Unexpected error: `One or more keywords are not available by default...`:
  - Choose a `keyword` from the list of default `Keywords`.
    - I have not built the program to accept custom `Keywords` that can be made on the PicoVoice dashboard.
    - This will be part of a future update to the program.

## Contributing
Contributions to improve the script or add new features are welcome. Please feel free to fork the repository and submit pull requests.

## License
This project is open-sourced under the [MIT License](LICENSE).

---

Enjoy the hands-free convenience of controlling your computer with your voice! 🎤💻
