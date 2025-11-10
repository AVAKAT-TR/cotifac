from django.db import models
from django.contrib.auth.models import User


class OrdenCompra(models.Model):
    # --- Datos del cliente ---
    comprador = models.CharField(max_length=200)
    razon_social = models.CharField(max_length=150, blank=True, null=True)
    rut = models.CharField(max_length=20, blank=True, null=True)
    giro = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    comuna = models.CharField(max_length=100, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # --- Datos del documento ---
    vendedor = models.CharField(max_length=200, blank=True, null=True)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    monto_total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    TIPO_CHOICES = [
        ("COTIZACIÓN", "Cotización"),
        ("FACTURA", "Factura"),
    ]

    tipo_documento = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default="COTIZACIÓN"
    )

    def __str__(self):
        return f"Orden {self.id} - {self.comprador}"


class Item(models.Model):
    orden = models.ForeignKey(OrdenCompra, related_name="items", on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.SET_NULL, null=True, blank=True)
    descripcion = models.CharField(max_length=200, blank=True)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio

class Producto(models.Model):
    tipo = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100)
    medida = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=12, decimal_places=0)

    def __str__(self):
        tipo = self.tipo or ""
        codigo = self.codigo or ""
        medida = self.medida or ""
        precio = f"${self.precio:,.0f}" if self.precio else "$0"
        return f"{tipo} - {codigo} {medida} ({precio})".strip()


