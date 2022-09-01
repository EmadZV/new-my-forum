from django.contrib import admin

from mycontent.models import PostModel, CommentModel, AnswerModel, TagModel, VoteModel

admin.site.register(PostModel),
admin.site.register(AnswerModel),
admin.site.register(CommentModel),
admin.site.register(TagModel),
admin.site.register(VoteModel),


