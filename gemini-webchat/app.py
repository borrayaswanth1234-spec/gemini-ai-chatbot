import os
from flask import Flask, render_template, request, jsonify, session
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv("../notepad.env")

app = Flask(__name__)
app.secret_key = "gembot-secret-key"

API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
client  = genai.Client(api_key=API_KEY) if API_KEY else None

SYSTEM_PROMPT = "You are GemBot, a helpful AI assistant. Format replies in Markdown."
AVAILABLE_MODELS = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"]

@app.route("/")
def index():
    session.setdefault("history", [])
    return render_template("index.html", models=AVAILABLE_MODELS)

@app.route("/chat", methods=["POST"])
def chat():
    data     = request.json
    user_msg = data.get("message", "").strip()
    model    = data.get("model", "gemini-2.5-flash")
    if not user_msg: return jsonify({"error": "Empty"}), 400
    if not client:   return jsonify({"error": "Set your GEMINI_API_KEY in notepad.env"}), 500
    history = session.get("history", [])
    history.append({"role": "user", "parts": [{"text": user_msg}]})
    contents = [types.Content(role=m["role"], parts=[types.Part(text=m["parts"][0]["text"])]) for m in history]
    try:
        response  = client.models.generate_content(model=model, contents=contents,
                      config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, temperature=0.7, max_output_tokens=2048))
        bot_reply = response.text
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    history.append({"role": "model", "parts": [{"text": bot_reply}]})
    session["history"] = history
    return jsonify({"reply": bot_reply, "turns": len(history)//2, "model": model})

@app.route("/clear", methods=["POST"])
def clear():
    session["history"] = []
    return jsonify({"status": "cleared"})

@app.route("/set_key", methods=["POST"])
def set_key():
    global client
    key = request.json.get("key", "").strip()
    if not key: return jsonify({"error": "No key"}), 400
    client = genai.Client(api_key=key)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    print("🚀 Open http://localhost:5000")
    app.run(debug=True, port=5000)