from googletrans import Translator
import speech_recognition as sr
import pyttsx3
import gtts
import playsound
import os , time, string, random



def listen_and_translate(target_language):
    # Initialize the translator
    translator = Translator()

    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Listen to the user's input
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Convert speech to text
        text = recognizer.recognize_google(audio)
        print("You said:", text)

        # Translate the text
        translated_text = translator.translate(text, dest=target_language)
        print("Translated:", translated_text.text)
        translated_text_str = translated_text.text


        # Speak the translated text
        # engine.say(translated_text_str)
        # engine.runAndWait()
        play_audio_text(translated_text_str, target_language, text)


    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except Exception as e:
        print("Error:", e)


def play_audio_text(translated_text_str, target_language, text):

    for i in range(5):
        try:
            converted_audio = gtts.gTTS(translated_text_str, lang=target_language)

            # Generate a unique filename for each run
            file_name = f"hello_{hash(f'{generate_random_string(5)}_{text}')}.mp3"
            file_path = f"files/{file_name}"

            converted_audio.save(file_path)
            time.sleep(1)
            playsound.playsound(file_path)
            
            #delete save file after process
            os.remove(file_path)    
            
            break
        except Exception as e:
            print("Error while playing audio trying again.", e)
            time.sleep(0.5)
            os.remove(file_path)

        



def generate_random_string(length):
    # Define the characters from which to generate the random string
    characters = string.ascii_letters + string.digits + string.punctuation

    # Generate the random string
    random_string = ''.join(random.choice(characters) for _ in range(length))

    return random_string

if __name__ == "__main__":
    target_language = input("Enter the target language (e.g., 'fr' for French): ")
    listen_and_translate(target_language)
