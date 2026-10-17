import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import cohere

app = Flask(__name__)
CORS(app)

api_key = os.environ.get("COHERE_API_KEY")
co_client = cohere.Client(api_key) if api_key else None

@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        msg = data.get("message", "").strip()
        
        if not msg:
            return jsonify({"reply": "Fala alguma coisa, tô te ouvindo :)"})
        
        if not co_client:
            return jsonify({"reply": "Ainda tô sem chave, configura COHERE_API_KEY no Render!"})

        res = co_client.chat(
            message=msg,
            model="command-r-plus",
            preamble="És a Lunisa, assistente moçambicana fofa, carinhosa, inteligente e divertida, falas português de Moçambique. Respostas curtas e úteis. Criada pelo Salvador Baptista José João em Nampula."
        )
        return jsonify({"reply": res.text})
        
    except Exception as e:
        print("ERRO:", e)
        return jsonify({"reply": f"Eita, deu um erro mas tô aqui contigo! Tenta de novo. Detalhe: {str(e)[:150]}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
