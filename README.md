# Kit de demos · Sesión 03 · Ingeniería de prompts y de contexto

Diplomado en Ingeniería de Software con IA y Sistemas Agénticos · FET

> **Estudiantes:** sigan la guía paso a paso en [GUIA_PRACTICAS.md](GUIA_PRACTICAS.md).

## Preparación (una vez)

Requisitos: [Ollama](https://ollama.com/download), [uv](https://docs.astral.sh/uv/) y Git. **No hace falta tener Python instalado**: uv lo descarga.

```bash
# 1. Instalar uv
#    Linux / macOS:
curl -LsSf https://astral.sh/uv/install.sh | sh
#    Windows (PowerShell):
#    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. Modelos de la clase
ollama pull qwen3.5:4b
ollama pull phi4-mini
ollama pull qwen3.5:0.8b

# 3. Clonar y preparar Python (descarga Python 3.12 e instala ollama y pydantic en .venv)
git clone https://github.com/777wills/fet-diplomadoIA-prompting-p2
cd fet-diplomadoIA-prompting-p2
uv sync

# 4. Modelos de práctica (desde la raíz del repositorio)
ollama create qwen-demo       -f modelfiles/Modelfile.qwen-demo
ollama create phi-demo        -f modelfiles/Modelfile.phi-demo
ollama create revisor-ingenuo -f modelfiles/Modelfile.ingenuo
ollama create revisor-fet     -f revisor-fet/Modelfile
```

Patrón para ejecutar cada práctica (Linux/macOS; en Windows use `cmd` y `\` en la ruta):

```bash
ollama run qwen-demo --think=false < prompts/03_zero_shot.txt
```

Los scripts de Python se ejecutan desde la carpeta `scripts/` con `uv run` (por ejemplo, `uv run evalua.py`).
Todos usan `qwen3.5:4b` con el razonamiento apagado, temperatura 0 y semilla 42, salvo que se indique otra cosa.

## Orden de uso en clase

El detalle de cada práctica (comandos para Linux, macOS y Windows, qué observar y preguntas) está en [GUIA_PRACTICAS.md](GUIA_PRACTICAS.md).

| Práctica | Modelo | Archivos |
|---|---|---|
| 1 · Un modelo, dos prompts | `qwen-demo` | `prompts/01_gancho_A.txt`, `01_gancho_B.txt` |
| 2 · Primer uso y parámetros | `qwen3.5:4b` (desde Python) | `scripts/01_primer_uso.py`, `scripts/demo_temperatura.py` |
| 3 · System prompt con `/set system` | `qwen3.5:4b` (interactivo) | `revisor-fet/system_revisor_fet_una_linea.txt` |
| 4 · Modelo propio con Modelfile | `revisor-fet` | `revisor-fet/Modelfile`, `revisor-fet/AGENTS.md` |
| 5 · Fórmula base | `qwen-demo` | `prompts/02_formula_antes.txt`, `02_formula_despues.txt` |
| 6 · Zero-shot | `qwen-demo` | `prompts/03_zero_shot.txt` |
| 7 · Few-shot | `qwen-demo` | `prompts/04_few_shot.txt` |
| 8 · Delimitadores | `qwen-demo` | `prompts/05_delimitadores.txt` |
| 9 · Cadena de pensamiento | `phi-demo` y `qwen3.5:4b` con razonamiento | `prompts/06_cot_sin.txt`, `06_cot_con.txt`, `06_cot_razonador.txt` |
| 10 · Encadenamiento | `qwen3.5:4b` (desde Python) | `scripts/cadena.py` o `prompts/07_cadena_*.txt` |
| 11 · Instrucciones claras | `qwen-demo` | `prompts/12_instrucciones_antes.txt`, `12_instrucciones_despues.txt`, `12_autoverificacion.txt` |
| 12 · Rol | `qwen-demo` | `prompts/08_rol_*.txt` |
| 13 · Formato: tabla y JSON | `qwen-demo` y Python | `prompts/09_formato_tabla.txt`, `scripts/reporte_json.py` |
| 14 · Más contexto no es mejor | `qwen3.5:4b` (desde Python) | `scripts/demo_contexto.py` |
| 14B · Chat largo: la instrucción que se olvida | `qwen-demo` (chat interactivo) | `prompts/13_chat_largo.txt` |
| 15 · Prompt injection | `revisor-ingenuo` y `revisor-fet` | `prompts/10_*.txt` |
| 16 · Optimizar con IA | Un modelo grande o `qwen-demo` | `prompts/11_meta_prompt.txt` |
| 17 · Evaluar prompts | `qwen3.5:4b` (desde Python) | `scripts/evalua.py` |

**Importante:** `revisor-fet` es solo para las prácticas 4 y 15. Su system prompt lo convierte en revisor de código, así que no sirve para estudiar las demás técnicas.

## Notas

- **Razonamiento:** si su versión de Ollama no reconoce `--think=false`, dentro del chat use `/set nothink`.
  En Python se controla con `think=False` (ya incluido en `scripts/comun.py`).
- **Resultados variables:** con modelos de 1–4 B la salida cambia entre versiones. Ensaye cada demo antes de clase.
- **demo_contexto.py:** el corte exacto depende del modelo y de la versión de Ollama. El script muestra cuántos
  tokens leyó el modelo; si con 2048 todavía responde bien, suba `--articulos`.
- **Respuestas esperadas del zero-shot:** «avisara por correo» → MEJORA; «¿cuántos libros…?» → DUDA;
  «renovar es lentísimo» → BUG (decisión del equipo; es el caso ambiguo).
