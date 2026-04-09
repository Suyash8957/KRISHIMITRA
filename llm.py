import subprocess
import time

# 🔥 MODELS
PRIMARY_MODEL = "qwen2.5-coder:7b"
FALLBACK_MODEL = "phi3:mini"


# 🧹 CLEAN OUTPUT
def clean_output(text):
    return (
        text.replace("```", "")
        .replace("**", "")
        .replace("#", "")
        .strip()
    )


# ⚡ RUN MODEL
def run_model(model, prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="ignore",
            timeout=35
        )

        output = result.stdout.strip()

        # ❌ Empty / bad output
        if not output or len(output) < 5:
            return None

        return clean_output(output)

    except subprocess.TimeoutExpired:
        print(f"⏳ Timeout from {model}")
        return None

    except Exception as e:
        print(f"❌ Error running {model}: {e}")
        return None


# 🧠 MAIN LLM FUNCTION
def ask_llm(prompt):

    # ⚡ 1. TRY PRIMARY MODEL
    output = run_model(PRIMARY_MODEL, prompt)
    if output:
        return output

    # 🔁 2. RETRY ONCE (handles temporary lag)
    time.sleep(1)
    output = run_model(PRIMARY_MODEL, prompt)
    if output:
        return output

    # 🛟 3. FALLBACK MODEL
    output = run_model(FALLBACK_MODEL, prompt)
    if output:
        return output

    # ❌ FINAL FAILURE RESPONSE
    return """🌱 Advice:
AI is currently busy.

💡 Tip:
Try again in a few seconds.

📊 Confidence:
Low"""