"""Primer uso: la misma pregunta que en la terminal, ahora desde Python.

    uv run 01_primer_uso.py
"""
from comun import preguntar

r = preguntar("Explica en 3 líneas qué es un préstamo bibliotecario.")
print(r.message.content)
print(f"\nTokens de entrada: {r.prompt_eval_count} · tokens de salida: {r.eval_count}")
