import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "core"))

import json
import time
from core.brain import smart_answer
from voice import speak, stop_voice
from agents.planner import plan_task
from agents.executor import execute_task
from agents.memory_agents import update_memory

VOICE_ENABLED = False
last_suggestions = []


# 🎨 COLORS
def color(text, code):
    return f"\033[{code}m{text}\033[0m"


# ✨ Typing Effect
def typing_effect(text):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(0.008)
    print()


# ⏳ Loading Animation
def loading(msg):
    for i in range(3):
        print(color(msg + "." * (i+1), 34), end="\r")
        time.sleep(0.25)
    print(" " * 50, end="\r")


# 🌍 Language Detection
def detect_language(text):
    text = text.lower()

    hindi_words = ["क्या", "कैसे", "है", "kaise", "kya", "hai"]
    kannada_words = ["ಏನು", "ಹೇಗೆ", "ಇದು"]

    if any(word in text for word in hindi_words):
        return "hi"
    elif any(word in text for word in kannada_words):
        return "kn"
    return "en"


# 🧠 INTENT DETECTION (FINAL FIXED)
def detect_intent(text):
    text = text.lower().strip()

    greetings = ["hi", "hello", "hey", "namaste", "namaskar"]

    small_talk = [
        "how are you", "who are you", "what can you do",
        "kaise ho", "kaise ho tum", "kya karte ho",
        "tum kya kar sakte ho", "tum kaun ho"
    ]

    emotions = [
        "i am sad", "i am tired", "i am happy",
        "main sad hoon", "main thak gaya", "main khush hoon"
    ]

    # 🔥 FULL FIX (added weather + temperature)
    farming_keywords = [
        "crop", "price", "weather", "temperature", "rain",
        "fertilizer", "soil", "mandi",
        "tomato", "wheat", "rice", "onion", "potato"
    ]

    if text in greetings:
        return "greeting"

    if any(x in text for x in small_talk):
        return "smalltalk"

    if any(x in text for x in emotions):
        return "emotion"

    if any(x in text for x in farming_keywords):
        return "farming"

    if len(text) < 3:
        return "invalid"

    return "chat"


# 💡 Suggestions Engine
def generate_suggestions(user_input):
    text = user_input.lower()

    if "tomato" in text:
        return [
            "What fertilizer for tomato?",
            "How to increase tomato yield?",
            "Common tomato diseases?"
        ]
    elif "wheat" in text:
        return [
            "Best season for wheat?",
            "Wheat market price?",
            "Fertilizer for wheat?"
        ]
    elif "price" in text:
        return [
            "Which crop gives highest profit?",
            "Market demand crops?",
            "Best crop to sell now?"
        ]
    else:
        return [
            "What crop should I grow?",
            "How to improve yield?",
            "Modern farming techniques?"
        ]


