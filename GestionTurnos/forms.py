#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django import forms

from globals import *


class RegisterForm(forms.Form):
    username = forms.CharField(label="Nombre de Usuario", widget=forms.TextInput(attrs={'class':'edt_c'}))
    password = forms.CharField(label="Contrasenia", widget=forms.PasswordInput(attrs={'class':'edt_c'}))
    re_password = forms.CharField(label="Contrasenia de Nuevo", widget=forms.PasswordInput(attrs={'class':'edt_c'}))
    first_name = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={'class':'edt_g'}))
    last_name = forms.CharField(label="Apellido", widget=forms.TextInput(attrs={'class':'edt_g'}))

    type_doc = forms.ChoiceField(label="Tipo de Documento", choices=TYPE_DOC_CHOICE)
    nro_doc = forms.CharField(label="Nro de Documento", widget=forms.TextInput(attrs={'class':'edt_c'}))
    address = forms.CharField(label='Direccion', widget=forms.TextInput(attrs={'class':'edt_g'}))
    gender = forms.ChoiceField(label='Genero', choices=SEXO_CHOICE)
    phone = forms.CharField(label="Telefono", widget=forms.TextInput(attrs={'class':'edt_c'}))
