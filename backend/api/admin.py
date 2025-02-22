from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile 
from .models import User
from .models import Todos
from .models import chatMessage


class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email']

class ProfileAdmin(admin.ModelAdmin):
    list_editable = ['verified']
    list_display = ['user','full_name','verified']

class TodosAdmin(admin.ModelAdmin):
    list_editable = ['completed']
    list_display = ['user','title','completed','date']

class chatMessageAdmin(admin.ModelAdmin):
    list_editable = ['is_read']
    list_display = ['sender','reciever','message','is_read']


admin.site.register(User,UserAdmin)
admin.site.register(Profile,ProfileAdmin)   
admin.site.register(Todos,TodosAdmin)
admin.site.register(chatMessage,chatMessageAdmin)       

