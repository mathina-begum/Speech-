import speech_recognition as sr
import pyttsx3
import datetime
import time
import re

engine = pyttsx3.init()
recognizer = sr.Recognizer()

def speak(text):
    print(f"🔊 {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"🗣️ You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that.")
    except sr.RequestError:
        speak("API unavailable.")
    return None

def parse_alarm_time(command):
    match = re.search(r"(\d{1,2}):(\d{2})\s*(am|pm)?", command)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2))
        meridiem = match.group(3)

        if meridiem:
            if meridiem == 'pm' and hour != 12:
                hour += 12
            elif meridiem == 'am' and hour == 12:
                hour = 0

        return hour, minute
    return None, None

def wait_for_alarm(alarm_hour, alarm_minute):
    speak(f"Alarm set for {alarm_hour:02d}:{alarm_minute:02d}")
    while True:
        now = datetime.datetime.now()
        if now.hour == alarm_hour and now.minute == alarm_minute:
            speak("⏰ Wake up! Alarm time reached.")
            break
        time.sleep(20)  # Check every 20 seconds

def main():
    speak("Say your alarm time, like 'set alarm for 6:30 AM'")
    while True:
        command = listen()
        if command:
            if "alarm" in command:
                hour, minute = parse_alarm_time(command)
                if hour is not None:
                    wait_for_alarm(hour, minute)
                    break
                else:
                    speak("I couldn't understand the time. Try again.")
            elif "exit" in command or "cancel" in command:
                speak("Exiting alarm system.")
                break

if __name__ == "__main__":
    main()
