from django import forms


class SaveFromPcForm(forms.Form):
    img = forms.ImageField(label=False)


class SaveFromUrlForm(forms.Form):
    attrs = {"style": "width: 80%;"}
    url = forms.CharField(widget=forms.TextInput(attrs=attrs), label=False)
