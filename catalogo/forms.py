from django import forms
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['nombre', 'apellido', 'telefono', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full bg-black border border-white/10 rounded-xl p-4 text-white focus:border-[#ff0000] focus:ring-1 focus:ring-[#ff0000] outline-none transition-all', 'placeholder': 'Tu nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'w-full bg-black border border-white/10 rounded-xl p-4 text-white focus:border-[#ff0000] focus:ring-1 focus:ring-[#ff0000] outline-none transition-all', 'placeholder': 'Tu apellido'}),
            'telefono': forms.TextInput(attrs={'class': 'w-full bg-black border border-white/10 rounded-xl p-4 text-white focus:border-[#ff0000] focus:ring-1 focus:ring-[#ff0000] outline-none transition-all', 'placeholder': 'Ej: 11 1234 5678'}),
            'direccion': forms.TextInput(attrs={'class': 'w-full bg-black border border-white/10 rounded-xl p-4 text-white focus:border-[#ff0000] focus:ring-1 focus:ring-[#ff0000] outline-none transition-all', 'placeholder': 'Calle 123 (Opcional)'}),
        }