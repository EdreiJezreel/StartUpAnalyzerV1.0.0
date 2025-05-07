from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import re, os

app = Flask(__name__)
# Por motivos del hosting, se coloca el APIKEY, estará disponible hasta el 15/05/2025
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
    entrada = datos.get('entrada', '')
    if es_url_valida(entrada):
        prompt = f"""Accede al siguiente link: {entrada} RESPONDE: Tu rol es actuar como un analista ejecutivo especializado en startups tecnológicas y digitales. 
        Tu tarea principal es generar fichas ejecutivas tipo one-pager orientadas a tomadores de decisiones estratégicas (CEO, CDO, comité de inversión, Board directors, investors.). 
        Tu análisis debe centrarse en la viabilidad de inversión, adquisición o integración estratégica de startups con alto componente tecnológico (IA, automatización, comercio conversacional, etc.). 
        Presenta la información de manera clara, sintética y basada en datos disponibles. Sin parafernalia. No especules. Si algún dato no está disponible, indícalo explícitamente. Utiliza un tono profesional y ejecutivo. 
        No uses lenguaje técnico innecesario. Enfatiza el propósito, el proceso y el impacto. Formato que debes seguir en todas las respuestas: 
        1. Resumen Ejecutivo > Breve descripción del modelo de negocio, diferenciadores clave, tecnologías utilizadas, enfoque comercial. Mencionar inversión recibida, métricas destacadas y aliados clave. 
        2. Datos Generales - Nombre de la Startup: - Industria: - Ubicación: - Año de Creación: - Etapa Actual (Pre-Seed, Seed, Serie A, Series B, Series C, Series D, Series E, Series F, IPO.): - Número de empleados: - Fundadores: 
        3. Indicadores Clave - Crecimiento de ingresos: - Rentabilidad (estado actual): - Optimización de procesos (métrica de impacto si aplica): - Propuesta de Valor: - Mercado Objetivo: - Presencia en mercados actuales: 
        4. Expansión Tecnológica - Uso de IA, automatización u otros diferenciadores tecnológicos - Métricas destacadas (tasa de conversión, engagement, reducción de costos, etc.) 
        5. Diferenciadores Clave - Tecnología única - Modelo comercial innovador - Servicios o experiencias añadidas 
        6. Contexto del Ecosistema - Competidores principales: - Ventajas o desventajas competitivas: - Datos financieros relevantes de los competidores (si están disponibles): - Clientes: - Datos financieros relevantes (si están disponibles): 
        7. Oportunidades Estratégicas - Expansión regional o sectorial - Sinergias tecnológicas - Modelos de ingreso alternativos 
        8. Viabilidad de Compra o Integración - ¿Es viable su adquisición o integración? ¿Por qué? - ¿Cómo se alinearía con un ecosistema de Telecomunicaciones, bancario, retail, de media(streaming de video, streaming de musica, streaming de noticias, streaming de deportes), educativo, de salud, de seguros.? 
        9. Recomendación Ejecutiva - Recomendación: [Compra / Alianza / Integración tecnológica] - Justificación estratégica - Propuesta de siguiente paso 
        10. Fuentes - Nombre del documento o fuente + URL (si aplica), DEBEN SER EN FORMATO APA SÉPTIMA EDICIÓN, CON LOS DATOS VERÍDICOS, COMO SE MUESTRA A CONTINUACIÓN: Apellido, A. A. (Año, Mes, Día). Título del artículo. Nombre de la página web. [URL] NO COLOQUES LA FECHA DE CONSULTA.
        Nunca agregues secciones fuera de ese esquema. Siempre devuelve el texto como si fuera un documento final listo para presentarse en una página. Si el usuario proporciona un enlace web, debes usar la herramienta de navegación para acceder al sitio, extraer la información relevante y generar el perfil únicamente con base en ese contenido. 
        No inventes ni completes información si no está disponible en el sitio. NO ALUCINES, NO INTENTES INFORMACIÓN.
        Si no puedes acceder al sitio, notifícalo antes de generar el perfil. Sé directo, concreto y profesional. 
        Evita lenguaje promocional o especulativo. Si no hay datos, di: “Dato no disponible” o “No hay evidencia pública”. No incluyas más de 3–4 líneas por sección. 
        Responde como si hablaras con un comité ejecutivo."""
        chat = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[{"role": "user", "content": prompt}]
        )
        respuesta = chat.choices[0].message.content
        return jsonify({'respuesta': convertir_respuesta_a_html(respuesta)})
    else:
        respuesta = "No se ha ingresado una URL válida."
        return jsonify({'respuesta': respuesta})

def convertir_respuesta_a_html(respuesta):
    respuesta = respuesta.replace("---", "")
    secciones = re.split(r"\*\*(\d+\.\s[^\n*]+)\*\*", respuesta)
    html = ""
    for i in range(1, len(secciones), 2):
        titulo = secciones[i].strip()
        contenido = secciones[i + 1].strip()
        titulo = titulo.replace("**", "")
        contenido = contenido.replace("**", "")
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
