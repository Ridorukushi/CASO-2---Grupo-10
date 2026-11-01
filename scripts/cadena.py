"""Encadenamiento: la salida de cada prompt es la entrada del siguiente.

    uv run cadena.py
"""
from comun import preguntar

REQUISITO = "que los estudiantes puedan renovar un préstamo desde la app"
REGLAS = ("Un préstamo se puede renovar una sola vez, solo si no está vencido y si ningún otro "
          "estudiante reservó el libro. La renovación extiende el vencimiento 8 días.")

historia = preguntar(
    "Eres analista de requisitos de BiblioFET. Convierte este requisito en UNA historia de usuario "
    f"con el formato: Como <rol>, quiero <acción>, para <beneficio>.\nRequisito: \"{REQUISITO}\".\n"
    "Devuelve solo la historia.").message.content
print("== 1. Historia ==\n" + historia)

criterios = preguntar(
    f"Escribe entre 3 y 5 criterios de aceptación Dado / Cuando / Entonces para esta historia.\n"
    f"Reglas: {REGLAS}\n<historia>{historia}</historia>").message.content
print("\n== 2. Criterios ==\n" + criterios)

pruebas = preguntar(
    "Escribe pruebas pytest, una por criterio, para la función renovar(prestamo, hoy) -> Prestamo, "
    "que lanza ValueError cuando no se puede renovar. Devuelve solo el código.\n"
    f"<criterios>{criterios}</criterios>").message.content
print("\n== 3. Pruebas ==\n" + pruebas)

revision = preguntar(
    "Para cada criterio indica qué prueba lo cubre. Si falta alguna, escríbela.\n"
    f"<criterios>{criterios}</criterios>\n<pruebas>{pruebas}</pruebas>").message.content
print("\n== 4. Revisión ==\n" + revision)
