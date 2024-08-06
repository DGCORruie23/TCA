from django import forms
from usuarios.models import Registro, Acciones,  Area, Mensaje
from django.core.validators import MaxValueValidator, MinValueValidator

class RegistroConAccionesYPruebasForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = ['claveAcuerdo','fecha_inicio', 'fecha_termino', 'rubro', 'area', ]
        labels = {
            'area': 'OR',
        }    

    accion1_area2 = forms.ModelMultipleChoiceField(queryset=Area.objects.all(), label="Áreas Responsables")
    accion1_descripcion = forms.CharField(widget=forms.Textarea, label="Descripción")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['area'].queryset = Area.objects.filter(idArea__lte=32) 

class RegistroConAccionesFORM(forms.ModelForm):
    class Meta:
        model = Registro
        fields = ['claveAcuerdo','fecha_inicio', 'fecha_termino', 'rubro', 'area', 'estado', 'porcentaje_avance']
        labels = {
            'claveAcuerdo': 'Clave de Acuerdo',
            'area': 'OR',
            'estado': 'Estatus',
            'porcentaje_avance': 'Porcentaje de Avance'
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['area'].queryset = Area.objects.filter(idArea__lte=32) 
        self.fields['porcentaje_avance'].validators.extend([MaxValueValidator(99), MinValueValidator(0)])


class AccionesForm(forms.ModelForm):
    class Meta:
        model = Acciones
        fields = ['area2', 'descripcion']
        labels = {
            'area2': 'Áreas Responsables',
        }

class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['texto', 'archivo']
        widgets = {
            'texto': forms.Textarea(attrs={'placeholder': 'Escribe tu mensaje aquí...'}),
        }


class CargarArchivoForm(forms.Form):
    archivo = forms.FileField()