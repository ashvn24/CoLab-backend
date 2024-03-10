from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from googleapiclient.discovery import build
# Create your views here.

class GetAnalytics(APIView):
    def get(self,request):
        
        channelName = request.data.get('channel')
        print('------------',channelName)
        apiKey = 'AIzaSyBFH7YLCVwTf0j3CZSBa9OfAxslBLllksA'
        
        youtube = build(
            "youtube",  # API to use,
            'v3',
            developerKey=apiKey
            )

        request = youtube.channels().list(
            part = 'statistics',
            forUsername = channelName
            )
        response = request.execute()
        
        return Response(response,status=status.HTTP_200_OK)