import pyttsx3
import pyaudio
import speech_recognition as SR

#init voice engine
engine=pyttsx3.init()

#make speak/say function
def speach(text):
    engine.say(text)
    engine.runAndWait()
#set up mic and Speech Recogntion
rec=SR.Recognizer()
mic=SR.Microphone()
with mic as source:
    print("Starting")
    print("listening")
    speach("listening")
    try:
        audio=rec.listen(source,timeout=5,phrase_time_limit=10)
        print("Processing")
        InitTranscript = rec.recognize_google(audio)
        print(f"Success! InitTranscript = '{InitTranscript}'")
        speach(f"You said: {InitTranscript}")
    except SR.WaitTimeoutError:
        print("Error: No speech detected before timeout.")
        speach("I did not hear anything.")
        InitTranscript = None
    except SR.UnknownValueError:
        print("Error: Could not understand the audio.")
        speach("I could not understand what you said.")
        InitTranscript = None
    except SR.RequestError as e:
        print(f"Error: Service unavailable; {e}")
        speach("Network error.")
        InitTranscript = None
