import subprocess

# 10 casos etiquetados a mano (incluye 3 ambiguos)
dataset = [
    {"texto": "Quiero encargar 2 empanadas para las 9 am", "etiqueta": "CREAR_PEDIDO"},
    {"texto": "¿Cuánto dinero me queda disponible en el carné?", "etiqueta": "CONSULTAR_SALDO"},
    {"texto": "Por favor cancelen el pedido que hice hace 10 minutos", "etiqueta": "CANCELAR_PEDIDO"},
    {"texto": "¿A qué hora cierran la cafetería hoy?", "etiqueta": "OTRO_CONSULTA"},
    {"texto": "Un jugo de naranja y un sándwich por favor", "etiqueta": "CREAR_PEDIDO"},
    {"texto": "¿Me alcanza para una gaseosa con lo que tengo?", "etiqueta": "CONSULTAR_SALDO"},  # Ambiguo
    {"texto": "Ya no voy a poder ir a recoger el café", "etiqueta": "CANCELAR_PEDIDO"},      # Ambiguo
    {"texto": "¿Tienen servicio el sábado por la tarde?", "etiqueta": "OTRO_CONSULTA"},
    {"texto": "Repetir mi última orden de pan de bono", "etiqueta": "CREAR_PEDIDO"},
    {"texto": "Buenas tardes, ¿hay alguien atendiendo?", "etiqueta": "OTRO_CONSULTA"}        # Ambiguo
]

PROMPT_V1 = """Clasifica el siguiente mensaje en una de estas categorías: [CREAR_PEDIDO, CONSULTAR_SALDO, CANCELAR_PEDIDO, OTRO_CONSULTA].
Responde ÚNICAMENTE con el nombre exacto de la categoría.

Mensaje: "{texto}"
Categoría:"""

PROMPT_V2 = """Eres el clasificador de intenciones de CafeFET. Clasifica el mensaje según estas definiciones:
- CREAR_PEDIDO: Comprar, encargar o repetir una orden de alimentos/bebidas.
- CONSULTAR_SALDO: Consultar dinero disponible o si alcanza el saldo del carné.
- CANCELAR_PEDIDO: Solicitar anulación o avisar que no recogerá un pedido.
- OTRO_CONSULTA: Dudas de horario, disponibilidad o saludos.

Ejemplo 1: "Un tinto por favor" -> CREAR_PEDIDO
Ejemplo 2: "¿Tengo saldo?" -> CONSULTAR_SALDO

Responde ÚNICAMENTE con el nombre exacto de la categoría.

Mensaje: "{texto}"
Categoría:"""

def evaluar(modelo, prompt_template):
    aciertos = 0
    for item in dataset:
        p = prompt_template.format(texto=item["texto"])
        res = subprocess.run(["ollama", "run", modelo, "--think=false", p], capture_output=True, text=True, encoding="utf-8")
        prediccion = res.stdout.strip()
        if item["etiqueta"] in prediccion:
            aciertos += 1
    return (aciertos / len(dataset)) * 100

if __name__ == "__main__":
    print("=== RETO 5 - PARTE B: EVALUACIÓN A/B (CafeFET) ===")
    modelos = ["qwen3.5:4b", "qwen3.5:0.8b"]
    for mod in modelos:
        print(f"\nEvaluando Modelo: {mod}")
        acc_v1 = evaluar(mod, PROMPT_V1)
        acc_v2 = evaluar(mod, PROMPT_V2)
        print(f"  Accuracy Prompt v1 (Zero-Shot): {acc_v1:.1f}%")
        print(f"  Accuracy Prompt v2 (Few-Shot):  {acc_v2:.1f}%")