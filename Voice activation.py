import speech_recognition as sr
import pyttsx3
from pynput.keyboard import Key, Controller

# Initialize recognizer, text-to-speech, and keyboard controller
recognizer = sr.Recognizer()
engine = pyttsx3.init()
keyboard = Controller()

# Commands map to keyboard actions
COMMANDS = {
    "jump": Key.space,
    "shoot": "f",
    "reload": "r",
    "pause": Key.esc,
    "run": "shift"
}

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_command():
    with sr.Microphone() as source:
        print("🎙️ Say a command (e.g., 'jump', 'shoot')...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"🗣️ You said: {command}")
        return command
    except sr.UnknownValueError:
        print("❌ Sorry, didn't catch that.")
    except sr.RequestError:
        print("❌ API unavailable.")
    return None

def perform_action(command):
    if command in COMMANDS:
        key = COMMANDS[command]
        print(f"🎮 Performing action: {command} -> {key}")
        speak(f"{command} activated")
        keyboard.press(key)
        keyboard.release(key)
    else:
        print("❗ Unknown command.")
        speak("Unknown command")

def main():
    speak("Voice game controller started.")
    while True:
        cmd = listen_command()
        if cmd == "exit" or cmd == "quit":
            speak("Exiting controller.")
            break
        if cmd:
            perform_action(cmd)

if __name__ == "__main__":
    main()
