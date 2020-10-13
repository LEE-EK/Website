from django.db import models
from django.utils import timezone
from member.models import Member

# Notice table
class Notice(models.Model):
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

# Notice_Comment table
class Notice_Comment(models.Model):
    objects = models.Manager()
    author = models.ForeignKey('member.member', on_delete=models.CASCADE)
    post = models.ForeignKey('Notice', on_delete = models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

#######################################################################################################

# From_mark table
class From_mark(models.Model):
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

# From_mark_Comment table
class From_mark_Comment(models.Model):
    objects = models.Manager()
    author = models.ForeignKey('member.member', on_delete=models.CASCADE)
    post = models.ForeignKey('From_mark', on_delete = models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

#######################################################################################################

# To_mark table
class To_mark(models.Model):
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

# To_mark_Comment table
class To_mark_Comment(models.Model):
    objects = models.Manager()
    author = models.ForeignKey('member.member', on_delete=models.CASCADE)
    post = models.ForeignKey('To_mark', on_delete = models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

#######################################################################################################

# Freetalk table
class Freetalk(models.Model):
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

# Freetalk_Comment table
class Freetalk_Comment(models.Model):
    objects = models.Manager()
    author = models.ForeignKey('member.member', on_delete=models.CASCADE)
    post = models.ForeignKey('Freetalk', on_delete = models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text


#######################################################################################################

# Auth table
class Auth(models.Model):
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

# Auth_Comment table
class Auth_Comment(models.Model):
    objects = models.Manager()
    author = models.ForeignKey('member.member', on_delete=models.CASCADE)
    post = models.ForeignKey('Auth', on_delete = models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

#######################################################################################################

# Question table
class Question(models.Model):
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

# Question_Comment table
class Question_Comment(models.Model):
    objects = models.Manager()
    author = models.ForeignKey('member.member', on_delete=models.CASCADE)
    post = models.ForeignKey('Question', on_delete = models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text                         