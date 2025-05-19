import speech_recognition as sr
import os
import datetime

NOTES_DIR = "notes"

def ensure_notes_dir():
    if not os.path.exists(NOTES_DIR):
        os.makedirs(NOTES_DIR)

def save_note(text):
    ensure_notes_dir()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{NOTES_DIR}/note_{timestamp}.txt"
    with open(filename, "w") as f:
        f.write(text)
    print(f"[✓] Note saved as {filename}")

def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("🎙️ Please speak your note...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("📝 Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"> You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Sorry, I could not understand the audio.")
    except sr.RequestError:
        print("❌ Could not request results. Check your internet connection.")
    return None

def view_notes():
    ensure_notes_dir()
    notes = os.listdir(NOTES_DIR)
    if not notes:
        print("📭 No notes found.")
        return
    for note_file in notes:
        print(f"\n🗒️ {note_file}")
        with open(f"{NOTES_DIR}/{note_file}", "r") as f:
            print(f.read())

def main():
    while True:
        print("\n--- Speech-Based Notes & Memo System ---")
        print("1. Create a new note")
        print("2. View saved notes")
        print("3. Exit")
        choice = input("Select an option (1-3): ")

        if choice == "1":
            text = recognize_speech()
            if text:
                save_note(text)
        elif choice == "2":
            view_notes()
        elif choice == "3":
            print("👋 Exiting. Goodbye!")
            break
        else:
            print("❗ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
