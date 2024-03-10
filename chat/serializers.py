from rest_framework import serializers
from .models import *

class ChatroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id','user1','user2'] 
        
        
class MessageSerializer(serializers.ModelSerializer):
    chat_room = ChatroomSerializer(read_only=True)  

    class Meta:
        model = Message
        fields = ['id', 'chat_room', 'user', 'content','timestamp']
        
class SignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signal
        fields = ['id', 'sender', 'receiver', 'message', 'created_at']