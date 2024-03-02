import speech_recognition as sr
import pyttsx3
import pywhatkit
import random

name = "tim"
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

playlist = [
            "Manda una señal", 
            "De pies a cabeza", 
            "Corazón espinado", 
            "Ángel de amor", 
            "How can it be now?", 
            "Labios compartidos",
            "Knee Socks"
            "Santana - La Flaca ft. Juanes"
            ]

maná = [
        "Manda una señal", 
        "De pies a cabeza",
        "Corazón espinado",
        "Ángel de amor",
        "Labios compartidos",
        "¿Dónde jugarán los niños?",
        "Vivir sin aire",
        "Bendita tu luz",
        "Mariposa Traicionera"
        "Se me olvidó otra vez"
        "El rey maná"
        "Te lloré un río"
        "Huele a tristeza"
        "Eres mi religión"
        "Me vale"
        "En el muelle de san blas"
        "Clavado en un bar"
        "Rayando el sol"]

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            listener.adjust_for_ambient_noise(source)
            pc = listener.listen(source)
            rec = listener.recognize_google(pc, language="es-ES")
            rec = rec.lower()
            if name in rec:
                rec = rec.replace(name, '')
            return rec
    except:
        pass

def run_tym():
    print("Hola soy TYM")
    print("Esperando tus instrucciones...")
    talk("Hola soy TIM. ¿En qué puedo ayudarte?")
    while True:
        rec = listen()
        if rec:
            if "reproduce" in rec:
                music = rec.replace('reproduce', '').strip()
                print("Reproduciendo " + music)
                talk("Reproduciendo " + music)
                pywhatkit.playonyt(music)
            elif "pon cualquier cosa" in rec:
                if len(playlist) > 0:
                    random_song = random.choice(playlist)
                    print("Reproduciendo " + random_song)
                    talk("Reproduciendo " + random_song)
                    pywhatkit.playonyt(random_song)
            elif "maná" in rec:
                if len(maná) > 0:
                    random_song = random.choice(maná)
                    print("Reproduciendo " + random_song)
                    talk("Reproduciendo " + random_song)
                    pywhatkit.playonyt(random_song)
            else:
                print("Lo siento, no entendí. ¿Puedes repetirlo?")

def show_playlist():
    if len(playlist) > 0:
        print("Lista de canciones:")
        for index, song in enumerate(playlist, start=1):
            print(f"{index}. {song}")
    if len(maná) > 0:
        print("Lista maná:")
        for index, song in enumerate(maná, start=1):
            print(f"{index}. {song}")
    else:
        print("La lista de reproducción está vacía.")
    talk("La lista de canciones ha sido mostrada en la consola.")

if __name__ == "__main__":
    run_tym()
