from django import forms


class ImportExcelForm(forms.Form):
    file = forms.FileField(label="Choose excel to upload")
