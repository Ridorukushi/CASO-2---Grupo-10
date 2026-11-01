# Análisis del Reto 5 (Bonus) — CafeFET

## Parte A: Comportamiento ante datos faltantes o ambiguos
1. **Manejo de nulos (`None`):** Cuando la información del mensaje era incompleta (ej. *"¿a cómo están las empanadas hoy?"*), el modelo asignó el valor `null` al campo opcional `hora_recogida` y clasificó el campo cerrado `metodo_pago` como `"desconocido"`, sin romper el JSON Schema de Pydantic.
2. **Respeto de tipos cerrados:** Los valores del enum `metodo_pago` se mantuvieron restringidos a los valores permitidos (`saldo_carne`, `efectivo`, `desconocido`).

## Parte B: Evaluación A/B de Prompts y Modelos
1. **Zero-Shot (v1) vs Few-Shot (v2):** El prompt v2 incluyó definiciones y ejemplos que ayudaron a desambiguar mensajes complejos como *'¿Me alcanza para una gaseosa con lo que tengo?'*, clasificándolo correctamente en `CONSULTAR_SALDO` en lugar de `CREAR_PEDIDO`.
2. **Comparación `qwen3.5:4b` vs `qwen3.5:0.8b`:**
   - `qwen3.5:4b`: Mantuvo alta precisión y estricto cumplimiento del formato sin agregar etiquetas decorativas.
   - `qwen3.5:0.8b`: Presentó pequeños errores de formato en Zero-Shot (v1), pero mejoró notoriamente su precisión al recibir los ejemplos Few-Shot en la versión v2.