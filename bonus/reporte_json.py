import json
import subprocess
from typing import List, Literal, Optional
from pydantic import BaseModel, Field

# Esquema Pydantic para CafeFET (4 campos requeridos)
class ItemProducto(BaseModel):
    nombre: str = Field(description="Nombre del producto o bebida")
    cantidad: int = Field(default=1, ge=1, description="Cantidad solicitada")

class PedidoCafeFET(BaseModel):
    productos: List[ItemProducto] = Field(description="Lista de productos del pedido")
    hora_recogida: Optional[str] = Field(default=None, description="Hora de recogida (ej. 10:30) o None si no especifica")
    metodo_pago: Literal["saldo_carne", "efectivo", "desconocido"] = Field(description="Método de pago seleccionado")
    observaciones: Optional[str] = Field(default=None, description="Notas especiales como sin azúcar o caliente")

# 6 mensajes de prueba (4 completos, 2 ambiguos/incompletos)
mensajes_test = [
    "Hola, quiero pedir 2 empanadas y 1 jugo de mora para recoger a las 10:30 am, me descuentas del saldo del carné.",
    "Un café tinto sin azúcar y una dona por favor, pago en efectivo.",
    "Por favor 1 sándwich de pollo para la 1:00 pm. Sin cebolla y me descuentas del saldo.",
    "Me da 3 deditos de queso para llevar a las 8:00 am.",
    "Buenas, ¿a cómo están las empanadas hoy?",              # Ambiguo / Incompleto
    "Quiero repetir lo que pedí ayer para más tarde."        # Ambiguo / Incompleto
]

def extraer_datos(mensaje: str) -> str:
    schema = json.dumps(PedidoCafeFET.model_json_schema(), ensure_ascii=False)
    prompt = f"""Extrae los datos del pedido de CafeFET en formato JSON válido según este esquema:
{schema}

Mensaje del usuario: "{mensaje}"
JSON:"""
    
    result = subprocess.run(
        ["ollama", "run", "qwen3.5:4b", "--think=false", prompt],
        capture_output=True, text=True, encoding="utf-8"
    )
    return result.stdout.strip()

if __name__ == "__main__":
    print("=== RETO 5 - PARTE A: EXTRACCIÓN JSON VALIDADO (CafeFET) ===")
    for idx, msg in enumerate(mensajes_test, 1):
        print(f"\n--- Mensaje {idx} ---")
        print(f"Texto: {msg}")
        print(f"JSON Extraído:\n{extraer_datos(msg)}")