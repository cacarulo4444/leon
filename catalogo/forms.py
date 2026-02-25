from django import forms
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['nombre', 'apellido', 'telefono', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Tu nombre', 'class': 'oneui-input'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Tu apellido', 'class': 'oneui-input'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ej: 11 1234 5678', 'class': 'oneui-input'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Dirección (Opcional)', 'class': 'oneui-input'}),
        }