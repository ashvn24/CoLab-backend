from django.db import models

from users.models import User

# Create your models here.

class Transaction(models.Model):
    sender = models.ForeignKey(User, related_name='razorpayment_sender', on_delete = models.CASCADE)
    reciever = models.ForeignKey(User, related_name='razorpayment_reciever', on_delete=models.CASCADE)
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    transacrtion_id = models.CharField(max_length=200)
    
    def __str__(self):
        return f'{self.reciever.username} to {self.sender.username}'