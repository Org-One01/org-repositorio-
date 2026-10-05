# src/generar_pagina.py
import os

# Crear la carpeta public si no existe
os.makedirs("public", exist_ok=True)

html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora de Suma</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh; 
            background-color: #f0f2f5; 
            margin: 0; 
        }
        .card { 
            background: white; 
            padding: 2rem; 
            border-radius: 12px; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.1); 
            text-align: center; 
            max-width: 350px; 
            width: 100%; 
        }
        .input-group { 
            margin-bottom: 15px; 
            text-align: left; 
        }
        .input-group label { 
            display: block; 
            font-size: 0.9rem; 
            margin-bottom: 5px; 
            color: #555; 
        }
        .input-group input { 
            width: 100%; 
            padding: 10px; 
            border: 1px solid #ccc; 
            border-radius: 6px; 
            box-sizing: border-box; 
            font-size: 1rem; 
        }
        button { 
            background-color: #007bff; 
            color: white; 
            border: none; 
            padding: 12px; 
            border-radius: 6px; 
            font-size: 1rem; 
            cursor: pointer; 
            width: 100%; 
            margin-top: 10px; 
            transition: background 0.3s; 
        }
        button:hover { 
            background-color: #0056b3; 
        }
        .resultado { 
            color: #2e7d32; 
            font-size: 1.8rem; 
            font-weight: bold; 
            margin-top: 20px; 
            min-height: 40px; 
        }
    </style>
</head>
<body>
    <div class="card">
        <h2>Calculadora de Suma</h2>
        
        <div class="input-group">
            <label for="num1">Primer Número:</label>
            <input type="number" id="num1" placeholder="Ingresa el primer número">
        </div>

        <div class="input-group">
            <label for="num2">Segundo Número:</label>
            <input type="number" id="num2" placeholder="Ingresa el segundo número">
        </div>

        <button onclick="calcularSuma()">Calcular Suma</button>

        <div class="resultado" id="resultado"></div>
    </div>

    <script>
        function calcularSuma() {
            const val1 = parseFloat(document.getElementById('num1').value);
            const val2 = parseFloat(document.getElementById('num2').value);
            const resDiv = document.getElementById('resultado');

            if (isNaN(val1) || isNaN(val2)) {
                resDiv.style.color = '#d32f2f';
                resDiv.textContent = 'Por favor, ingresa números válidos.';
            } else {
                const suma = val1 + val2;
                resDiv.style.color = '#2e7d32';
                resDiv.textContent = `Resultado: ${suma}`;
            }
        }
    </script>
</body>
</html>"""

with open("public/index.html", "w", encoding="utf-8") as file:
    file.write(html_content)