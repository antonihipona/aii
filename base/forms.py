from django import forms
from .models import Genre


class GenreModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class FilmForm(forms.Form):
    title = forms.CharField(
        label="Título",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False
    )
    genres = GenreModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Genre.objects.all(),
        to_field_name="name",
    )

class ActorForm(forms.Form):
    name = forms.CharField(
        label="Nombre",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False
    )