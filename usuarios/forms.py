from django import forms
from usuarios.models import Usuario
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from typing import Any


class UsuarioRegistraForm(UserCreationForm):

    email = forms.EmailField(max_length=60, help_text="Obrigatório. Entre com o seu email")

    class Meta:
        model = Usuario
        fields = ('email', 'username', 'password1', 'password2')

class UsuarioAutenticaForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password = password):
                raise forms.ValidationError("Login Inválido")
            
class UsuarioAtualizaForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ('email','username')

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                usuario = Usuario.objects.exclude(pk=self.instance.pk).get(email=email)
            except Usuario.DoesNotExist:
                 return email
            raise forms.ValidationError('Email "%s" já sendo utilizado.' % email)
        
    def clean_nome(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                usuario = Usuario.objects.exclude(pk=self.instance.pk).get(username=username)
            except Usuario.DoesNotExist:
                 return username
            raise forms.ValidationError('Nome "%s" já sendo utilizado.' % username)
        