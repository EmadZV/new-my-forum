from django import forms
from myauth.models import UserModel


class CompleteUserForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('age', 'gender', 'phone_number', 'profile_image',)

# class AnswerForm(forms.ModelForm):
