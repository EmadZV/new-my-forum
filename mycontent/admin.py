from django.contrib import admin

from mycontent.models import PostModel, CommentModel, AnswerModel, TagModel

admin.site.register(PostModel),
admin.site.register(AnswerModel),
admin.site.register(CommentModel),
admin.site.register(TagModel),


