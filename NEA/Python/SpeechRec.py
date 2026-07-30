import pyttsx3
import pyaudio
import speech_recognition as SR
import string
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
    def __init__(self):
        # Initialize the voice engine, recognizer, and microphone
        self.engine=pyttsx3.init()
        self.rec=SR.Recognizer()
        self.mic=SR.Microphone()
    def speach(self,text):
        self.engine.say(text)
        self.engine.runAndWait()
    def listen(self):
        with self.mic as source:
            print("Starting")
            print("|adjusting for ambient noise|")
            self.speach("adjusting for ambient noise")
            self.rec.adjust_for_ambient_noise(source, duration=1)
            print("listening")
            self.speach("listening")

            try:
                audio = self.rec.listen(source, timeout=15, phrase_time_limit=10)
                print("Processing")
                InitTranscript = self.rec.recognize_google(audio)
                print(f"Success! InitTranscript = '{InitTranscript}'")
                self.speach(f"You said: {InitTranscript}")
                return InitTranscript

            except SR.WaitTimeoutError:
                print("Error: No speech detected before timeout.")
                self.speach("I did not hear anything.")
                return None

            except SR.UnknownValueError:
                print("Error: Could not understand the audio.")
                self.speach("I could not understand what you said.")
                return None

            except SR.RequestError as e:
                print(f"Error: Service unavailable; {e}")
                self.speach("Network error.")
                return None

# placeholder intergration
if __name__ == "__main__":
    assistant = InitialTranscript()
    processor = TranscriptProcessor()

    raw_transcript = assistant.listen()
    if raw_transcript:
        cleaned = processor.clean_text(raw_transcript)
        tokens = processor.extract_tokens(cleaned)
        print(f"Raw:     '{raw_transcript}'")
        print(f"Cleaned: '{cleaned}'")
        print(f"Tokens:  {tokens}")
