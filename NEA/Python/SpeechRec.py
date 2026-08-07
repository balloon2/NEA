from ctypes import CFUNCTYPE, c_char_p, c_int, cdll
import time
import pyttsx3
import speech_recognition as SR
import string
import os

# Suppress ALSA error logging on Linux
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
    pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

try:
    asound = cdll.LoadLibrary('libasound.so.2')
    asound.snd_lib_error_set_handler(c_error_handler)
except OSError:
    pass

class TranscriptProcessor:
    def __init__(self, custom_stop_words=None):
        self.stop_words = custom_stop_words or {
            "um", "uh", "ah", "er"
        }

    def clean_text(self, raw_text: str) -> str:
        if not raw_text:
            return ""
        
        # 1. Lowercase
        text = raw_text.lower()
        
        # 2. Remove punctuation
        text = text.translate(str.maketrans("", "", string.punctuation))
        
        # 3. Tokenize and filter stop words
        tokens = text.split()
        cleaned_tokens = [word for word in tokens if word not in self.stop_words]
        
        return " ".join(cleaned_tokens)

    def extract_tokens(self, cleaned_text: str) -> list[str]:
        return cleaned_text.split()

class InitialTranscript:
    def __init__(self, mic_name_keyword=None):
        # Initialize the voice engine, recognizer, and microphone
        self.engine = pyttsx3.init()
        self.rec = SR.Recognizer()
        device_index = self._find_mic_index(mic_name_keyword) if mic_name_keyword else None
        self.mic = SR.Microphone(device_index=device_index)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with self.mic as source:
            print("Starting")
            print("|adjusting for ambient noise|")
            self.speak("adjusting for ambient noise")
            time.sleep(0.5)
            self.rec.adjust_for_ambient_noise(source, duration=1)
            print("listening")
            self.speak("listening")
            time.sleep(0.5)

            try:
                audio = self.rec.listen(source, timeout=15, phrase_time_limit=10)
                print("Processing")
                init_transcript = self.rec.recognize_google(audio)
                print(f"Success! init_transcript = '{init_transcript}'")
                self.speak(f"You said: {init_transcript}")
                return init_transcript

            except SR.WaitTimeoutError:
                print("Error: No speech detected before timeout.")
                self.speak("I did not hear anything.")
                return None

            except SR.UnknownValueError:
                print("Error: Could not understand the audio.")
                self.speak("I could not understand what you said.")
                return None

            except SR.RequestError as e:
                print(f"Error: Service unavailable; {e}")
                self.speak("Network error.")
                return None

    def _find_mic_index(self, keyword: str):
        #scans mic for keywrd
        mic_list = SR.Microphone.list_microphone_names()
        for index, name in enumerate(mic_list):
            if keyword.lower() in name.lower():
                print(f"[Audio Engine] Bound to mic index {index}: '{name}'")
                return index
        print(f"[Audio Engine] Keyword '{keyword}' not found. Falling back to system default.")
        return None

# placeholder intergration
if __name__ == "__main__":
    # Tip: Pass "pulse" or "pipewire" or your device keyword if default mic fails
    assistant = InitialTranscript(mic_name_keyword="pulse")
    processor = TranscriptProcessor()

    raw_transcript = assistant.listen()
    if raw_transcript:
        cleaned = processor.clean_text(raw_transcript)
        tokens = processor.extract_tokens(cleaned)
        print(f"Raw:     '{raw_transcript}'")
        print(f"Cleaned: '{cleaned}'")
        print(f"Tokens:  {tokens}")