from django.db import models
from users.models import User,EditorRequest,SubmitWork

# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    obj = models.ForeignKey(EditorRequest, related_name='post_notification', on_delete=models.CASCADE,blank=True, null=True)
    work = models.ForeignKey(SubmitWork, related_name='post_notification', on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return f'Notification for {self.user.username}'

    class Meta:
        ordering = ['-timestamp']
