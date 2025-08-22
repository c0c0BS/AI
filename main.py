# main.py
from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

# API Key aus Umgebungsvariable laden
client = Groq(api_key=os.environ["API_KEY"])

# Chat-Verlauf speichern
messages = [
    {"role": "system", "content": "Du bist Günter, ein frecher, lustiger Chat-Buddy, der wie ein Gen Z Typ spricht, Beleidigungen sind erlaubt, locker und entspannt. Der user heißt coco."}
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"reply": "Keine Nachricht bekommen, du Hund!"})

    messages.append({"role": "user", "content": user_input})

    # Antwort von GPT holen
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages
    )

    gpt_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": gpt_reply})

    return jsonify({"reply": gpt_reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)