from django.db import models
from django.utils import timezone
from member.models import Member

# Post table
class Post(models.Model):
    objects = models.Manager()
    subject = models.CharField(max_length=45)
    name = models.CharField(max_length=50)
    memo = models.TextField(max_length=300)
    hits = models.PositiveIntegerField(default=0)
    create_date = models.DateField('create_date', auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.subject


# Comment table
class Comment(models.Model):
    objects = models.Manager()
    author = models.ForeignKey('member.member', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name='comments', on_delete = models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text