# 📜 History
def save_history(user, response):
    try:
        with open("history.json", "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append({"user": user, "response": response})

    with open("history.json", "w") as f:
        json.dump(data, f, indent=2)


def show_history():
    try:
        with open("history.json", "r") as f:
            data = json.load(f)
            print(color("\n📜 Task History:\n", 36))
            for item in data[-5:]:
                print(color(f"👨‍🌾 {item['user']}", 33))
                print(color(f"🤖 {item['response']}\n", 32))
    except:
        print("No history yet")


# 🧠 Smart Formatter
def format_response(raw, user_input):
    raw_lower = raw.lower()

    if "weather" in raw_lower:
        return raw

    if "advice:" in raw_lower:
        return raw

    if "price" in user_input.lower():
        extra = "💰 Sell when demand is high."
    elif "weather" in user_input.lower() or "temperature" in user_input.lower():
        extra = "🌦 Plan irrigation accordingly."
    else:
        extra = "🌱 Smart farming improves yield."

    return f"""
🌱 Advice:
{raw.strip()}

{extra}

📊 Confidence:
High
"""


# 🚀 MAIN SYSTEM
def run():
    global VOICE_ENABLED, last_suggestions

    print("""
🌾══════════════════════════════════════🌾
     KRISHIMITRA AI - FARM ASSISTANT
🌾══════════════════════════════════════🌾
""")

    print(color("🙏 Namaste! I am your KrishiMitra AI 🌾", 32))
    print(color("I can talk with you AND help in farming 😊\n", 36))

    while True:
        user_input = input(color("👨‍🌾 Ask: ", 33)).strip()

        if not user_input:
            continue

        # 🔢 Suggestion Selection
        if user_input.isdigit():
            try:
                idx = int(user_input) - 1
                if 0 <= idx < len(last_suggestions):
                    user_input = last_suggestions[idx]
                    print(color(f"👉 Selected: {user_input}", 36))
            except:
                pass

        # 🎤 Controls
        if user_input.lower() == "stop":
            stop_voice()
            print(color("🔇 Voice stopped", 31))
            continue

        if user_input.lower() == "voice on":
            VOICE_ENABLED = True
            print(color("🔊 Voice Enabled", 32))
            continue

        if user_input.lower() == "voice off":
            VOICE_ENABLED = False
            print(color("🔇 Voice Disabled", 31))
            continue

        if user_input.lower() == "exit":
            break

        if user_input.lower() == "history":
            show_history()
            continue

        if user_input.lower() == "demo":
            print(color("\n🚀 Running Demo...\n", 32))
            user_input = "Best crop in Karnataka"

        # 🔥 FORCE FARMING FOR CRITICAL QUERIES (ULTIMATE FIX)
        if any(word in user_input.lower() for word in ["weather", "temperature", "price", "rain"]):
            intent = "farming"
        else:
            intent = detect_intent(user_input)

        lang = detect_language(user_input)

        # 👋 GREETING
        if intent == "greeting":
            response = "🙏 Namaste! Aap kaise ho? Main aapki madad ke liye yahan hoon 😊"
            typing_effect(color("\n🤖 ", 32) + response)
            if VOICE_ENABLED:
                speak(response, lang="hi")
            continue

        # 💬 SMALL TALK
        if intent == "smalltalk":
            response = "🌾 Main KrishiMitra AI hoon. Main farming ke saath-saath aapse baat bhi kar sakta hoon 😊"
            typing_effect(color("\n🤖 ", 32) + response)
            if VOICE_ENABLED:
                speak(response, lang="hi")
            continue

        # ❤️ EMOTION
        if intent == "emotion":
            response = "💛 Tension mat lo, sab theek ho jayega. Main hoon na aapke saath 😊"
            typing_effect(color("\n🤖 ", 32) + response)
            if VOICE_ENABLED:
                speak(response, lang="hi")
            continue

        # 💬 NORMAL CHAT
        if intent == "chat":
            response = "😊 Achha laga aapse baat karke! Aap farming ke baare mein bhi pooch sakte ho."
            typing_effect(color("\n🤖 ", 32) + response)
            continue

        # ❌ INVALID
        if intent == "invalid":
            response = "⚠️ Please ask a proper question."
            typing_effect(color("\n🤖 ", 32) + response)
            continue

        # 🌾 FARMING MODE
        loading("🔍 Understanding")

        decision = smart_answer(user_input)

        if isinstance(decision, dict) and decision.get("type") in ["data", "web"]:
            raw = decision.get("response", "No data found")
        else:
            loading("🧠 Thinking")
            plan = plan_task(user_input)

            loading("⚙️ Executing")
            raw = execute_task(plan, user_input)

        result = format_response(raw, user_input)

        typing_effect(color("\n🤖 ", 32) + result)

        last_suggestions = generate_suggestions(user_input)

        print(color("\n💡 Suggested Questions:", 36))
        for i, s in enumerate(last_suggestions, 1):
            print(f"{i}. {s}")

        if VOICE_ENABLED:
            speak(raw, lang=lang)

        update_memory("last_task", user_input)
        save_history(user_input, raw)


if __name__ == "__main__":
    run()