from django import forms

class DocumentoForm(forms.Form):
    nombre = forms.CharField(max_length=255)
    archivo = forms.FileField()
