from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys

recognizer = speech_recognition.Recognizer()
recognizer.dynamic_energy_threshold = False
recognizer.energy_threshold = 50

speaker = tts.init()
speaker.setProperty('rate', 150)

todo_list = []

recognizer = speech_recognition.Recognizer()
recognizer.dynamic_energy_threshold = False
recognizer.energy_threshold = 50


# language  : en_US, de_DE, ...
# gender    : VoiceGenderFemale, VoiceGenderMale
def change_voice(engine, language, gender='VoiceGenderFemale'):
    for voice in engine.getProperty('voices'):
        if language in voice.languages and gender == voice.gender:
            engine.setProperty('voice', voice.id)
            return True

    raise RuntimeError("Language '{}' for gender '{}' not found".format(language, gender))


speaker = tts.init()
change_voice(speaker, "fr_FR", "VoiceGenderMale")
speaker.setProperty('rate', 140)


def hello():
    speaker.say("Bonjour, que puis-je faire pour vous")
    speaker.runAndWait()


def quit():
    speaker.say("Fin de la communication, bonne journée maître!")
    speaker.runAndWait()
    sys.exit(1)


def create_note():
    global recognizer
    global speaker

    # speaker.say("What do you want to write onto your note?")
    speaker.say("Que voulez-vous écrire sur votre nouvelle note?")
    speaker.runAndWait()

    done = False

    while not done:
        with speech_recognition.Microphone() as mic:

            recognizer.adjust_for_ambient_noise(mic, duration=1)
            # print("Say something:")
            print("Dites quelque chose (création note):")
            speaker.say("Je vous écoute pour la création de la note")
            speaker.runAndWait()
            audio = recognizer.listen(mic)

            try:
                note = recognizer.recognize_google(audio, language='fr-FR')
                note = note.lower()
                print(note)

                if 'stop' in note or 'quitter' in note or 'fin' in note:
                    return None

                # speaker.say("Choose a filename!")
                speaker.say("Choisissez un nom pour votre nouvelle note !")
                speaker.runAndWait()

            except:
                recognizer = speech_recognition.Recognizer()
                # speaker.say("I did not understand you! Please try again")
                speaker.say("Je n'ai pas compris! S'il vous plaît recommencez.")
                speaker.runAndWait()

            recognizer.adjust_for_ambient_noise(mic, duration=1)
            # print("Say something")
            print("Dites quelque chose (création note):")
            speaker.say("Je vous écoute")
            speaker.runAndWait()
            audio = recognizer.listen(mic)

            try:

                filename = recognizer.recognize_google(audio, language='fr-FR')
                filename = filename.lower()
                print(filename)

                if 'stop' in filename or 'quitter' in filename or 'fin' in filename:
                    return None

                with open(filename, 'w') as f:
                    f.write(note)
                    done = True
                    # speaker.say(f"I succesfully created the note {filename}")
                    speaker.say(f"J'ai créé la nouvelle note {filename} avec succès")
                    speaker.runAndWait()

            except:  # speech_recognition.UnknownValueError
                recognizer = speech_recognition.Recognizer()
                # speaker.say("I did not understand you!, Please try again")
                speaker.say("Je n'ai pas compris! S'il vous plait recommencez.")
                speaker.runAndWait()

    quit()


def add_todo():
    global recognizer
    global speaker

    # speaker.say("What to_do do you want to add?")
    speaker.say("Quel élément voulez-vous ajouter à la todo liste?")
    speaker.runAndWait()

    done = False

    while not done:
        with speech_recognition.Microphone() as mic:

            recognizer.adjust_for_ambient_noise(mic, duration=1)
            # print("Say something:")
            print("Dites quelque chose (ajout todo liste):")
            speaker.say("Je vous écoute pour l'ajout d'un élément à la todo liste")
            speaker.runAndWait()
            audio = recognizer.listen(mic)

            try:
                item = recognizer.recognize_google(audio, language='fr-FR')
                item = item.lower()
                print(item)

                if 'stop' in item or 'quitter' in item or 'fin' in item:
                    return None

                todo_list.append(item)
                done = True

                speaker.say(f"J'ai ajouté {item} à la todo liste avec succès")
                speaker.runAndWait()

            except:
                recognizer = speech_recognition.Recognizer()
                # speaker.say("I did not understand you! Please try again")
                speaker.say("Je n'ai pas compris! S'il vous plaît recommencez.")
                speaker.runAndWait()


def show_todos():
    speaker.say("Les éléments de votre todo liste sont les suivants")

    for item in todo_list:
        print(item)
        speaker.say(item)
        speaker.runAndWait()

    speaker.say("Fin de la todo liste")
    speaker.runAndWait()


mappings = {
    "greeting": hello,
    "create_note": create_note,
    "add_todo": add_todo,
    "show_todos": show_todos,
    "exit": quit
}

assistant = GenericAssistant('intents copie.json', intent_methods=mappings)
assistant.train_model()
# assistant.save_model()
# assistant.load_model()


while True:

    with speech_recognition.Microphone() as mic:

        recognizer.adjust_for_ambient_noise(mic, duration=1)
        print("Dites quelque chose:\n")
        audio = recognizer.listen(mic)

        try:

            message = recognizer.recognize_google(audio, language='fr-FR')
            message = message.lower()
            print("J'ai compris:\n" + message.upper() + "\n")
            assistant.request(message)

        except speech_recognition.UnknownValueError:

            print("Je ne comprend pas, veuillez recommencer.")
            recognizer = speech_recognition.Recognizer()

