import string
import random
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags import humanize
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
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
    image = models.ImageField()
    tag = models.ManyToManyField(TagModel, )

    def save(self, *args, **kwargs):
        self.slug = self.generate_slug()
        return super().save(*args, **kwargs)

    def generate_slug(self, save_to_obj=False, add_random_suffix=True):
        """
        Generates and returns slug for this obj.
        If `save_to_obj` is True, then saves to current obj.
        Warning: setting `save_to_obj` to True
              when called from `.save()` method
              can lead to recursion error!

        `add_random_suffix ` is to make sure that slug field has unique value.
        """

        # We rely on django's slugify function here. But if
        # it is not sufficient for you needs, you can implement
        # you own way of generating slugs.
        generated_slug = slugify(self.title)

        # Generate random suffix here.
        random_suffix = ""
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

# class VoteModel(models.Model):
#     upvote = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
#     downvote = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
#     totalvote = models.PositiveIntegerField
#
#     def addvote(self):
#
#         def save(self, *args, **kwargs):  # new
#             if not self.:
#                 self.slug = slugify(self.title)
#             return super().save(*args, **kwargs)
#
#         def get_absolute_url(self):
#             return reverse('mycontent:tag_detail',
#                            args=[self.slug])
