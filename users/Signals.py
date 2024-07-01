from django.db.models.signals import post_save,post_delete
from .models import User,UserProfile,Post
from django.dispatch import receiver
from django.core.cache import cache


@receiver(post_save, sender= User)
def create_profile(sender, instance, created, **kwargs):
    print('sender,instance,created',sender,instance,created)
    if created:
        UserProfile.objects.create(user= instance)
        
        
@receiver(post_save, sender=Post)
def clear_cache_on_save(sender, instance, **kwargs):
    cache_key = f'user_posts_{instance.user.id}'
    cache.delete(cache_key)

@receiver(post_delete, sender=Post)
def clear_cache_on_delete(sender, instance, **kwargs):
    cache_key = f'user_posts_{instance.user.id}'
    cache.delete(cache_key)