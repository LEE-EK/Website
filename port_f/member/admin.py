from django.contrib import admin
from member.models import Member

class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'member_id', 'member_pw', 'nickname', 'member_name', 'address', 'address_in', 'phone_no', 'email', 'member_date')

admin.site.register(Member,MemberAdmin)



