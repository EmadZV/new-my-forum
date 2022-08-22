from django import forms
from .models import PostModel, CommentModel, AnswerModel, TagModel


class PostCreateForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = PostModel
        fields = ('title', 'body', 'image',)


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ('cbody',)


class AnswerCreateForm(forms.ModelForm):
    class Meta:
        model = AnswerModel
        fields = ('abody',)


class TagSearchForm(forms.ModelForm):
    class Meta:
        model = TagModel
        fields = ('title', )
