"""Evaluar prompts como código: dos versiones del prompt contra los mismos casos.

    uv run evalua.py
    uv run evalua.py --modelo qwen3.5:0.8b
"""
import argparse
import re
from comun import preguntar

CASOS = [
    ("Busco por autor García Márquez y la app se queda cargando.", "BUG"),
    ("Ojalá la app me avisara por correo dos días antes del vencimiento.", "MEJORA"),
    ("¿Cuántos libros puedo tener prestados a la vez?", "DUDA"),
    ("Renovar es lentísimo, ¿eso es normal?", "BUG"),
    ("Me cobraron una multa de un libro que ya devolví.", "BUG"),
    ("Podrían agregar modo oscuro a la app.", "MEJORA"),
    ("¿Los libros de referencia se pueden sacar el fin de semana?", "DUDA"),
    ("La app no deja iniciar sesión desde el celular desde ayer.", "BUG"),
]

V1 = """Clasifica el reporte de un usuario de BiblioFET en UNA categoría: BUG, MEJORA o DUDA.
Responde solo con la categoría.
Reporte: "{reporte}\""""

V2 = """Clasifica el reporte de un usuario de BiblioFET en UNA categoría.
- BUG: algo que debería funcionar no funciona, o funciona mal o muy lento, aunque el usuario lo escriba como pregunta.
- MEJORA: una funcionalidad nueva que el usuario desea.
- DUDA: una pregunta sobre reglas o uso, sin falla de por medio.

Ejemplo: "Renovar tarda un minuto, ¿es normal?" -> BUG

Responde solo con BUG, MEJORA o DUDA.
Reporte: "{reporte}\""""


def clasificar(plantilla, reporte, modelo):
    r = preguntar(plantilla.format(reporte=reporte), modelo=modelo, num_predict=10)
    m = re.search(r"BUG|MEJORA|DUDA", r.message.content.upper())
    return m.group(0) if m else r.message.content.strip()


ap = argparse.ArgumentParser()
ap.add_argument("--modelo", default="qwen3.5:4b")
a = ap.parse_args()

for nombre, plantilla in [("v1", V1), ("v2", V2)]:
    ok = 0
    for reporte, esperado in CASOS:
        obtenido = clasificar(plantilla, reporte, a.modelo)
        if obtenido == esperado:
            ok += 1
        else:
            print(f"  [{nombre}] falló: «{reporte}» -> {obtenido} (esperado {esperado})")
    print(f"{nombre}: {ok}/{len(CASOS)}\n")
