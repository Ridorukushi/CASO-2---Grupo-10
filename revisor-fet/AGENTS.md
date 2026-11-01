# AGENTS.md · BiblioFET

## Stack
Python 3.12, FastAPI, PostgreSQL, pytest

## Comandos
- Pruebas: pytest -q
- Formato: ruff format .

## Reglas
- Toda regla de negocio lleva al menos una prueba.
- No modificar migraciones ya aplicadas.
- Reglas de préstamo: máximo 3 activos, sin multas, la colección de referencia no se presta.
