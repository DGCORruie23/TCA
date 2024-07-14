from django import forms
from usuarios.models import Registro, Acciones,  Area, Mensaje


class RegistroConAccionesYPruebasForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = ['claveAcuerdo','fecha_inicio', 'fecha_termino', 'rubro', 'area', 'estado']
    

    accion1_area2 = forms.ModelMultipleChoiceField(queryset=Area.objects.all(), label="Área 2")
    accion1_descripcion = forms.CharField(widget=forms.Textarea, label="Descripción")
    

class AccionForm(forms.ModelForm):
    class Meta:
        model = Acciones
        fields = ['area2', 'descripcion']


class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['texto', 'archivo']
        widgets = {
            'texto': forms.Textarea(attrs={'placeholder': 'Escribe tu mensaje aquí...'}),
        }
