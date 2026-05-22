from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label="Nombre", max_length=120)
    email = forms.EmailField(label="Correo")
    company = forms.CharField(label="Empresa", max_length=140)
    message = forms.CharField(label="Mensaje", widget=forms.Textarea(attrs={"rows": 5}))
