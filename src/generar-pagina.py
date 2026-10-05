# src/generar_pagina.py
import os

num1 = 15
num2 = 25
suma = num1 + num2

# Crear la carpeta public si no existe
os.makedirs("public", exist_ok=True)

html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resultado de la Suma</title>
    <style>
        body {{ font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f0f2f5; margin: 0; }}
        .card {{ background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center; font-size: 1.2rem; }}
        .resultado {{ color: #2e7d32; font-size: 2rem; font-weight: bold; margin-top: 10px; }}
    </style>
</head>
<body>
    <div class="card">
        <h2>Resultado de la Suma</h2>
        <p>La suma de {num1} + {num2} es:</p>
        <div class="resultado">{suma}</div>
    </div>
</body>
</html>"""

with open("public/index.html", "w", encoding="utf-8") as file:
    file.write(html_content)