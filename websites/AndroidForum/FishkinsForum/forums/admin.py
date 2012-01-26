from forums.models import Thread, Post
from django.contrib import admin

class PostInline(admin.StackedInline):
    model = Post
    extra = 1

class ThreadAdmin(admin.ModelAdmin):
    inlines = [PostInline]
    list_display = ('name', 'posted_by', 'created_on')

admin.site.register(Thread,ThreadAdmin)

