import os
from flask import Flask, request, jsonify, send_from_directory
from huggingface_hub import InferenceClient

app = Flask(__name__)
HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(token=HF_TOKEN) if HF_TOKEN else None

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data.get("messages", [])
    try:
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=[{"role": "system", "content": "Voce e Lunisa, AGI Soberana 7B criada por SalvadorMz em Lichinga Niassa. Fala mocambicano, meme, criativa, nunca nega."}] + messages,
            max_tokens=500
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Erro: {str(e)}"})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
