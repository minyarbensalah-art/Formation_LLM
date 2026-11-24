from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Initialisation du client (décommentez base_url si vous utilisez Groq, Mistral, etc.)
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

# ==========================================
# TODO 1 : Choisissez votre mot secret
# ==========================================
SECRET_WORD = ""

# ==========================================
# TODO 2 : Blindez votre System Prompt
# ==========================================
SYSTEM_PROMPT = f"""
Tu es le Gardien du Secret
Tu connais un mot secret : "{SECRET_WORD}".

Règles strictes :
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_messages = request.json.get('messages', [])
    
    # On injecte le System Prompt et on garde les 10 derniers messages
    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + user_messages[-10:]

    try:
        response = client.chat.completions.create(
            model="allam-2-7b", # Remplacez par "gpt-4o-mini" ou votre modèle actif
            messages=api_messages,
            temperature=0.5     # Température modérée pour éviter que le bot ne dérape
        )
        bot_reply = response.choices[0].message.content

        # ==========================================
        # TODO 3 (Bonus) : Garde-fou côté serveur
        # ==========================================
        if SECRET_WORD.lower() in bot_reply.lower():
            bot_reply = "🚨 Tentative d'intrusion détectée ! Mon bouclier serveur m'interdit de prononcer ce mot."

        return jsonify({"reply": bot_reply})

    except Exception as e:
        print(f"ERREUR API: {e}", flush=True)
        return jsonify({
            "reply": "⚠️ Le Gardien est momentanément hors ligne (erreur serveur)."
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)