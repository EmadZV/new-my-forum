from django import forms
from .models import PostModel, CommentModel, AnswerModel


class PostCreateForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = PostModel
        fields = ('title', 'body', 'image',)


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ('body',)


class AnswerCreateForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ('body',)
