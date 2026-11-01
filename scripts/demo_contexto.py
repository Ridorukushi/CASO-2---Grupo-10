"""¿Qué pasa cuando el contexto no cabe en la ventana?

La instrucción va en el primer mensaje, el reglamento largo y la pregunta en el último.
Si num_ctx es pequeño, Ollama descarta los mensajes más antiguos para que quepa el último:
la instrucción se pierde.

    uv run demo_contexto.py --num_ctx 2048
    uv run demo_contexto.py --num_ctx 8192

Ensaye antes de clase: el punto exacto de corte depende del modelo y de la versión de Ollama.
Si con 2048 la instrucción todavía cabe, suba --articulos.
"""
import argparse
from comun import preguntar

TEMAS = [
    ("préstamos", "Los estudiantes activos pueden tener hasta tres préstamos simultáneos por un plazo de ocho días hábiles."),
    ("renovaciones", "Cada préstamo puede renovarse una sola vez, siempre que no esté vencido y que ningún usuario lo haya reservado."),
    ("multas", "El retraso en la devolución genera una multa de mil pesos por día y por ejemplar."),
    ("colección de referencia", "Los diccionarios, enciclopedias y obras de referencia solo se consultan en sala y no se prestan."),
    ("reservas", "Un usuario puede reservar un ejemplar prestado; la reserva se mantiene durante dos días hábiles tras la devolución."),
    ("daños", "Quien dañe o pierda un ejemplar debe reponerlo con uno de la misma edición o pagar su valor comercial."),
    ("horarios", "La biblioteca atiende de lunes a viernes de siete de la mañana a nueve de la noche y los sábados hasta el mediodía."),
    ("salas", "Las salas de estudio grupal se reservan por bloques de dos horas con un máximo de seis personas."),
]


def reglamento(n):
    arts = []
    for i in range(n):
        tema, regla = TEMAS[i % len(TEMAS)]
        arts.append(f"Artículo {i + 1}. Sobre {tema}. {regla} Esta disposición aplica a estudiantes, docentes y "
                    f"personal administrativo de la Fundación Escuela Tecnológica de Neiva, salvo las excepciones "
                    f"que apruebe por escrito la coordinación de la biblioteca.")
    return "\n".join(arts)


ap = argparse.ArgumentParser()
ap.add_argument("--num_ctx", type=int, default=2048)
ap.add_argument("--articulos", type=int, default=40)
ap.add_argument("--modelo", default="qwen3.5:4b")
a = ap.parse_args()

mensajes = [
    {"role": "user", "content": "Instrucción para toda la conversación: responde SOLO con la palabra SÍ o la palabra NO, sin explicación."},
    {"role": "assistant", "content": "Entendido."},
    {"role": "user", "content": f"<reglamento>\n{reglamento(a.articulos)}\n</reglamento>\n\n"
                                "Pregunta: ¿puede un estudiante sin multas llevarse prestado un diccionario?"},
]
r = preguntar(None, modelo=a.modelo, num_ctx=a.num_ctx, num_predict=200, mensajes=mensajes)
print(f"num_ctx={a.num_ctx} · tokens que el modelo realmente leyó: {r.prompt_eval_count}")
print("Respuesta:", r.message.content.strip())
