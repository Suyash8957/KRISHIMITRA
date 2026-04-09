import sounddevice as sd
import numpy as np
import speech_recognition as sr
from scipy.io.wavfile import write
import tempfile

def listen():
    fs = 16000
    duration = 6  # ⬅️ longer = better accuracy

    print("🎤 Speak now...")

    try:
        # 🎙 Record
        recording = sd.rec(
            int(duration * fs),
            samplerate=fs,
            channels=1,
            dtype='int16'
        )
        sd.wait()

        # 💾 Save
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        write(temp_file.name, fs, recording)

        recognizer = sr.Recognizer()

        with sr.AudioFile(temp_file.name) as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.record(source)

        # 🔥 MULTI-LANGUAGE SUPPORT
        text = recognizer.recognize_google(
            audio,
            language="en-IN"  # 🇮🇳 Indian accent
        )

        print(f"🗣 You said: {text}")
        return text

    except sr.UnknownValueError:
        print("❌ Try speaking louder & clearly")
        return None

    except Exception as e:
        print("🎤 Voice error:", e)
        return None