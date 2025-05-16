import openai
import os
from datetime import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")

def generar_tips_html():
    fecha_actual = datetime.now().strftime("%Y-%m-%d")

    prompt = (
        f"Genera 30 tips deportivos detallados para {fecha_actual}, "
        "de diferentes deportes como fútbol, tenis, baloncesto, béisbol, etc. "
        "Para cada tip, incluye: el deporte, el evento o enfrentamiento, la predicción o apuesta sugerida, "
        "una cuota estimada y una justificación breve. Devuélvelo en formato JSON como una lista de objetos "
        "con las claves: 'deporte', 'evento', 'tip', 'cuota', 'justificacion'."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    import json
    try:
        tips = json.loads(response['choices'][0]['message']['content'])
    except Exception as e:
        tips = []
    
    # Construir HTML
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Tips Diarios de Apuestas Deportivas - {fecha_actual}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #2c3e50; }}
        .tip {{ border-bottom: 1px solid #ddd; padding: 10px 0; }}
        .deporte {{ font-weight: bold; color: #2980b9; }}
        .evento {{ font-style: italic; }}
        .cuota {{ color: #27ae60; }}
        .justificacion {{ margin-top: 5px; }}
    </style>
</head>
<body>
    <h1>Tips Diarios de Apuestas Deportivas - {fecha_actual}</h1>
"""

    if tips:
        for tip in tips:
            html_content += f"""
    <div class="tip">
        <div class="deporte">{tip.get('deporte', '')}</div>
        <div class="evento">{tip.get('evento', '')}</div>
        <div><strong>Tip:</strong> {tip.get('tip', '')}</div>
        <div class="cuota"><strong>Cuota:</strong> {tip.get('cuota', '')}</div>
        <div class="justificacion">{tip.get('justificacion', '')}</div>
    </div>
"""
    else:
        html_content += "<p>No se pudieron generar tips hoy.</p>"

    html_content += """
</body>
</html>
"""

    with open("tips.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    generar_tips_html()
