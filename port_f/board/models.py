from django.db import models
from django.utils import timezone
from member.models import Member

#장고는 클래스 메소드를 사용하는 대신, 별도의 Manager클래스를 정의하고 
#Manager클래스의 메소드를 통해서 테이블에 대한 CRUD동작을 수행합니다.

#모든 모델은 반드시 Manager속성을 가져한다
# ex)Album.object.all() 처럼 QuerySet객체를 반환하여 쓸수있습니다 all(),filter()등등

# Notice table
class Notice(models.Model):
    objects = models.Manager()
    subject = models.CharField(max_length=45)
    name = models.CharField(max_length=50)
    memo = models.TextField(max_length=300)
    hits = models.PositiveIntegerField(default=0)
    create_date = models.DateField('create_date', auto_now_add=True)

    class Meta:
        ordering = ['-id'] #(-)내림차순

    def __str__(self):#객체의 문자열 메소드
        return self.subject

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

#######################################################################################################

# Inquiry table
class Inquiry(models.Model):
    objects = models.Manager()
    author = models.ForeignKey('member.member', on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
       
# Inquiry_Comment table
class Inquiry_Comment(models.Model):
    objects = models.Manager()
    author = models.ForeignKey('member.member', on_delete=models.CASCADE)
    post = models.ForeignKey('Inquiry', on_delete = models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text



#######################################################################################################

# Report table
class Report(models.Model):
    objects = models.Manager()
    author = models.ForeignKey('member.member', on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text


# Report_Comment table
class Report_Comment(models.Model):
    objects = models.Manager()
    author = models.ForeignKey('member.member', on_delete=models.CASCADE)
    post = models.ForeignKey('Report', on_delete = models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text        