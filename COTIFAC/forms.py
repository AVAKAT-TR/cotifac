from django import forms
from .models import OrdenCompra, Item, Producto
from django.forms import inlineformset_factory


# ============================================================
# FORMULARIO PRINCIPAL: ORDEN DE COMPRA (COTIZACIÓN)
# ============================================================
class OrdenForm(forms.ModelForm):
    # Campo adicional para escribir un texto opcional junto al descuento.
    # Este texto se mostrará en el PDF (si está escrito y el descuento > 0).
    nota_descuento = forms.CharField(
        required=False,  # no es obligatorio
        label="Título del descuento",  # etiqueta visible en el formulario
        widget=forms.TextInput(attrs={
            'placeholder': 'Ej: Descuento transferencia electrónica',
            'style': 'width:250px;'  # ancho del campo en pantalla
        })
    )

    # Campo calculado automáticamente (solo lectura)
    monto_total = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    class Meta:
        model = OrdenCompra
        # Orden de los campos tal como deben mostrarse en el formulario
        fields = [
            'comprador',
            'fecha_emision',
            'fecha_vencimiento',
            'descuento',       # porcentaje de descuento global
            'nota_descuento',  # texto personalizado del descuento
            'monto_total',     # total final (calculado con JS)
        ]
        widgets = {
            # Campos de fecha con selector de calendario
            'fecha_emision': forms.DateInput(attrs={'type': 'date'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),

            # Campo de descuento global en porcentaje (editable)
            'descuento': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '0',
                'max': '100',
                'placeholder': '%',
                'style': 'width:80px; text-align:center;'
            }),
        }

    # Validación personalizada del campo monto_total
    # Convierte los valores que vienen con separadores o comas en un número real.
    def clean_monto_total(self):
        data = self.cleaned_data['monto_total']
        if isinstance(data, str):
            data = data.replace(".", "").replace(",", ".")
        try:
            return float(data)
        except Exception:
            raise forms.ValidationError("El monto no es un número válido")


# ============================================================
# FORMULARIO DE ÍTEMS (LÍNEAS DE PRODUCTOS NORMALES)
# ============================================================
class ItemForm(forms.ModelForm):
    # Selector de producto del catálogo existente (opcional)
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.all(),
        required=False,
        label="Producto",
        widget=forms.Select(attrs={"onchange": "actualizarPrecio(this)"})
    )

    class Meta:
        model = Item
        fields = ['producto', 'descripcion', 'cantidad', 'precio', 'descuento']
        widgets = {
            "descripcion": forms.TextInput(attrs={"readonly": "readonly"}),  # se autocompleta
            "precio": forms.NumberInput(attrs={"readonly": "readonly"}),     # se autocompleta
            "cantidad": forms.NumberInput(attrs={'min': '1'}),               # no puede ser negativa
            "descuento": forms.NumberInput(attrs={                           # descuento individual
                'step': '0.1',
                'min': '0',
                'max': '100',
                'placeholder': '%',
                'style': 'width:80px; text-align:center;'
            }),
        }
        labels = {
            'producto': 'Producto',
            'descripcion': 'Descripción',
            'cantidad': 'Unidades',
            'precio': 'Precio Neto',
            'descuento': 'Desc. (%)'
        }


# ============================================================
# FORMSET: para manejar múltiples ítems en una sola orden
# ============================================================
ItemFormSet = inlineformset_factory(
    OrdenCompra,  # modelo padre
    Item,         # modelo hijo
    form=ItemForm,
    extra=5,      # número de filas vacías disponibles
    can_delete=False
)


# ============================================================
# FORMULARIO FACTURA (con datos extendidos del cliente)
# ============================================================
class OrdenFacturaForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = [
            'comprador',
            'razon_social',
            'rut',
            'giro',
            'direccion',
            'comuna',
            'ciudad',
            'email',
            'fecha_emision',
            'fecha_vencimiento',
            'descuento',
        ]
        widgets = {
            'fecha_emision': forms.DateInput(attrs={'type': 'date'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
            'descuento': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '0',
                'max': '100'
            }),
        }
