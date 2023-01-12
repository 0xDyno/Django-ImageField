from django import forms


class SaveForm(forms.Form):
    img = forms.ImageField()