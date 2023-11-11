import pyaudio
import struct
import pvporcupine
import speech_recognition as sr
import pyautogui
import logging
import sys
import json
import os
from datetime import datetime
from time import sleep

class JsonFileHandler(logging.FileHandler):
    def emit(self, record):
        log_entry = self.format(record)
        self.stream.write(json.dumps(log_entry) + '\n')
        self.stream.flush()

class CustomFormatter(logging.Formatter):
    def format(self, record):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        original_format = self._style._fmt
        self._style._fmt = f"{current_time} '{original_format}'"

        result = super().format(record)
        self._style._fmt = original_format

        return result

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
json_handler = JsonFileHandler('log.json', mode='a')
formatter = CustomFormatter("%(message)s")
json_handler.setFormatter(formatter)
logger.addHandler(json_handler)

config_file = 'config.json'

def is_valid_access_key(key):
    # Check if the key is of the expected length and contains only allowed characters
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/=+")
    return len(key) == 56 and all(char in allowed_chars for char in key)

def load_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            return json.load(file)
    else:
        if len(sys.argv) != 3:
            logger.error("ERROR- Usage: python stt.py <access_key> <keyword>")
            print("Usage: python stt.py <access_key> <keyword>")
            logger.info("INFO- Exiting.")
            print("Exiting.")
            sys.exit(1)
        
        access_key = sys.argv[1]
        if not is_valid_access_key(access_key):
            logger.error("ERROR- Invalid access_key.")
            print("Invalid access_key.")
            logger.info("INFO- Exiting.")
            print("Exiting.")
            sys.exit(1)

        config = {
            'access_key': access_key,
            'keyword': sys.argv[2]
        }
        with open(config_file, 'w') as file:
            json.dump(config, file)
        return config

def main():
    config = load_config()
    program_initialized = False
    waiting_for_keyword = False

    def clean_up(porcupine, audio_stream, pa):
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()
        logger.info("INFO- Cleaned up resources.")
        print("Cleaned up resources.")
        logger.info("INFO- Exiting.")
        print("Exiting.")

    try:
        porcupine = pvporcupine.create(access_key=config['access_key'], keywords=[config['keyword']])
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)
        recognizer = sr.Recognizer()
        program_initialized = True

        while True:
            if program_initialized:
                logger.info("INFO- Program started. Waiting for keyword.")
                print("Program started. Waiting for keyword.")
                program_initialized = False

            if waiting_for_keyword:
                logger.info("INFO- Waiting for keyword.")
                print("Waiting for keyword.")
                waiting_for_keyword = False

            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            if porcupine.process(pcm) >= 0:
                with sr.Microphone() as source:
                    logger.info("INFO- Keyword detected. Listening for speech...")
                    print("Keyword detected. Listening for speech...")
                    recognizer.adjust_for_ambient_noise(source, duration=0.25)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=60)

                    try:
                        text = recognizer.recognize_google(audio)
                        logger.info(f"INFO- Speech recognized: `{text}`")
                        print(f"Speech recognized: `{text}`")
                        if text.strip().lower() == "exit":
                            logger.info("INFO- Exit command received.")
                            print("Exit command received.")
                            break
                        pyautogui.write(text)
                        pyautogui.press('enter')
                        waiting_for_keyword = True
                    except sr.WaitTimeoutError:
                        logger.warning("WARNING- Listening timed out while waiting for phrase to start.")
                        print("Listening timed out while waiting for phrase to start.")
                        waiting_for_keyword = True
                    except sr.UnknownValueError:
                        logger.warning("WARNING- Speech not understood.")
                        print("Speech not understood.")
                        waiting_for_keyword = True
                    except sr.RequestError as e:
                        logger.error(f"ERROR- Google Speech Recognition service error: `{e}`")
                        print(f"Google Speech Recognition service error: `{e}`")
                        waiting_for_keyword = True

    except Exception as e:
        logger.error(f"ERROR- Unexpected error: `{e}`")
        print(f"Unexpected error: `{e}`")
    except KeyboardInterrupt:
        pass
    finally:
        clean_up(porcupine, audio_stream, pa)

if __name__ == "__main__":
    main()
