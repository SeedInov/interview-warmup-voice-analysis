import speech_recognition as sr

def recognize_google_wav(audio_file_path):
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Load the audio file
    with sr.AudioFile(audio_file_path) as source:
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)

        # Record the audio
        audio = recognizer.record(source)

    try:
        # Use Google Web Speech API for recognition
        text = recognizer.recognize_sphinx(audio, show_all=True)
        return text
    except sr.UnknownValueError:
        print("Google Web Speech API could not understand the audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")
        return None

def recognize_sphinx_wav(audio_file_path):
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Load the audio file
    with sr.AudioFile(audio_file_path) as source:
        # Adjust for ambient noise (optional)
        recognizer.adjust_for_ambient_noise(source)

        # Record the audio
        audio = recognizer.record(source)

    try:
        # Use Sphinx for recognition
        text = recognizer.recognize_sphinx(audio, show_all=True)
        return text
    except sr.UnknownValueError:
        print("Sphinx could not understand the audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Sphinx; {e}")
        return None

# Example usage
audio_file_path = "audio/record.wav"
result = recognize_sphinx_wav(audio_file_path)

if result:
    print("Google Speech Recognition Result:", list ( result) )
else:
    print("Speech recognition failed.")
