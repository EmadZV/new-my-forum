import string
import random
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags import humanize
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Count
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.conf import settings

# from myauth.models import UserModel
from myauth.models import UserModel


class TagModel(models.Model):
    # def generate_slug(self):
    #     generated_slug = slugify(self.title)
    #     return self.slug

    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('mycontent:tag_detail',
                       args=[self.slug])

    def __str__(self):
        return self.title


class PostModel(models.Model):
    STATUS = (
        ('locked', 'Locked'),
        ('open', 'Open')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_post',
                             default=None)
    title = models.CharField(max_length=64)
    slug = models.SlugField(null=True, blank=True, unique=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS, max_length=6, default='open')
    image = models.ImageField(default=None)
    tag = models.ManyToManyField(TagModel, )

    def save(self, *args, **kwargs):
        self.slug = self.generate_slug()
        return super().save(*args, **kwargs)

    def generate_slug(self, save_to_obj=False, add_random_suffix=True):
        generated_slug = slugify(self.title)
        if add_random_suffix:
            random_suffix = ''.join([
                random.choice(string.ascii_letters + string.digits)
                for i in range(5)
            ])
            generated_slug += '-%s' % random_suffix

        if save_to_obj:
            self.slug = generated_slug
            self.save(update_fields=['slug'])

        return generated_slug

    def get_absolute_url(self):
        return reverse('mycontent:post_detail',
                       args=[self.created.year,
                             self.created.month,
                             self.created.day, self.slug])

    def get_date(self):
        return humanize.naturaltime(self.updated)

    @property
    def lock(self):
        self.status = 'locked'
        return self.save()

    @property
    def unlock(self):
        self.status = 'open'
        return self.save()

    @property
    def get_similar_posts(self):
        posttag = self.tag.all()
        post_tags_ids = self.tag.values_list('id', flat=True)
        similar_posts = PostModel.objects.filter(tag__in=post_tags_ids).exclude(id=self.id).distinct()
        similar_posts = similar_posts.annotate(same_tags=Count('tag')).order_by('-same_tags', '-created')
        return similar_posts

    @property
    def get_post_netvotes(self):
        post_upvotes = self.votemodel_set.filter(vote=True).count()
        post_downvotes = self.votemodel_set.filter(vote=False).count()
        return post_upvotes - post_downvotes

    def __str__(self):
        return self.title


class AcceptedAnswerManager(models.Manager):
    def get_queryset(self):
        return super(AcceptedAnswerManager,
                     self).get_queryset() \
            .filter(accepted=True)


class AnswerModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_answer', default=None)
    abody = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='post_answer', default=None)
    image = models.ImageField()
    accepted = models.BooleanField(default=False)
    objects = models.Manager()
    ok = AcceptedAnswerManager()

    def __str__(self):
        return self.abody

    @property
    def get_net_answer(self):
        answer_upvotes = self.votemodel_set.filter(vote=True).count()
        answer_downvotes = self.votemodel_set.filter(vote=False).count()
        return answer_upvotes - answer_downvotes


class CommentModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='post_comment', null=True)
    answer = models.ForeignKey(AnswerModel, on_delete=models.CASCADE, related_name='answer_comment', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment', null=True, default=None)
    cbody = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_date(self):
        return humanize.naturaltime(self.created, self.updated)

    def __str__(self):
        return self.cbody


class CustomModelManager(models.Manager):
    def create(self, *args, **kwargs):
        # model_type, voter, vote = model_type, obj_data.get('voter'), obj_data.get('vote')
        voter, newvote = kwargs.get('voter'), kwargs.get('vote')

        # if kwargs['post']:
        post = kwargs['post']
        # elif kwargs['answer']:
        answer = kwargs['answer']
        # answer_id = obj_data['answer_id']
        if answer:
            myvote = VoteModel.objects.filter(voter=voter, answer=answer)
        elif post:
            myvote = VoteModel.objects.filter(voter=voter, post=post)
        else:
            myvote = None
        # VoteModel.objects.create(post=post, voter=voter, vote=bool(vote_value), model_type='post')
        # import pdb;
        # pdb.set_trace()
        # aya in usere object vote dare baraye in object feli
        if myvote.exists():

            prevvote = myvote.values_list('vote', flat=True).last()
            # import pdb;
            # pdb.set_trace()
            if prevvote == newvote:
                myvote.delete()

            elif prevvote != newvote:
                myvote.delete()
                super(CustomModelManager, self).create(*args, **kwargs)
        else:
            super(CustomModelManager, self).create(*args, **kwargs)


class VoteModel(models.Model):
    voter = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='votes', unique=False)
    vote = models.BooleanField()

    post = models.ForeignKey(PostModel, null=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(AnswerModel, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, null=True, on_delete=models.CASCADE)

    objects = CustomModelManager()

    #
    # def get_absolute_url(self):
    #     return reverse('mycontent:tag_detail',
    #                    args=[self.slug])
