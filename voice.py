from gtts import gTTS
from playsound import playsound
import uuid
import re
import os
import threading

# 🎯 GLOBAL CONTROL
CURRENT_AUDIO = None


# 🧼 CLEAN TEXT (FIXED FOR MULTILINGUAL)
def clean_text(text):
    text = re.sub(r'[#*`]', '', text)  # remove markdown only
    text = text.replace("\n", ". ")
    return text.strip()


# 🌍 LANGUAGE AUTO DETECT (simple)
def detect_lang(text):
    if any(ch in text for ch in "अआइईउऊएऐओऔ"):
        return "hi"
    elif any(ch in text for ch in "ಅಆಇಈಉಊಎಏಐಒಓ"):
        return "kn"
    else:
        return "en"


# 🔊 PLAY AUDIO THREAD (NON-BLOCKING)
def _play_audio(file):
    global CURRENT_AUDIO
    CURRENT_AUDIO = file

    try:
        playsound(file)
    except:
        pass

    # cleanup
    try:
        if os.path.exists(file):
            os.remove(file)
    except:
        pass

    CURRENT_AUDIO = None


# 🔊 MAIN SPEAK FUNCTION
def speak(text, lang=None):
    try:
        text = clean_text(text)

        # auto detect language if not passed
        if not lang:
            lang = detect_lang(text)

        filename = f"voice_{uuid.uuid4().hex}.mp3"

        tts = gTTS(
            text=text,
            lang=lang,
            slow=False   # 🔥 faster, more natural
        )

        tts.save(filename)

        # 🔥 play in thread (NO UI FREEZE)
        thread = threading.Thread(target=_play_audio, args=(filename,))
        thread.start()

    except Exception as e:
        print("🔊 Voice error:", e)


# ⛔ STOP VOICE
def stop_voice():
    global CURRENT_AUDIO

    try:
        if CURRENT_AUDIO and os.path.exists(CURRENT_AUDIO):
            os.remove(CURRENT_AUDIO)
            CURRENT_AUDIO = None
    except:
        pass