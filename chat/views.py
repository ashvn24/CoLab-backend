from rest_framework.exceptions import NotFound
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import ChatRoom, Message

from .serializers import MessageSerializer
# Create your views here.


class MessageListView(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        user_id1 = self.kwargs['user_id1']
        user_id2 = self.kwargs['user_id2']
        try:
            chat_room = ChatRoom.objects.filter(
            Q(user1_id=user_id1, user2_id=user_id2) |
            Q(user1_id=user_id2, user2_id=user_id1)
        )
            print("------",chat_room)
            if not chat_room:  
                raise NotFound('Room not found')

            
            return Message.objects.filter(chat_room__in=chat_room).order_by('-timestamp') 
        except ChatRoom.DoesNotExist:  
            return Message.objects.none()
