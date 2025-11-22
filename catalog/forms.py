from django import forms
from .models import Libro

class LibroForm(forms.ModelForm):
  class Meta:
      model = Libro
      fields = ['titulo', 'autor', 'ejemplares']  # 'disponible' se calcula por ejemplares

class LoginForm(forms.Form):
    username_or_email = forms.CharField(label="Usuario o email", max_length=150)
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

