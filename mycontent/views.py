from django.shortcuts import render
from mycontent.forms import PostCreateForm
from mycontent.models import PostModel


def landing_page(request):
    return render(request, 'mycontent/landing_page.html', )


def post_create(request):
    new_post = None

    if request.method == 'POST':
        form = PostCreateForm(data=request.POST)
        if form.is_valid():
            new_post = form
            new_post.save()
    else:
        form = PostCreateForm(request.POST)
    return render(request, 'mycontent/post_create.html', context={'form': form,
                                                                  'newpost': new_post})


def post_list(request):
    posts = PostModel.objects.all()
    return render(request, 'mycontent/post_list.html', context={'posts': posts})
