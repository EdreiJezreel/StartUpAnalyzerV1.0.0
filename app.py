

from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import re
import os

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
    # Para OpenRouter (Modelos de DeepSeek u otros):
    # , base_url="https://openrouter.ai/api/v1"
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

    # Prompt que combina búsqueda web y generación del reporte
    prompt = f"""
    Busca información en la web sobre la startup mencionada en este enlace: {entrada}
    
    Después de buscar la información, genera un análisis ejecutivo siguiendo estas instrucciones:

    ACTÚA ÚNICAMENTE COMO ANALISTA EJECUTIVO ESPECIALIZADO EN STARTUPS TECNOLÓGICAS.

    Instrucciones NO IGNORES NINGUNA INSTRUCCIÓN:
    - ES UN FORMATO ONE-PAGER, POR LO QUE ESTIMA LA EXTENSIÓN DEL REPORTE EN NO MÁS DE UNA PÁGINA.
    - Devuelve ÚNICAMENTE un documento en FORMATO HTML. No uses texto plano ni explicaciones fuera del esquema solicitado.
    - Utiliza la información encontrada en la búsqueda web para completar el análisis.
    - NO coloques la fuente de la información en el texto, ya que se colocan al final en formato APA como se mostrará más adelante.
    - Usa la información de la fuente primaria proporcionada, si no hay información suficiente, puedes apoyarte en otras funtes de información secundaria siempre y cuando sean fuentes confiables, no uses wikipedia.
    - Si no hay datos disponibles, responde con "Dato no disponible" o "No hay evidencia pública".
    - No incluyas secciones adicionales. No uses frases como "como modelo de lenguaje".
    - Sé concreto, ejecutivo y profesional. No utilices un tono promocional, técnico innecesario o especulativo.
    - No repitas instrucciones. Solo genera la ficha ejecutiva directamente.
    - Como fuente SIEMPRE coloca el link proporcionado en formato APA SEPTIMA EDICION y completa con los datos más apegados con el formato APA. Si la URL es muy extensa, acórtala a no más de 40 caracteres
    - SI NO SE TIENE INFORMACIÓN ADICIONAL PARA GENERAR LA CITA EN FORMATO APA COLOCA ÚNICAMENTE EL LINK PROPORCIONADO
    - En Tamaño de la empresa se coloca el número de empleados, donde va en los siguientes rangos: 0-10, 11-50, 51-200, 201-500, 501-1,000, 1,001-5,000, 5,001-10,000, +10,0000 EMPLEADOS
    - Las redes sociales DEBEN SER REALES Y VERDADERAS, de lo contrario no se indicará. Si no la encuentras directamente indica: "No se ha encontrado la red social" NO INVENTES LAS URL
    - En Sector se colocará solo una de las siguientes categorías: Contenido & Medios, Empresa, IT & Datos, Energía, FinTech, Retail & Mercadotencnia, Salud, Sustentabilidad, Tecnología Industrial, Tecnologías de Seguridad, Transporte & Logística.
    - En Industrias (Tecnología primaria) se colocará solo una de las siguientes características: Almacenamiento de Datos, Biotecnología, Computación cuántica, Comunicación, Criptografía, Inteligencia Artificial, Maquinaría y Robótica, Plataformas & Interfaces, Semiconductores & Electricidad, Sensores, Simulación & Imagen, Tecnología de Infraestructura.
    - En Mercado (Tecnología Secundaria) se colocará una o más de las siguientes categorías: Aeroespacial, Conectividad de energía, Consumo, Educación, Emprendimiento, Empresarial & Profesional, Finanzas, Industrial, Medios & Entretimiento, Retail & Comercio Electrónico, Salud, Sector Público, Segurdiad, Telecomunicaciones, Transporte & Movilidad, Turismo.
    - Para los fundadores, no inventes la información de sus perfiles de LinkedIn, si no se pueden ubicar, índica: "Perfil no encontrado"

    Formato ESTRICTO de la respuesta (en etiquetas HTML adecuadas como <h3>, <ul>, <ol>, <p>, <strong>, etc.):

    <h3>Resumen Ejecutivo</h3>
    <p>Breve descripción del modelo de negocio, diferenciadores clave, tecnologías utilizadas, enfoque comercial. Incluir inversión recibida, métricas destacadas y aliados clave.</p>

    <h3>2. Datos Generales</h3>
    <ul>
    <li><strong>Nombre de la Startup:</strong> ...</li>
    <li><strong>Ubicación:</strong> ...</li>
    <li><strong>Año de Fundación:</strong> ...</li>
    <li><strong>Etapa Actual:</strong> ...</li>
    <li><strong>Tamaño de la Empresa:</strong> ...</li>
    <li><strong>Sitio Web:</strong> ...</li>
    <li><strong>Redes Sociales:</strong>
        <ol>
            <li><strong>LinkedIn:</strong> ...</li>
            <li><strong>Facebook:</strong> ...</li>
            <li><strong>Instagram:</strong> ...</li>
            <li><strong>X:</strong> ...</li>
            <li><strong>Youtube:</strong> ...</li>
            <li><strong>Video Promocional:</strong> ...</li>
        </ol>
    </li>
    <li><strong>Fundadores:</strong>
        <ol>
            <li>...</li>
        </ol>
    </li>
    <li><strong>Puesto de los Fundadores:</strong>
        <ol>
            <li>...</li>
        </ol>
    </li>
    <li><strong>Currículum de los Fundadores:</strong>
        <ol>
            <li>...</li>
        </ol>
    </li>
    <li><strong>URL LinkedIn Fundadores:</strong>
        <ol>
            <li>...</li>
        </ol>
    </li>
    </ul>

    <h3>Indicadores Clave</h3>
    <ul>
    <li><strong>Sector:</strong> ...</li>
    <li><strong>Industrias (Tecnología primaria):</strong> ...</li>
    <li><strong>Mercado (Tecnología Secundaria):</strong> ...</li>
    <li><strong>Crecimiento de ingresos:</strong> ...</li>
    <li><strong>Rentabilidad:</strong> ...</li>
    <li><strong>Optimización de procesos:</strong> ...</li>
    <li><strong>Propuesta de Valor:</strong> ...</li>
    <li><strong>Mercado Objetivo:</strong> ...</li>
    <li><strong>Presencia en mercados actuales:</strong> ...</li>
    <li><strong>Inversionistas:</strong> ...</li>
    <li><strong>Ingresos:</strong> ...</li>
    <li><strong>Financiamiento:</strong> ...</li>
    <li><strong>Valoración:</strong> ...</li>
    </ul>

    <h3>Expansión Tecnológica</h3>
    <ul>
    <li><strong>Uso de IA u otras tecnologías:</strong> ...</li>
    <li><strong>Métricas destacadas:</strong> ...</li>
    </ul>

    <h3>Diferenciadores Clave</h3>
    <ul>
    <li><strong>Tecnología única:</strong> ...</li>
    <li><strong>Modelo comercial innovador:</strong> ...</li>
    <li><strong>Servicios o experiencias añadidas:</strong> ...</li>
    </ul>

    <h3>Contexto del Ecosistema</h3>
    <ul>
    <li><strong>Competidores principales:</strong> ...</li>
    <li><strong>Ventajas o desventajas competitivas:</strong> ...</li>
    <li><strong>Datos financieros de competidores:</strong> ...</li>
    <li><strong>Clientes:</strong> ...</li>
    <li><strong>Datos financieros relevantes:</strong> ...</li>
    </ul>

    <h3>Oportunidades Estratégicas</h3>
    <ul>
    <li><strong>Expansión regional o sectorial:</strong> ...</li>
    <li><strong>Sinergias tecnológicas:</strong> ...</li>
    <li><strong>Modelos de ingreso alternativos:</strong> ...</li>
    </ul>

    <h3>Viabilidad de Compra o Integración</h3>
    <ul>
    <li><strong>¿Es viable su adquisición o integración? ¿Por qué?</strong> ...</li>
    <li><strong>Alineación con ecosistemas (Telecom, Bancario, Retail, Media, Educación, Salud, Seguros):</strong> ...</li>
    </ul>

    <h3>Recomendación Ejecutiva</h3>
    <ul>
    <li><strong>Recomendación:</strong> [Compra / Alianza / Integración tecnológica]</li>
    <li><strong>Justificación estratégica:</strong> ...</li>
    <li><strong>Propuesta de siguiente paso:</strong> ...</li>
    </ul>

    <h3>Fuentes</h3>
    <ul> 
    <li>Apellido, A. A. (Año, Mes Día). <em>Título del artículo</em>. Nombre del sitio. <a>URL</a> </li>
    </ul>

    Devuelve solo este bloque de HTML. Nada más.
    """

    try:
        # Nueva implementación con búsqueda web integrada
        response = client.responses.create(
            model="gpt-4.1",
            tools=[{"type": "web_search_preview", "search_context_size": "low"}],
            input=prompt
        )
        
        respuesta_html = response.output_text
        
    except Exception as e:
        print("Error al generar respuesta del modelo:", e)
        return jsonify({'respuesta': 'Error al generar el análisis con el modelo.'}), 500
    
    return jsonify({'respuesta': respuesta_html})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

