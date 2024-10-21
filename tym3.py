import speech_recognition as sr
import pyttsx3
import pywhatkit
import random
import sqlite3
import re

name = "tim"
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Lista corregida
playlist = ["Manda una señal", "De pies a cabeza", "Corazón espinado", "Ángel de amor", 
            "Labios compartidos", "¿Dónde jugarán los niños?", "Vivir sin aire", 
            "Bendita tu luz", "Mariposa Traicionera", "Se me olvidó otra vez", 
            "El rey maná", "Te lloré un río", "Huele a tristeza", "Eres mi religión", 
            "Me vale", "En el muelle de san blas", "Clavado en un bar", "Rayando el sol", 
            "How can it be now?", "Knee Socks", "Santana - La Flaca ft. Juanes"]

maná = ["Manda una señal", "De pies a cabeza", "Corazón espinado", "Ángel de amor", 
        "Labios compartidos", "¿Dónde jugarán los niños?", "Vivir sin aire", 
        "Bendita tu luz", "Mariposa Traicionera", "Se me olvidó otra vez", 
        "El rey maná", "Te lloré un río", "Huele a tristeza", "Eres mi religión", 
        "Me vale", "En el muelle de san blas", "Clavado en un bar", "Rayando el sol"]

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

# Función para crear la conexión con SQLite
def create_connection():
    try:
        conn = sqlite3.connect('canciones.db')  # Crea o conecta la base de datos
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

# Función para crear la tabla si no existe
def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS canciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                categoria TEXT NOT NULL
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creando la tabla: {e}")

# Función para insertar una canción en la base de datos
def insert_song(conn, nombre, categoria):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO canciones (nombre, categoria) VALUES (?, ?)", (nombre, categoria))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error insertando la canción: {e}")

# Verificar si el video de YouTube es válido (opcional: podría necesitarse una API de YouTube)
def is_valid_youtube_url(url):
    # Un patrón de regex básico para verificar si el enlace es un video de YouTube
    regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+')
    if regex.match(url):
        return True
    return False

# Función para reproducir una canción con verificación
def play_song(song_name):
    print("Buscando y reproduciendo: " + song_name)
    talk("Reproduciendo " + song_name)
    try:
        pywhatkit.playonyt(song_name)  # Reproduce directamente en YouTube
    except Exception as e:
        print(f"Error al intentar reproducir la canción: {e}")
        talk("Hubo un error al intentar reproducir la canción.")

# Función principal para ejecutar TIM
def run_tym():
    conn = create_connection()
    if conn is not None:
        create_table(conn)
    else:
        print("No se pudo conectar a la base de datos.")
        return
    
    print("Hola soy TYM")
    print("Esperando tus instrucciones...")
    talk("Hola soy TIM. ¿En qué puedo ayudarte?")
    while True:
        rec = listen()
        if rec:
            if "reproduce" in rec:
                music = rec.replace('reproduce', '').strip()
                play_song(music)
                insert_song(conn, music, 'playlist')  # Guarda la canción reproducida en la base de datos
            elif "pon cualquier cosa" in rec:
                if len(playlist) > 0:
                    random_song = random.choice(playlist)
                    play_song(random_song)
                    insert_song(conn, random_song, 'playlist')  # Guarda la canción en la base de datos
            elif "maná" in rec:
                if len(maná) > 0:
                    random_song = random.choice(maná)
                    play_song(random_song)
                    insert_song(conn, random_song, 'maná')  # Guarda la canción en la base de datos
            else:
                print("Lo siento, no entendí. ¿Puedes repetirlo?")
        else:
            print("No se recibió ninguna instrucción.")

# Ejecución del programa
if __name__ == "__main__":
    run_tym()
