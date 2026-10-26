# src/app_app/models.py
from django.db import models
from django.db.models import Avg


# ─────────────────────────────────────────────────────────────
# ENTIDADES BASE
# ─────────────────────────────────────────────────────────────
class Proveedor(models.Model):
    """🏭 1:N — Un proveedor tiene MUCHOS productos."""
    nombre     = models.CharField(max_length=100)
    contacto   = models.CharField(max_length=100, blank=True)
    telefono   = models.CharField(max_length=20,  blank=True)
    email      = models.EmailField(blank=True)
    pais       = models.CharField(max_length=50,  blank=True)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Etiqueta(models.Model):
    """🏷️ N:N con ProductoRopa."""
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Coleccion(models.Model):
    """📚 N:N con ProductoRopa."""
    nombre      = models.CharField(max_length=100)
    temporada   = models.CharField(max_length=50, blank=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Colección"
        verbose_name_plural = "Colecciones"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.temporada})" if self.temporada else self.nombre


# ─────────────────────────────────────────────────────────────
# PRODUCTO PRINCIPAL
# ─────────────────────────────────────────────────────────────
class ProductoRopa(models.Model):
    CATEGORIAS = [
        ('CAMISA',    'Camisa / Camiseta'),
        ('PANTALON',  'Pantalón / Jean'),
        ('CHAQUETA',  'Chaqueta / Abrigo'),
        ('CALZADO',   'Calzado'),
        ('ACCESORIO', 'Accesorio'),
    ]

    nombre        = models.CharField(max_length=100)
    categoria     = models.CharField(max_length=20, choices=CATEGORIAS, default='CAMISA')
    talla         = models.CharField(max_length=10, default='M')
    precio        = models.DecimalField(max_digits=10, decimal_places=2)
    stock         = models.IntegerField(default=10)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # 🔗 1:N  ── Muchos productos → 1 proveedor
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='productos'
    )

    # 🔗 N:N ── Muchos productos ↔ Muchas etiquetas
    etiquetas = models.ManyToManyField(
        Etiqueta, related_name='productos', blank=True
    )

    # 🔗 N:N ── Muchos productos ↔ Muchas colecciones
    colecciones = models.ManyToManyField(
        Coleccion, related_name='productos', blank=True
    )

    class Meta:
        verbose_name = "Producto de Ropa"
        verbose_name_plural = "Productos de Ropa"
        ordering = ['-fecha_creacion']

# ... (resto del código de ProductoRopa)
    def __str__(self):
        return f"{self.nombre} ({self.talla}) - ${self.precio}"

    # ✅ CORREGIDO: Debe ir con sangría dentro de la clase
    @property
    def promedio_calificacion(self):
        cache = getattr(self, '_prefetched_objects_cache', {}).get('resenas')
        if cache is not None:
            total = len(cache)
            return sum(r.calificacion for r in cache) / total if total else 0
        return self.resenas.aggregate(prom=Avg('calificacion'))['prom'] or 0


# ─────────────────────────────────────────────────────────────
# RELACIÓN 1:1
# ─────────────────────────────────────────────────────────────
class DetalleProducto(models.Model):
    """📝 1:1 — Cada producto tiene UN detalle (y viceversa)."""
    producto             = models.OneToOneField(
        ProductoRopa, on_delete=models.CASCADE, related_name='detalle'
    )
    descripcion          = models.TextField(blank=True)
    material             = models.CharField(max_length=100, blank=True)
    instrucciones_cuidado = models.TextField(blank=True)
    pais_fabricacion     = models.CharField(max_length=50, blank=True)
    peso_gramos          = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Detalle de Producto"
        verbose_name_plural = "Detalles de Producto"

    def __str__(self):
        return f"Detalle de {self.producto.nombre}"


# ─────────────────────────────────────────────────────────────
# RELACIÓN 1:N (más)
# ─────────────────────────────────────────────────────────────
class Variante(models.Model):
    """🎨 1:N — Un producto tiene MUCHAS variantes (color/talla)."""
    producto    = models.ForeignKey(
        ProductoRopa, on_delete=models.CASCADE, related_name='variantes'
    )
    color       = models.CharField(max_length=30)
    talla       = models.CharField(max_length=10)
    stock       = models.IntegerField(default=0)
    precio_extra = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Variante"
        verbose_name_plural = "Variantes"
        ordering = ['producto', 'color', 'talla']

    def __str__(self):
        return f"{self.producto.nombre} — {self.color} / {self.talla}"


class Resena(models.Model):
    """⭐ 1:N — Un producto tiene MUCHAS reseñas."""
    producto      = models.ForeignKey(
        ProductoRopa, on_delete=models.CASCADE, related_name='resenas'
    )
    autor         = models.CharField(max_length=100)
    comentario    = models.TextField()
    calificacion  = models.PositiveSmallIntegerField(default=5)  # 1..5
    fecha         = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.autor} — {self.calificacion}★ ({self.producto.nombre})"