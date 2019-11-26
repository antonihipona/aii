from django import forms
from principal.models import Usuario, Director

class UserForm(forms.ModelForm):
    class Meta:    
        model = Usuario
        fields = "__all__"
        
class DirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = "__all__"