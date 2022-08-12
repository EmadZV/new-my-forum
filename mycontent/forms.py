from django import forms
from .models import PostModel


class PostCreateForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = PostModel
        fields = ('title', 'body', 'image')

