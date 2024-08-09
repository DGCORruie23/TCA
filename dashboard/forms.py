from django import forms
from usuarios.models import Registro, Acciones,  Area, Mensaje
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
import re
from datetime import datetime
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
        fields = ['claveAcuerdo', 'fecha_inicio', 'fecha_termino', 'rubro', 'area', 'estado', 'porcentaje_avance']
        labels = {
            'claveAcuerdo': 'Clave de Acuerdo',
            'area': 'OR',
            'estado': 'Estatus',
            'porcentaje_avance': 'Porcentaje de Avance'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['area'].queryset = Area.objects.filter(idArea__lte=32)
        self.fields['porcentaje_avance'].validators.extend([MaxValueValidator(100), MinValueValidator(0)])

    def clean_claveAcuerdo(self):
        claveAcuerdo = self.cleaned_data.get('claveAcuerdo')
        pattern = r'^\d{2}/[A-Z]{3}/\d{2}/\d{4}$'
        if not re.match(pattern, claveAcuerdo):
            raise ValidationError("La clave del acuerdo debe tener el formato 00/AREA/MES/AÑO.")

        instance_id = self.instance.idRegistro
        if Registro.objects.exclude(idRegistro=instance_id).filter(claveAcuerdo=claveAcuerdo).exists():
            raise forms.ValidationError("Esta clave de acuerdo ya existe.")


        return claveAcuerdo

    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        if not fecha_inicio:
            raise ValidationError("La fecha de inicio es obligatoria.")
        try:
            datetime.strptime(fecha_inicio.strftime('%d/%m/%Y'), '%d/%m/%Y')
        except ValueError:
            raise ValidationError("La fecha debe tener el formato dd/mm/yyyy.")
        return fecha_inicio

    def clean_fecha_termino(self):
        fecha_termino = self.cleaned_data.get('fecha_termino')
        if not fecha_termino:
            raise ValidationError("La fecha de término es obligatoria.")
        try:
            datetime.strptime(fecha_termino.strftime('%d/%m/%Y'), '%d/%m/%Y')
        except ValueError:
            raise ValidationError("La fecha debe tener el formato dd/mm/yyyy.")
        return fecha_termino
    
    def clean(self):
        cleaned_data = super().clean()
        porcentaje_avance = cleaned_data.get('porcentaje_avance')

        if porcentaje_avance == 100:
            cleaned_data['estado'] = 2
        else:
            cleaned_data['estado'] = 1
        estado = cleaned_data.get('estado')
        print(estado)
        print(porcentaje_avance)
        if estado == 1 and porcentaje_avance != 100:
            raise forms.ValidationError('El estado está en "Atendido", pero el porcentaje de avance no es 100.')

        return cleaned_data

    
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