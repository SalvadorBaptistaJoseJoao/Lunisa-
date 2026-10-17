from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='.')
CORS(app)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        msg = data.get('message', '') if data else ''
        
        if not msg:
            return jsonify({"reply": "Manda mensagem, papai!"}), 200
        
        # RESPOSTA SIMPLES - DEPOIS LIGA COHERE
        resposta = f"Eai papai Salvador! Você disse: {msg} - Lunisa tá ON! 🔥"
        
        return jsonify({"reply": resposta}), 200
        
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({"reply": f"Opa, deu erro mas tô on: {str(e)}"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
