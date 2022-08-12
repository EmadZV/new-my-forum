from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
# from myauth.forms import CompleteUserForm


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


# def profile(request):
#     if request.method == 'POST':
#         form = CompleteUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Account Completed successfully')
#
#     else:
#         form = CompleteUserForm()
#
#     context = {
#         'form': form
#     }
#     return render(request, 'myauth/profile.html', context)
