from django.contrib import admin
from .models import User,UserProfile,PostAttachment,Post,EditorRequest
# Register your models here.

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(PostAttachment)
admin.site.register(Post)
admin.site.register(EditorRequest)