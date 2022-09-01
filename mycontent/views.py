from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from mycontent.forms import PostCreateForm, CommentCreateForm, AnswerCreateForm, TagSearchForm
from mycontent.models import PostModel, AnswerModel, CommentModel, TagModel, VoteModel
from myauth.models import UserModel
from django.db.models import Count

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


def post_detail(request, year, month, day, post):
    new_comment = None
    new_answer = None
    post = get_object_or_404(PostModel, slug=post,
                             created__year=year,
                             created__month=month,
                             created__day=day)
    comment = post.post_comment.all()
    answer = post.post_answer.all()
    answerform = AnswerCreateForm(request.POST)
    commentform = CommentCreateForm(request.POST)
    user = request.user
    posttag = post.tag.all()
    similar_posts = post.get_similar_posts
    post_netvotes = post.get_post_netvotes
    answer_netvotes = []
    for obj in answer:
        answer_netvotes.append(obj.get_net_answer)
    if request.method == 'POST':

        if 'comment' in request.POST:
            commentform = CommentCreateForm(data=request.POST)
            if commentform.is_valid():
                new_comment = commentform.save(commit=False)
                new_comment.post = post
                new_comment.user = user
                new_comment.save()
        elif 'answer' in request.POST:
            answerform = AnswerCreateForm(data=request.POST)
            if answerform.is_valid():
                new_answer = answerform.save(commit=False)
                new_answer.post = post
                new_answer.user = user
                new_answer.save()

    return render(request, 'mycontent/post_detail.html', context={'post': post,
                                                                  'comment': comment,
                                                                  'answer': answer,
                                                                  'newcomment': new_comment,
                                                                  'newanswer': new_answer,
                                                                  'answerform': answerform,
                                                                  'commentform': commentform,
                                                                  'posttag': posttag,
                                                                  'similarpost': similar_posts,
                                                                  'postnet': post_netvotes,
                                                                  'answernet': answer_netvotes})


def tag_list(request):
    if request.method == 'POST':
        form = TagSearchForm(data=request.POST)
        if form.is_valid():
            taglist = TagModel.objects.filter(title__contains=form.cleaned_data['title'])
    else:
        form = TagSearchForm(request.POST)
        taglist = TagModel.objects.all()

    return render(request, 'mycontent/tag_list.html', context={'taglist': taglist,
                                                               'form': form})


def tag_detail(request, tag):
    obj = get_object_or_404(TagModel, title=tag)
    post = PostModel.objects.filter(tag=obj)
    return render(request, 'mycontent/tag_detail.html', context={'obj': obj,
                                                                 'post': post})


def vote_post(request, post_id, vote_value):
    voter = get_object_or_404(UserModel, user=request.user)
    post = get_object_or_404(PostModel, id=post_id)
    VoteModel.objects.create(post=post, voter=voter, vote=bool(vote_value), answer=None)
    return redirect(request.META.get('HTTP_REFERER'))


def vote_user(request, user_id, vote_value):
    pass


def vote_answer(request, answer_id, vote_value):
    voter = get_object_or_404(UserModel, user=request.user)
    answer = get_object_or_404(AnswerModel, id=answer_id)
    VoteModel.objects.create(answer=answer, voter=voter, vote=bool(vote_value), post=None)
    return redirect(request.META.get('HTTP_REFERER'))


def post_status(request, status_value, post_id):
    post = PostModel.objects.get(id=post_id)

    if status_value == 1:
        post.unlock

    else:
        post.lock

    return redirect('mycontent:post_list')

# def answer_status(request, answer_status_value, answer_id):
#     answer = AnswerModel.objects.get(id=answer_id)
#     if answer_status_value == 1:
#         answer.accepted = True
#         answer.save()
#     else:
#         answer.accepted = False
#         answer.save()
#
#     return redirect(request.META.get('HTTP_REFERER'))


# ---------------------------------------------------- #
#            1. add model property                     #
#            2. separate views                         #
#            3. deploy                                 #
# ---------------------------------------------------- #
