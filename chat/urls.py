from . import views
from django.urls import path
from .views import *


urlpatterns = [
    path('user/<int:user_id1>/<int:user_id2>/', MessageListView.as_view(), name='chat-messages'),
]
