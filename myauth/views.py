from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
# from myauth.forms import CompleteUserForm
from myauth.forms import CompleteUserForm
from myauth.models import UserModel
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


def user_page(request, userpage):
    user = get_object_or_404(UserModel, user__username=userpage)
    visiter = get_object_or_404(UserModel, user=request.user)
    if visiter == user:
        editor_mode = True
    # else:
    #     follower=
    #     following=
    # user_posts=
    # user_comments=
    # user_answers=

    # import pdb;
    # pdb.set_trace()

    pass
