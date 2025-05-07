from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import re, os

app = Flask(__name__)

# API KEY válida hasta el 15/05/2025
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
    #,base_url="https://openrouter.ai/api/v1"
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
   ''' prompt = f"""Accede al siguiente link: {entrada} RESPONDE: Tu rol es actuar como un analista ejecutivo especializado en startups tecnológicas y digitales. 
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
        Responde como si hablaras con un comité ejecutivo.""" '''
        prompt = f"""
                NO ACCEDAS AL LINK. NO INTENTES ACCEDER A INTERNET. NO GENERES CONTENIDO INVENTADO.
    
                ACTÚA ÚNICAMENTE COMO ANALISTA EJECUTIVO ESPECIALIZADO EN STARTUPS TECNOLÓGICAS.
    
                Contexto: Se te proporciona este enlace solo como referencia del contenido sobre una empresa: {entrada}. El contenido ya fue extraído y será procesado por ti.
    
                Instrucciones:
                - Devuelve ÚNICAMENTE un documento en FORMATO HTML. No uses texto plano ni explicaciones fuera del esquema solicitado.
                - NO accedas a Internet ni intentes inferir datos que no estén explícitamente disponibles.
                - Si no hay datos disponibles, responde con “Dato no disponible” o “No hay evidencia pública”.
                - No incluyas secciones adicionales. No uses frases como “como modelo de lenguaje”.
                - Sé concreto, ejecutivo y profesional. No utilices un tono promocional, técnico innecesario o especulativo.
                - No repitas instrucciones. Solo genera la ficha ejecutiva directamente.
                - Como fuente coloca  el link proporcionado en formato APA SEPTIMA EDICION y completa con los datos más apegados con el formato APA
    
                Formato ESTRICTO de la respuesta (en etiquetas HTML adecuadas como <h2>, <ul>, <ol>, <p>, <strong>, etc.):
    
                <h2>1. Resumen Ejecutivo</h2>
                <p>Breve descripción del modelo de negocio, diferenciadores clave, tecnologías utilizadas, enfoque comercial. Incluir inversión recibida, métricas destacadas y aliados clave.</p>
    
                <h2>2. Datos Generales</h2>
                <ul>
                <li><strong>Nombre de la Startup:</strong> ...</li>
                <li><strong>Industria:</strong> ...</li>
                <li><strong>Ubicación:</strong> ...</li>
                <li><strong>Año de Creación:</strong> ...</li>
                <li><strong>Etapa Actual:</strong> ...</li>
                <li><strong>Número de empleados:</strong> ...</li>
                <li><strong>Fundadores:</strong> ...</li>
                </ul>
    
                <h2>3. Indicadores Clave</h2>
                <ul>
                <li><strong>Crecimiento de ingresos:</strong> ...</li>
                <li><strong>Rentabilidad:</strong> ...</li>
                <li><strong>Optimización de procesos:</strong> ...</li>
                <li><strong>Propuesta de Valor:</strong> ...</li>
                <li><strong>Mercado Objetivo:</strong> ...</li>
                <li><strong>Presencia en mercados actuales:</strong> ...</li>
                </ul>
    
                <h2>4. Expansión Tecnológica</h2>
                <ul>
                <li><strong>Uso de IA u otras tecnologías:</strong> ...</li>
                <li><strong>Métricas destacadas:</strong> ...</li>
                </ul>
    
                <h2>5. Diferenciadores Clave</h2>
                <ul>
                <li><strong>Tecnología única:</strong> ...</li>
                <li><strong>Modelo comercial innovador:</strong> ...</li>
                <li><strong>Servicios o experiencias añadidas:</strong> ...</li>
                </ul>
    
                <h2>6. Contexto del Ecosistema</h2>
                <ul>
                <li><strong>Competidores principales:</strong> ...</li>
                <li><strong>Ventajas o desventajas competitivas:</strong> ...</li>
                <li><strong>Datos financieros de competidores:</strong> ...</li>
                <li><strong>Clientes:</strong> ...</li>
                <li><strong>Datos financieros relevantes:</strong> ...</li>
                </ul>
    
                <h2>7. Oportunidades Estratégicas</h2>
                <ul>
                <li><strong>Expansión regional o sectorial:</strong> ...</li>
                <li><strong>Sinergias tecnológicas:</strong> ...</li>
                <li><strong>Modelos de ingreso alternativos:</strong> ...</li>
                </ul>
    
                <h2>8. Viabilidad de Compra o Integración</h2>
                <ul>
                <li><strong>¿Es viable su adquisición o integración? ¿Por qué?</strong> ...</li>
                <li><strong>Alineación con ecosistemas (Telecom, Bancario, Retail, Media, Educación, Salud, Seguros):</strong> ...</li>
                </ul>
    
                <h2>9. Recomendación Ejecutiva</h2>
                <ul>
                <li><strong>Recomendación:</strong> [Compra / Alianza / Integración tecnológica]</li>
                <li><strong>Justificación estratégica:</strong> ...</li>
                <li><strong>Propuesta de siguiente paso:</strong> ...</li>
                </ul>
    
                <h2>10. Fuentes</h2>
                <ul> 
                <li>Apellido, A. A. (Año, Mes Día). <em>Título del artículo</em>. Nombre del sitio. [URL]</li>
                </ul>
    
                Devuelve solo este bloque de HTML. Nada más.
                """

    try:
        chat = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[{"role": "user", "content": prompt}]
        )
        respuesta = chat.choices[0].message.content
    except Exception as e:
        print("Error al generar respuesta del modelo:", e)
        print(respuesta)
        return jsonify({'respuesta': 'Error al generar el análisis con el modelo.'}), 500

    try:
        respuesta_html = respuesta
    except Exception as e:
        print("Error al convertir la respuesta a HTML:", e)
        return jsonify({'respuesta': 'Se generó el análisis, pero hubo un error al procesarlo.'}), 500
    return jsonify({'respuesta': respuesta_html})

'''def convertir_respuesta_a_html(respuesta):
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
    return html'''

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
