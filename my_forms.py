#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django import forms


from GestionTurnos.models import UserInformation



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
        label="Avatar",
        required = False
    )



class ChangeUserInformationForm(forms.ModelForm):
    class Meta:
        model = UserInformation
        fields = (
            'type_doc',
            'nro_doc',
            'gender',
            'phone',
            'address',
            'city',
            'state',
            'birth_date',
            #'matricula',
        )

        widgets = {
            'birth_date': forms.TextInput(attrs={'class':'edt_c',}),
            'nro_doc': forms.TextInput(attrs={'class':'edt_c',}),
            'address' : forms.TextInput(attrs={'class':'edt_g',}),
        }


class ChangeMedicInformationForm(forms.ModelForm):
    class Meta:
        model = UserInformation
        fields = (
            'type_doc',
            'nro_doc',
            'gender',
            'phone',
            'address',
            'city',
            'state',
            'birth_date',
            'matricula',
        )

        widgets = {
            'birth_date': forms.TextInput(attrs={'class':'edt_c',}),
            'nro_doc': forms.TextInput(attrs={'class':'edt_c',}),
            'address' : forms.TextInput(attrs={'class':'edt_g',}),
        }


class ChangeUserDataForm(forms.Form):

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

    email = forms.EmailField(
        label="Email (*)",
        widget=forms.TextInput(attrs={'class':'edt_m'}),
        error_messages={'required': 'El Campo "Email" es obligatorio'}
    )
        #def __init__(self, *args, **kwargs):
            #"""
            #Todo esto de redefinir el constructor para
            #que el campo matricula no sea obligatorio
            #"""
            #super(ChangeUserInformationForm, self).__init__(*args, **kwargs)
            #self.fields['matricula'].required = False