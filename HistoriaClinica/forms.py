#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django import forms
from django.contrib.auth.models import User

from HistoriaClinica.models import *
from globals import *



class AntecedentesPerinatalesForm(forms.ModelForm):
    """
    """
    class Meta:
        model = AntecedentesPerinatales
        fields = (
            'pregnancy_number',
            'pregnancy_duration',
            'controls',
            'normal_birth',
            'weight',
            'size',
            'pathologies',
            'medical_care',
            'coments',
        )
        widgets = {
            'pregnancy_number': forms.TextInput({'class':'edt_c'}),
            'pregnancy_duration': forms.TextInput({'class':'edt_c'}),
            'weight': forms.TextInput({'class':'edt_c'}),
            'size': forms.TextInput({'class':'edt_c'}),
            'coments': forms.Textarea(attrs={'cols':'52', 'rows':'5'}),
        }



class ToxicHabitsForm(forms.ModelForm):
    """
    """
    class Meta:
        model = ToxicHabits
        fields = (
                'snuff',
                'alcohol',
                'drugs',
                'infusions',
                'observations',
        )
        widgets = {
            'observations': forms.Textarea(attrs={'cols':'52', 'rows':'5'}),
        }



class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = (
            'title',
            #'date', #es automatico
            'content',
            'image',
        )
        widgets = {
            'title': forms.TextInput({'class':'edt_g'}),
            'content': forms.Textarea(attrs={'cols':'52', 'rows':'5'}),
        }



class BasicExamForm(forms.ModelForm):
    class Meta:
        model = BasicExam

        fields = (
            'body_temperature',
            'sistolic_blood_pressure',
            'diastolic_blood_pressure',
            'respiratory_rate',
            #'pulse',
            'average_weight',
            'average_height',
            'weight',
            'height',
            #'size',
            'bmi',
            'general_impression',
        )

        widgets = {
            'body_temperature': forms.TextInput(attrs={'class':'edt_c'}),
            'sistolic_blood_pressure': forms.TextInput(attrs={'class':'edt_c'}),
            'diastolic_blood_pressure': forms.TextInput(attrs={'class':'edt_c'}),
            'respiratory_rate': forms.TextInput(attrs={'class':'edt_c'}),
            #'pulse': forms.TextInput(attrs={'class':'edt_c'}),
            'average_weight': forms.TextInput(attrs={'class':'edt_c'}),
            'average_height': forms.TextInput(attrs={'class':'edt_c'}),
            'weight': forms.TextInput(attrs={'class':'edt_c'}),
            'height': forms.TextInput(attrs={'class':'edt_c'}),
            #'size': forms.TextInput(attrs={'class':'edt_c'}),
            'bmi': forms.TextInput(attrs={'class':'edt_c'}),
            'general_impression': forms.Textarea(attrs={'cols':'62', 'rows':'5'}),
        }



class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = [
            'title',
            'content',
            'image',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class':'edt_g'}),
        }



class HeadExamForm(forms.ModelForm):
    class Meta:
        model = HeadExam
        exclude = [
            'patient',
            'date',
        ]
        widgets = {
            'observations' : forms.Textarea(attrs={'cols':'62', 'rows':'5'}),
        }



class NeckExamForm(forms.ModelForm):
    class Meta:
        model = NeckExam
        exclude = [
            'patient',
            'date'
        ]
        comments = {
            'observations' : forms.Textarea(attrs={'cols':'62', 'rows':'5'}),
        }



class PFTSExamForm(forms.ModelForm):
    class Meta:
        model = PFTSExam
        exclude = [
            'patient',
            'date'
        ]
        widgets = {
            'aspect' : forms.Textarea(attrs={'cols':'62', 'rows':'3'}),
            'pilosa_distribution' : forms.Textarea(attrs={'cols':'62', 'rows':'3'}),
            'injuries' : forms.Textarea(attrs={'cols':'62', 'rows':'3'}),
            'appendages' : forms.Textarea(attrs={'cols':'62', 'rows':'3'}),
            'subcutaneous_tissue' : forms.Textarea(attrs={'cols':'62', 'rows':'3'}),
        }



class OsteoArticularExamForm(forms.ModelForm):
    class Meta:
        model = OsteoArticularExam
        exclude = [
            'patient',
            'date'
        ]
        widgets = {
            'vertebra_column' : forms.Textarea(attrs={'cols':'62', 'rows':'3'}),
            'bone_axles' : forms.Textarea(attrs={'cols':'62', 'rows':'3'}),
            'joints' : forms.Textarea(attrs={'cols':'62', 'rows':'3'}),
            'members' : forms.Textarea(attrs={'cols':'62', 'rows':'3'}),
            'muscular_tropism' : forms.Textarea(attrs={'cols':'62', 'rows':'3'}),
            #'' : forms.Textarea(attrs={'cols':'62', 'rows':'3'}),
        }



class RespiratorySystemExamForm(forms.ModelForm):
    class Meta:
        model = RespiratorySystemExam
        exclude = [
            'patient',
            'date'
        ]
        widgets = {
            'breast' : forms.Textarea(attrs={'cols':'62', 'rows':'3'}),
            'comments' : forms.Textarea(attrs={'cols':'62', 'rows':'3'}),
        }



class CardiovascularSystemExamForm(forms.ModelForm):
    class Meta:
        model = CardiovascularSystemExam
        exclude = [
            'patient',
            'date'
        ]
        widgets = {
            'comments' : forms.Textarea(attrs={'cols':'60', 'rows':'3'}),
        }



class ImageInfoForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = [
            'image',
            'date',
            'patient',
            'medic',
        ]
        widgets = {
            'title' : forms.TextInput(attrs={'class':'edt_g'}),
            'content' : forms.Textarea(attrs={'cols':'60', 'rows':'3'}),
        }



class UserModelChoiceField(forms.ModelChoiceField):
    """
        Redefinido un model ChoiceField para cambiar la etiqueta que tiene que
        mostrar
    """
    def label_from_instance(self, obj):
        return "%s %s" %(obj.first_name, obj.last_name)




class RelationForm(forms.ModelForm):           

    def __init__(self, patient, *args, **kwargs):
        super(RelationForm, self).__init__(*args, **kwargs)        
        self.fields['kin'] = UserModelChoiceField(queryset=User.objects.filter(groups__name='Paciente').exclude(username=patient), to_field_name='username')

        for key in self.fields:
            self.fields[key].required = False


    class Meta:
        model = Relation
        exclude = [
            'patient',
        ]
        widgets = {
            #'kin' : forms.ModelChoiceField(queryset=User.objects.filter(groups__name='Paciente'), to_field_name=None, empty_label=None)        
        }
