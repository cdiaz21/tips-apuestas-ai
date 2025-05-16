import openai
import json
from datetime import datetime
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generar_tips():
    fecha_actual = datetime.now().strftime("%Y-%m-%d")

    prompt = (
        f"Genera 30 tips deportivos detallados para {fecha_actual}, "
        "de diferentes deportes (fútbol, tenis, baloncesto, etc.), "
        "incluye predicción, cuota estimada y una breve justificación en cada tip. "
        "Devuelve el resultado en formato JSON con los siguientes campos: "
        "'deporte', 'evento', 'tip', 'cuota', 'justificacion'."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    contenido = response['choices'][0]['message']['content']

    try:
        tips = json.loads(contenido)
    except json.JSONDecodeError:
        tips = {"error": "No se pudo analizar el contenido generado como JSON"}

    with open("tips.json", "w", encoding="utf-8") as f:
        json.dump(tips, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generar_tips()
