from django.contrib.auth import get_user_model
from django.shortcuts import render
from mycontent.forms import PostCreateForm
from mycontent.models import PostModel

User = get_user_model()


def landing_page(request):
    return render(request, 'mycontent/landing_page.html', )


def post_create(request):
    new_post = None
    user = PostModel.user
    if request.method == 'POST':
        form = PostCreateForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = user
            new_post.save()
    else:
        form = PostCreateForm(request.POST)
    return render(request, 'mycontent/post_create.html', context={'form': form,
                                                                  'newpost': new_post})


def post_list(request):
    posts = PostModel.objects.all()
    return render(request, 'mycontent/post_list.html', context={'posts': posts})
