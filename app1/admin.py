from django.contrib import admin
from .models import User, Category, Blog, Comment
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Blog)
admin.site.register(Comment)