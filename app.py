from flask import Flask, jsonify, request
from flask_cors import CORS
from textblob import TextBlob
from deep_translator import GoogleTranslator
import random

app = Flask(__name__)
# A MUDANÇA ESTÁ AQUI: Abrindo o CORS para qualquer origem
CORS(app)

ultima_resposta_ia = ""

# O resto do código continua exatamente igual...
respostas = {
    "muito_positivo": ["Que notícia fantástica! Fico radiante por você.", "Isso é absolutamente incrível!", "Maravilhoso! Continue com essa energia!"],
    "positivo": ["Fico feliz em ouvir isso. O que te deixou com esse sentimento bom?", "Isso é ótimo. Parece que você está em um bom caminho.", "Boas notícias! O que podemos fazer para manter essa sensação?"],
    "neutro": ["Entendido. E como você se sente sobre isso?", "Ok, informação recebida. Existe algum sentimento associado a isso?", "Anotado. Quer explorar mais esse pensamento?"],
    "negativo": ["Puxa, que chato. Sinto muito por isso.", "Isso parece difícil. Lembre-se de ser gentil consigo mesmo.", "Lamento ouvir isso. Estou aqui se quiser desabafar."],
    "muito_negativo": ["Isso soa muito pesado. Por favor, cuide-se. Lembre-se que sentimentos são temporários.", "Sinto muito que esteja passando por isso.", "É válido se sentir assim. Quer me contar mais sobre a situação?"],
    "saudacao": ["Olá! Como você está se sentindo hoje?", "Oi! Sobre o que vamos conversar?", "E aí! Me conte o que está na sua mente."],
    "identidade": ["Eu sou uma IA conversacional criada para explorar sentimentos.", "Pode me chamar de seu confidente digital. Eu analiso emoções."],
    "clarificacao": ["Eu quis dizer que processei sua última mensagem. Minhas respostas são baseadas no sentimento que eu detecto.", "Minha resposta anterior foi baseada na emoção que senti nas suas palavras.", "Como uma IA, eu 'entendo' analisando os padrões no texto."]
}

@app.route('/')
def index():
    return jsonify({"message": "Servidor do Chatbot está online."})

@app.route('/chat', methods=['POST'])
def conversar():
    global ultima_resposta_ia
    dados = request.get_json()
    texto_usuario = dados.get('texto', '').lower().strip()

    if not texto_usuario:
        resposta_ia = "Estou ouvindo..."
        ultima_resposta_ia = resposta_ia
        return jsonify({"resposta": resposta_ia})

    palavras_clarificacao = ["?", "oque?", "entendeu oque?", "como assim?", "como?", "por que?"]
    if texto_usuario in palavras_clarificacao:
        resposta_ia = random.choice(respostas["clarificacao"])
        ultima_resposta_ia = resposta_ia
        return jsonify({"resposta": resposta_ia})
        
    if any(saudacao in texto_usuario for saudacao in ["oi", "olá", "e aí"]):
        resposta_ia = random.choice(respostas["saudacao"])
        ultima_resposta_ia = resposta_ia
        return jsonify({"resposta": resposta_ia})
    
    if any(pergunta in texto_usuario for pergunta in ["quem é você", "o que você faz", "qual seu propósito"]):
        resposta_ia = random.choice(respostas["identidade"])
        ultima_resposta_ia = resposta_ia
        return jsonify({"resposta": resposta_ia})

    try:
        texto_em_ingles = GoogleTranslator(source='pt', target='en').translate(texto_usuario)
        blob = TextBlob(texto_em_ingles)
        polaridade = blob.sentiment.polarity
    except Exception as e:
        print(f"Erro na tradução ou análise: {e}")
        polaridade = 0

    categoria_sentimento = "neutro"
    if "quero" in texto_usuario or "queria" in texto_usuario:
        categoria_sentimento = "neutro"
    elif polaridade > 0.5: categoria_sentimento = "muito_positivo"
    elif polaridade > 0.2: categoria_sentimento = "positivo"
    elif polaridade < -0.5: categoria_sentimento = "muito_negativo"
    elif polaridade < -0.2: categoria_sentimento = "negativo"
    
    resposta_ia = random.choice(respostas[categoria_sentimento])
    ultima_resposta_ia = resposta_ia
    return jsonify({"resposta": resposta_ia})
