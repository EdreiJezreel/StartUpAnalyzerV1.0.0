from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import re, os

app = Flask(__name__)

# API KEY válida hasta el 15/05/2025
client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

def es_url_valida(texto):
    patron = re.compile(r'^https?://[^\s]+$')
    return re.match(patron, texto)

@app.route('/')
def index():
    return render_template('paginaChat.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    datos = request.get_json()
    if not datos or 'entrada' not in datos:
        return jsonify({'respuesta': 'No se recibió una entrada válida.'}), 400

    entrada = datos['entrada']

    if not es_url_valida(entrada):
        return jsonify({'respuesta': 'No se ha ingresado una URL válida.'}), 400

    # Construcción del prompt
    prompt = f"""Accede al siguiente link: {entrada} RESPONDE: Tu rol es actuar como un analista ejecutivo especializado en startups tecnológicas y digitales..."""  # recortado aquí por claridad

    try:
        chat = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[{"role": "user", "content": prompt}]
        )
        respuesta = chat.choices[0].message.content
    except Exception as e:
        print("Error al generar respuesta del modelo:", e)
        return jsonify({'respuesta': 'Error al generar el análisis con el modelo.'}), 500

    try:
        respuesta_html = convertir_respuesta_a_html(respuesta)
    except Exception as e:
        print("Error al convertir la respuesta a HTML:", e)
        return jsonify({'respuesta': 'Se generó el análisis, pero hubo un error al procesarlo.'}), 500
    return jsonify({'respuesta': respuesta_html})

def convertir_respuesta_a_html(respuesta):
    respuesta = respuesta.replace("---", "")
    secciones = re.split(r"\*\*(\d+\.\s[^\n*]+)\*\*", respuesta)
    html = ""
    for i in range(1, len(secciones), 2):
        titulo = secciones[i].strip().replace("**", "")
        contenido = secciones[i + 1].strip().replace("**", "")
        contenido = re.sub(r"- ([^\n]+)", r"<li>\1</li>", contenido)
        if "<li>" in contenido:
            contenido = f"<ul>{contenido}</ul>"
        else:
            contenido = f"<p>{contenido}</p>"
        html += f"<section><h2>{titulo}</h2>{contenido}</section>\n"
    return html

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
