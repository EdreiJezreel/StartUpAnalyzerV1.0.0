# StartUpAnalyzerV1.0.0
StartUpAnalyzer es un generador de reportes One-Page sobre startups relevantes mediante inteligencia artificial. 

> [!WARNING]
> El API_KEY de OpenAI estrá activa en Render hasta el 15 de mayo de 2025. Posterior a la fecha el sitio ya no contará con la funcionalidad hasta que se genera una nueva llave como variable de entorno.

## Funcionamiento
1. Se debe ingresar una URL para que el modelo de IA realice la consulta y genere el reporte de la Startup a investigar y dar clic en "Enviar".
2. Esperar la generación de del reporte (tiempo promedio de generación: 15 segundos).
3. El reporte se mostrará en la parte inferior del input.
4. Se puede consultar nuevamente el reporte generado en el historial de reportes, en el ícono ubicado en la parte superior derecha de la página.

> [!NOTE]
> Acceso al proyecto disponible en: https://startupanalyzer.onrender.com/

## Tecnologías utilizadas

- HTML5 + CSS3
- Bootstrap 5
- JavaScript Vanilla (No se usaron Frameworks)
- Backend: Flask (Python) 
- IA: Modelo de lenguaje `gpt-4.1-nano` (Puede ser modificado vía OpenRouter a otros modelos con mayor capacidad o gratuitos, incluso por modelos de OpenAI).
