#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django import forms


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label="Contrasenia Anterior (*):",
        widget=forms.PasswordInput(attrs={'class':'edt_c'}),
        error_messages={'required': 'El Campo "Contrasenia Anterior" es obligatorio'}
    )

    password = forms.CharField(
        label="Nueva Contrasenia (*):",
        widget=forms.PasswordInput(attrs={'class':'edt_c'}),
        error_messages={'required': 'El Campo "Nueva Contrasenia" es obligatorio'}
    )
    re_password = forms.CharField(
        label="Repita Contrasenia (*):",
        widget=forms.PasswordInput(attrs={'class':'edt_c'}), #msj error redefinido abajo
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



class ChangeAvatarForm(forms.Form):
    photo = forms.ImageField(
        label="Foto",
        required = False
    )