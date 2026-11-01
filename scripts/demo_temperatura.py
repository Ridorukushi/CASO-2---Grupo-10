"""La misma pregunta varias veces, con temperatura alta y con temperatura 0 + semilla.

    uv run demo_temperatura.py
"""
from comun import preguntar

PREGUNTA = "Inventa un nombre corto para la app de préstamos de la biblioteca de la FET. Responde solo el nombre."

print("== Temperatura 1.2, sin semilla ==")
for i in range(3):
    r = preguntar(PREGUNTA, temperatura=1.2, seed=None, num_predict=20)
    print(f"  {i + 1}. {r.message.content.strip()}")

print("\n== Temperatura 0, semilla 42 ==")
for i in range(3):
    r = preguntar(PREGUNTA, temperatura=0, seed=42, num_predict=20)
    print(f"  {i + 1}. {r.message.content.strip()}")
