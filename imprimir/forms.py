from django import forms

class formulario(forms.Form):
    number = forms.IntegerField(label='Número de copias', required=False)
    barcode = forms.CharField(label='Código de barras', max_length=100, required=False)