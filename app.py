import streamlit as st
import threading
import time

from core.brain import smart_answer
from agents.planner import plan_task
from agents.executor import execute_task

from voice import speak, stop_voice
from voice_input import listen

st.set_page_config(page_title="KrishiMitra AI 🌾", layout="wide")

# 🧠 STATE
if "history" not in st.session_state:
    st.session_state.history = []

if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = False

if "loading" not in st.session_state:
    st.session_state.loading = False

# 🎨 STYLE
st.markdown("""
<style>
.chat-container {
    max-width: 900px;
    margin: auto;
}
</style>
""", unsafe_allow_html=True)

# 🎨 HEADER
st.title("🌾 KrishiMitra AI")
st.caption("India’s Smart Farming Assistant 🇮🇳")

# 🎛️ SIDEBAR
with st.sidebar:
    st.header("⚙️ Settings")

    st.session_state.voice_enabled = st.toggle("🔊 Voice Output")

    if st.button("⛔ Stop Voice"):
        stop_voice()

    if st.button("🗑 Clear Chat"):
        st.session_state.history = []
        st.rerun()

    st.markdown("---")
    st.markdown("💡 Try asking:")
    st.markdown("- Tomato price today")
    st.markdown("- Weather in Karnataka")
    st.markdown("- Best crop for summer")

# 💬 CHAT DISPLAY
for chat in st.session_state.history:
    with st.chat_message("user"):
        st.write(chat["user"])

    with st.chat_message("assistant"):
        st.write(chat["bot"])

# 🎤 VOICE INPUT
col1, col2 = st.columns([8, 1])

with col2:
    if st.button("🎤"):
        voice_text = listen()
        if voice_text:
            st.session_state.history.append({
                "user": voice_text,
                "bot": "⏳ Thinking..."
            })
            st.rerun()

# 🧠 INPUT
user_input = st.chat_input("Ask anything about farming...")

# 🔊 VOICE THREAD
def run_voice(text):
    if st.session_state.voice_enabled:
        speak(text, lang="hi")

# ✨ FORMAT (🔥 UPGRADED)
def format_response(text):
    lower = text.lower()

    if "price" in lower:
        extra = "💰 Sell when demand is high."
    elif "weather" in lower:
        extra = "🌦 Plan irrigation accordingly."
    else:
        extra = "🌱 Smart farming improves yield."

    return f"""
✅ **Answer:**
{text}

{extra}

💡 **Suggestions:**
• Ask about fertilizer  
• Ask about market price  
• Ask about weather  
"""

# 🚀 MAIN LOGIC
if user_input:
    st.session_state.history.append({
        "user": user_input,
        "bot": "⏳ Thinking..."
    })

    with st.chat_message("assistant"):
        placeholder = st.empty()

        # ⏳ LOADING
        for i in range(3):
            placeholder.markdown(f"⏳ Thinking{'.'*i}")
            time.sleep(0.3)

        try:
            # 🧠 BRAIN FIRST
            decision = smart_answer(user_input)

            if decision["type"] in ["data", "web"]:
                raw = decision["response"]
            else:
                plan = plan_task(user_input)
                raw = execute_task(plan, user_input)

        except Exception as e:
            raw = f"❌ Error: {str(e)}"

        result = format_response(raw)

        # ✨ TYPING EFFECT
        typed = ""
        for char in result:
            typed += char
            placeholder.markdown(typed)
            time.sleep(0.003)

    st.session_state.history[-1]["bot"] = result

    # 🔊 VOICE OUTPUT
    if st.session_state.voice_enabled:
        threading.Thread(target=run_voice, args=(raw,)).start()