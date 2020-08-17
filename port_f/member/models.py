from django.db import models


# member table
class Member(models.Model):
    objects = models.Manager()
    member_id = models.CharField(max_length=50)
    member_pw = models.CharField(max_length=200)
    nickname = models.CharField(max_length=50)
    member_name = models.CharField(max_length=50)
    address = models.CharField(max_length=200, blank=True)
    address_in = models.CharField(max_length=200, blank=True)
    phone_no = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    member_date = models.DateField('join_date', auto_now_add=True)

    def __str__(self):
        return self.nickname
