from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
# from myauth.forms import CompleteUserForm
from myauth.forms import CompleteUserForm
from mycontent.models import AnswerModel, PostModel


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')

    else:
        form = UserCreationForm()

    context = {
        'form': form
    }
    return render(request, 'myauth/register.html', context)


def profile(request):
    user = request.user
    answer = AnswerModel.objects.filter(post__user=user)
    post = PostModel.objects.filter(user=user)
    if request.method == 'POST':
        form = CompleteUserForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            messages.success(request, 'Account Completed successfully')

    else:
        form = CompleteUserForm()

    context = {
        'form': form,
        'user': user,
        'answer': answer,
        'posts': post
    }
    return render(request, 'myauth/profile.html', context)
