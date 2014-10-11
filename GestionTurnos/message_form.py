#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django import forms

from globals import *


class MessageToMedic(form.Form):
    to_user = None

    issue = forms.CharField(
        label="Asunto:",
        widget=forms.TextInput(attrs={'class':'edt_g',}),
        required = True
    )
    content = forms.CharField(
        label="Contenido:",
        widget= forms.Textarea(attrs={'cols':'45'}),
        required = True
    )


