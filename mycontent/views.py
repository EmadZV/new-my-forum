from django.contrib.auth import get_user_model
from django.shortcuts import render
from mycontent.forms import PostCreateForm, CommentCreateForm, AnswerCreateForm
from mycontent.models import PostModel, AnswerModel, CommentModel
from myauth.models import UserModel

User = get_user_model()


def landing_page(request):
    return render(request, 'mycontent/landing_page.html', )


def post_create(request):
    new_post = None
    user = request.user
    if request.method == 'POST':
        form = PostCreateForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)

            new_post.user = user
            new_post.save()
        else:
            print('is not valid', form.errors)
    else:
        form = PostCreateForm(request.POST)
    return render(request, 'mycontent/post_create.html', context={'form': form,
                                                                  'newpost': new_post})


def post_list(request):
    posts = PostModel.objects.all()
    return render(request, 'mycontent/post_list.html', context={'posts': posts})


def post_detail(request, post_id=1):
    new_comment = None
    new_answer = None
    post = PostModel.objects.get(id=post_id)
    # comment = CommentModel.objects.get(post=post_id)
    # CommentModel.post = post
    # answer = AnswerModel.objects.get()
    answerform = AnswerCreateForm(request.POST)
    commentform = CommentCreateForm(request.POST)
    if request.method == 'POST':

        if 'comment' in request.POST:
            commentform = CommentCreateForm(data=request.POST)
            if commentform.is_valid():
                new_comment = commentform.save(commit=False)
                new_comment.post = post
                new_comment.save()
        elif 'answer' in request.POST:
            answerform = AnswerCreateForm(data=request.POST)
            if answerform.is_valid():
                new_answer = answerform.save(commit=False)
                new_answer.post = post
                new_answer.save()

    return render(request, 'mycontent/post_detail.html', context={'post': post,
                                                                  'newcomment': new_comment,
                                                                  'newanswer': new_answer,
                                                                  'answerform': answerform,
                                                                  'commentform': commentform})
