#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django import forms

from globals import *


class RegisterForm(forms.Form):
    username = forms.CharField(
        label="Nombre de Usuario (*)",
        widget=forms.TextInput(attrs={'class':'edt_c'}),
        error_messages={'required': 'El Campo "Nombre de Usuario" es obligatorio'},
        
    )
    password = forms.CharField(
        label="Contrasenia (*)",
        widget=forms.PasswordInput(attrs={'class':'edt_c'}),
        error_messages={'required': 'El Campo "Contrasenia" es obligatorio'}
    )
    re_password = forms.CharField(
        label="Repita Contrasenia (*)",
        widget=forms.PasswordInput(attrs={'class':'edt_c'}), #msj error redefinido abajo
        required = False
    )
    email = forms.EmailField(
        label="Email (*)",
        #widget=forms.TextInput(attrs={'class':'edt_m'}),
        error_messages={'required': 'El Campo "Email" es obligatorio'}
    )
    first_name = forms.CharField(
        label="Nombre", 
        widget=forms.TextInput(attrs={'class':'edt_m'}),
        required = False
    )
    last_name = forms.CharField(
        label="Apellido", 
        widget=forms.TextInput(attrs={'class':'edt_m'}),
        required = False
    )

    type_doc = forms.ChoiceField(label="Tipo de Documento", choices=TYPE_DOC_CHOICE)
    nro_doc = forms.CharField(
        label="Nro de Documento",
        widget=forms.TextInput(attrs={'class':'edt_c'}),
        required = False
    )
    gender = forms.ChoiceField(label='Genero', choices=SEXO_CHOICE)
    address = forms.CharField(
        label='Direccion',
        widget=forms.TextInput(attrs={'class':'edt_g'}),
        required = False
    )
    phone = forms.CharField(
        label="Telefono",
        widget=forms.TextInput(attrs={'class':'edt_c'}),
        required = False
    )


    def clean_re_password(self):
        """
            compara si las contrasenias coinciden
        """
        re_password = self.cleaned_data.get('re_password', '')
        password = self.cleaned_data.get('password', '')
        
        if password != re_password:
            raise forms.ValidationError("Error las contrasenias no coinciden")


    """
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        _password = cleaned_data.get("password")
        _re_password = cleaned_data.get("re_password")

        if _password != _re_password:

            self._errors["re_password"] = "Error las contrase�as no coinciden" #self.error_class(["Error las contrase�as no coinciden"])
            #del cleaned_data["re_password"]
            
        return cleaned_data
    """



class MedicRegisterForm(RegisterForm):
    matricula = forms.CharField(
        label="Matricula",
        widget=forms.TextInput(attrs={'class':'edt_c'}),
        required = False
    )



class MedicSpecialityAdd(forms.Form):
    specialty = forms.ChoiceField(label="Tipo de Documento", choices="")