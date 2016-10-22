# -*- coding: utf-8 -*-
from django import forms
from sistema.models import TiempoAsignacion, BusAlimentador, Despacho
#from sistema.views  import solicitudes


class FormularioContactos(forms.Form):
    asunto = forms.CharField(max_length=100)
    email = forms.EmailField(required=False, label='Tu correo electronico')
    mensaje = forms.CharField(widget=forms.Textarea)

    def clean_mensaje(self):
        mensaje = self.cleaned_data['mensaje']
        num_palabras = len(mensaje.split())
        if num_palabras < 4:
            raise forms.ValidationError("¡Se requieren mínimo 4 palabras!")
        return mensaje


class TiempoAsignacionForm(forms.ModelForm):
    class Meta:
        model = TiempoAsignacion
        #exclude = ['CodRuta', 'Despachado']
        fields = ['NumeroBus',]
        

    #Filtrar el campo Numero de bus del formulario
    def __init__(self, *args, **kwargs):
        super(TiempoAsignacionForm, self).__init__(*args, **kwargs)
        # access object through self.instance...
        self.fields['NumeroBus'].queryset = BusAlimentador.objects.filter(Estado='DISPONIBLE')

    def clean_NumeroBus(self):
        num_bus = self.cleaned_data['NumeroBus']        
        if num_bus == None:
            raise forms.ValidationError("¡Por favor, seleccione un bus antes de despachar la ruta!")
        return num_bus

class BusAlimentadorForm(forms.ModelForm):
    class Meta:
        model = BusAlimentador
        exclude = ['CodRuta', 'Estado', 'CapacidadBus', 'NumDespacho']


class DespachoForm(forms.ModelForm):
    class Meta:
        model = Despacho
        fields = []

     


