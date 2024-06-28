from django import forms
from usuarios.models import Registro, Acciones, Pruebas, Area

# class RegistroForm(forms.ModelForm):
#     class Meta:
#         model = Registro
#         fields = ['fecha_inicio', 'fecha_termino', 'rubro', 'area', 'estado']


class RegistroConAccionesYPruebasForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = ['claveAcuerdo','fecha_inicio', 'fecha_termino', 'rubro', 'area', 'estado']
    
    accion1_area1 = forms.ModelMultipleChoiceField(queryset=Area.objects.all(), label="Área 1")
    accion1_area2 = forms.ModelMultipleChoiceField(queryset=Area.objects.all(), label="Área 2")
    accion1_descripcion = forms.CharField(widget=forms.Textarea, label="Descripción")
    
    prueba1_nom_archivo = forms.CharField(max_length=100, label="Nombre del Archivo")
    prueba1_tipo = forms.ChoiceField(choices=Pruebas.types_archivo, label="Tipo")
    prueba1_archivo_url = forms.CharField(max_length=100, label="URL del archivo")

    # area = forms.ModelChoiceField(queryset=Area.objects.all(), label="Área")



class PruebaForm(forms.ModelForm):
    class Meta:
        model = Pruebas
        fields = ['nom_archivo', 'tipo', 'archivo_url']


class AccionForm(forms.ModelForm):
    class Meta:
        model = Acciones
        fields = ['area1', 'area2', 'descripcion']

class PruebaForm(forms.ModelForm):
    class Meta:
        model = Pruebas
        fields = ['nom_archivo', 'tipo', 'archivo_url']
