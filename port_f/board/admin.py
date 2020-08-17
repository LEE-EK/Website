from django.contrib import admin
from board.models import Post
from board.models import Comment
from django_summernote.admin import SummernoteModelAdmin


class PostAdmin(SummernoteModelAdmin):
    list_display = ('id', 'subject', 'name', 'memo', 'hits', 'create_date')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post', 'text', 'created_date')
 
 
admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)

