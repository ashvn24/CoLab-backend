from django.contrib import admin
from .models import User,UserProfile,PostAttachment,Post
# Register your models here.

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(PostAttachment)
admin.site.register(Post)