# StartUpAnalyzerV1.0.0
StartUpAnalyzer es un generador de reportes One-Page sobre startups relevantes mediante inteligencia artificial. 

> [!WARNING]
> El API_KEY de OpenAI estrá activa en Render hasta el 7 de Junio de 2025. Posterior a la fecha el sitio ya no contará con la funcionalidad hasta que se genera una nueva llave como variable de entorno.

> [!CAUTION]
> El modelo a la fecha (30 de Mayo de 2025) tiene un saldo disponible de $3.79 USD. Cada uso consume aproximadamente $0.01 USD en promedio, por lo que se solicita amplicar dicho límite para un uso correcto y continuo de la herramienta mediante una API KEY empresarial; o, en su defecto, un uso moderado hasta una implementación en WIKICID.

## Funcionamiento
1. Se debe ingresar una URL para que el modelo de IA realice la consulta y genere el reporte de la Startup a investigar y dar clic en "Enviar".
2. Esperar la generación de del reporte (tiempo promedio de generación: 25 segundos por la nueva funcionalidad, ya que el modelo prioriza la búsqueda en la fuente primaria como en externas).
3. El reporte se mostrará en la parte inferior del input.
4. Se puede consultar nuevamente el reporte generado en el historial de reportes, en el ícono ubicado en la parte superior derecha de la página (Se trata de una sesión temporal, por lo que no se almacena el reporte y se borrará una vez sea actualizada la página).

> [!NOTE]
> Acceso al proyecto disponible en: https://startupanalyzer.onrender.com/

## Tecnologías utilizadas

- HTML5 + CSS3
- Bootstrap 5
- JavaScript Vanilla (No se usaron Frameworks)
- Backend: Flask (Python) 
- IA: Modelo de lenguaje `gpt-4.1` Puede ser modificado a otro modelo de OpenAI que mantenga la herramienta de web search, como puede ser `gpt-4.1-mini` (Herramienta solo disponible en estos dos modelos).
- Hosting: Render

> [!CAUTION]
> Todo reporte es generado en su totalidad por IA acorde a las capacidades del modelo empleado, es posible que las indicaciones en el prompt sean omitidas por el modelo, como puede ser la navegación web, por lo que los datos mostrados en el reporte deben ser verificados en fuentes confiables, ya que los modelos de IA puede cometer errores. 

Por motivos de la herramienta de Hosting, tuve que integrar la lógica de de JavaScript y los estilos en el html, esto será corregido en una siguiente versión.
