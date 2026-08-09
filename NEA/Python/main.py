import os


from intent_classifier import IntentClassifier, TrainingData
from SpeechRec import InitialTranscript, TranscriptProcessor


def main():
    MODEL_PATH = os.path.join("saved_models", "intent_model.pkl")
    print("init system")

    audioEngine= InitialTranscript(mic_name_keyword="pulse")
    processor=TranscriptProcessor()
    classifier=IntentClassifier()

    if os.path.exists(MODEL_PATH):
        print("Loading pre-trained model",MODEL_PATH)
        classifier.loadModel(MODEL_PATH)
    else:
        print("No model found training now")
        xtrain,ytrain=zip(*TrainingData)
        classifier.fit(list(xtrain),list(ytrain))
        classifier.save(MODEL_PATH)
        print("training complete")

    raw_transcript = audioEngine.listen()

    if raw_transcript:
        cleanedtext = processor.clean_text(raw_transcript)
        tokens = processor.extract_tokens(cleaned_text)
        intent = classifier.predict(cleaned_text)
        # Output results
        print("\n" + "=" * 40)
        print(f" RAW TRANSCRIPT : '{raw_transcript}'")
        print(f" CLEANED TEXT   : '{cleaned_text}'")
        print(f" TOKENS         : {tokens}")
        print(f" PREDICTED INTENT: {intent}")
        print("=" * 40 + "\n")

        # Spoken audio confirmation
        audioEngine.speak(f"Categorized as {intent}")
if __name__ == "__main__":
    main()