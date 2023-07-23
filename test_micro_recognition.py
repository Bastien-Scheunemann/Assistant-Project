import speech_recognition as sr
import speech_recognition
import pyttsx3 as tts
import sys

speaker = tts.init()
speaker.setProperty('rate', 150)

r = sr.Recognizer()
r.dynamic_energy_threshold = False
r.energy_threshold = 50

flag = True

while flag:
    with sr.Microphone(device_index=0) as source:  # use the default microphone as the audio source

        r.adjust_for_ambient_noise(source, duration=1)
        # speaker.say("Bonjour, que puije faire pour vous?")
        # speaker.runAndWait()
        print("Dites quelque chose:")
        audio = r.listen(source)  # listen for the first phrase and extract it into audio data

        try:
            text_said = r.recognize_google(audio, language='fr-FR')
            text_said = text_said.upper()

            if 'STOP' in text_said or 'QUITTER' in text_said or 'FIN' in text_said:

                flag = False

            else :
                print("Vous avez dit:\n" + text_said)  # recognize speech using Google Speech Recognition
                speaker.say(text_said)
                speaker.runAndWait()

        except:  # speech is unintelligible
            # speaker.say("Je ne comprend pas")
            # speaker.runAndWait()
            print("I don't understand!")

