from django import forms
from django.forms import ModelForm
from django.forms.widgets import TextInput

from .models import *


class ColorForm(ModelForm):
    class Meta:
        model = Color
        fields = "__all__"
        widgets = {
            "color_code": TextInput(attrs={"type": "color"}),
        }


class ExportOrder(forms.Form):
    date_from = forms.DateField(
        label="Почетна дата", widget=forms.widgets.DateInput(attrs={"type": "date"})
    )
    date_to = forms.DateField(
        label="Крајна дата", widget=forms.widgets.DateInput(attrs={"type": "date"})
    )
