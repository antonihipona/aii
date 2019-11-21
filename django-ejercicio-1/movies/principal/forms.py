from django import forms
from principal.models import Usuario

class UserForm(forms.ModelForm):
    class Meta:    
        model = Usuario
        fields = "__all__"
        