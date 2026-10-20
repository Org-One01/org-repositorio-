# src/app_app/models.py
from django.db import models

class ProductoRopa(models.Model):
    CATEGORIAS = [
        ('CAMISA', 'Camisa / Camiseta'),
        ('PANTALON', 'Pantalón / Jean'),
        ('CHAQUETA', 'Chaqueta / Abrigo'),
        ('CALZADO', 'Calzado'),
        ('ACCESORIO', 'Accesorio'),
    ]

    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='CAMISA')
    talla = models.CharField(max_length=10, default='M')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=10)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.talla}) - ${self.precio}"