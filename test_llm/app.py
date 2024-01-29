import speech_recognition as sr


def record_volume(language='en-US'):
    r = sr.Recognizer()

    with sr.Microphone(device_index=1) as source:
        print("Listen...")
        audio = r.listen(source)

    try:
        # Use the language parameter in recognize_google
        query = r.recognize_google(audio, language=language)
        print(query.lower(), type(query.lower()))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")


# Example usage with English (default) language
record_volume()

# Example usage with a different language (e.g., French)
record_volume(language='fr-FR')