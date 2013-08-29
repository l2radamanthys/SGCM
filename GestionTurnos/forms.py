#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django import forms

from globals import *


class RegisterForm(forms.Form):
    """
        Formulario de registro de usuarios paciente y/o administrativos
    """
    #login information
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
        widget=forms.TextInput(attrs={'class':'edt_m'}),
        error_messages={'required': 'El Campo "Email" es obligatorio'}
    )

    #user information
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
    birth_date =forms.DateField(
        label="Fecha de Nacimiento",
        widget=forms.DateInput(attrs={'class':'edt_c', 'id':'birth_date', 'value':'DD/MM/AAAA'}),
        input_formats= ['%d/%m/%Y'],
        error_messages={'required': 'El Campo "Fecha de Nacimiento" es obligatorio'}
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
    city = forms.CharField(
        label='Ciudad',
        widget=forms.TextInput(attrs={'class':'edt_m'}),
        required = False
    )
    state = forms.ChoiceField(label='Provincia', choices=ARG_STATES_CHOICE)
    phone = forms.CharField(
        label="Telefono",
        widget=forms.TextInput(attrs={'class':'edt_c'}),
        required = False
    )
    photo = forms.ImageField(
        label="Foto",
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


    #def clean(self):
        #cleaned_data = super(RegisterForm, self).clean()
        #_password = cleaned_data.get("password")
        #_re_password = cleaned_data.get("re_password")

        #if _password != _re_password:

            #self._errors["re_password"] = "Error las contrasenias no coinciden" #self.error_class(["Error las contrasenias no coinciden"])
            ##del cleaned_data["re_password"]

        #return cleaned_data



class MedicRegisterForm(RegisterForm):
    """
        Formulario de Registro de usuarios medicos
    """
    matricula = forms.CharField(
        label="Matricula",
        widget=forms.TextInput(attrs={'class':'edt_c'}),
        required = False
    )



class BasicInfoForm(forms.Form):
    """
	Formulario para modificacion de datos Basicos
    """
    email = forms.EmailField(
        label="Email (*)",
        widget=forms.TextInput(attrs={'class':'edt_m'}),
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

    city = forms.CharField(
        label='Ciudad',
        widget=forms.TextInput(attrs={'class':'edt_m'}),
        required = False
    )
    state = forms.ChoiceField(label='Provincia', choices=ARG_STATES_CHOICE)


    phone = forms.CharField(
        label="Telefono",
        widget=forms.TextInput(attrs={'class':'edt_c'}),
        required = False
    )
    photo = forms.ImageField(
        label="Foto",
        required = False
    )




class BusinessHoursForm(forms.Form):
    """
        Formulario para registrar Horario de atencion
    """
    date = forms.ChoiceField(label="Dia", choices=DATE_CHOICE)
    start_time = forms.CharField(
        label="Turno Inicia a las (HH:MM)",
        widget=forms.TextInput(attrs={'class':'edt_c', 'style':'text-align: center', 'value':'8:00'}),
        required = True
    )
    end_time = forms.CharField(
        label="Turno Termina a las (HH:MM)",
        widget=forms.TextInput(attrs={'class':'edt_c', 'style':'text-align: center', 'value':'10:00'}),
        required = True
    )
    turn_duration = forms.CharField(
        label="Duracion en Minutos",
        widget=forms.TextInput(attrs={'class':'edt_c', 'style':'text-align: center', 'value':'20'}),
        required = True
    )


    #def clean_start_time(self):
    #    pass



class MessageSendForm(forms.Form):
    to_user = forms.CharField(
        label="Destinatario:",
        widget=forms.TextInput(attrs={'class':'edt_g',}),
        required = True
    )
    issue = forms.CharField(
        label="Asunto:",
        widget=forms.TextInput(attrs={'class':'edt_g',}),
        required = True
    )
    content = forms.CharField(
        label="Contenido:",
        widget= forms.Textarea(attrs={'cols':'60'}),
        required = True
    )



class MessageReSendForm(forms.Form):
    content = forms.CharField(
        label="Contenido:",
        widget= forms.Textarea(attrs={'style':'width:650px'}),
        required = True
    )



class OnlineConsulationForm(forms.Form):
    issue = forms.CharField(
        label="Asunto:",
        widget=forms.TextInput(attrs={'class':'edt_g',}),
        required = True
    )

    content = forms.CharField(
        label="Contenido:",
        widget= forms.Textarea(attrs={'style':'width:400px'}),
        required = True
    )


