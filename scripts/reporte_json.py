"""Salida estructurada: Ollama genera JSON que respeta un esquema de Pydantic.

    uv run reporte_json.py
"""
from typing import Literal
from pydantic import BaseModel
from comun import preguntar


class Reporte(BaseModel):
    tipo: Literal["BUG", "MEJORA", "DUDA"]
    modulo: Literal["busqueda", "prestamos", "multas"]
    severidad: Literal["alta", "media", "baja"]
    resumen: str


REPORTES = [
    "Intento renovar 'Cien años de soledad' y sale error 500. Ya probé dos veces.",
    "Sería útil poder pagar la multa desde la app con PSE.",
    "¿La búsqueda encuentra libros por ISBN o solo por título?",
]

for texto in REPORTES:
    r = preguntar(f"Extrae los datos del reporte de un usuario de BiblioFET:\n<reporte>{texto}</reporte>",
                  formato=Reporte.model_json_schema())
    rep = Reporte.model_validate_json(r.message.content)   # falla si el JSON no cumple el esquema
    print(f"{rep.tipo:7} | {rep.modulo:10} | {rep.severidad:5} | {rep.resumen}")
