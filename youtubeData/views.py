from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Create your views here.

API_KEY = 'AIzaSyBFH7YLCVwTf0j3CZSBa9OfAxslBLllksA'
class GetAnalytics(APIView):
    def get(self, request):
        # Your YouTube Data API key
        
        api_key = API_KEY

        # Channel name of the YouTube channel you want to retrieve details for
        channel_name = request.data.get('channel_name')

        # Build the YouTube Data API service
        youtube = build('youtube', 'v3', developerKey=api_key)

        try:
            # Search for the channel by name
            search_response = youtube.search().list(
                part='snippet',
                q=channel_name,
                type='channel',
                maxResults=1
            ).execute()

            # Extract the channel ID from the search response
            if 'items' in search_response:
                channel_id = search_response['items'][0]['id']['channelId']

                # Retrieve channel statistics
                channel_response = youtube.channels().list(
                    part='statistics',
                    id=channel_id
                ).execute()

                # Extract statistics from the response
                if 'items' in channel_response:
                    channel_stats = channel_response['items'][0]['statistics']
                    subscriber_count = channel_stats.get('subscriberCount', 0)
                    video_count = channel_stats.get('videoCount', 0)
                    view_count = channel_stats.get('viewCount', 0)

                    # Construct the response data
                    response_data = {
                        'subscriber_count': subscriber_count,
                        'video_count': video_count,
                        'view_count': view_count
                    }

                    return Response(response_data)
                else:
                    return Response({'error': 'Channel statistics not found'}, status=404)
            else:
                return Response({'error': 'Channel not found'}, status=404)

        except Exception as e:
            return Response({'error': str(e)}, status=500)
        

class ChannelVideosView(APIView):
    def get(self, request, format=None):
        channel_name = request.data.get('channel_name', None)
        if not channel_name:
            return Response("Please provide a channel_name parameter in the request.", status=status.HTTP_400_BAD_REQUEST)

        videos = self.get_channel_videos(channel_name)
        if videos:
            data = []
            for video in videos[:10]:
                title = video['snippet']['title']
                video_id = video['snippet']['resourceId']['videoId']
                like_count = video['statistics'].get('likeCount', 0)
                comment_count = video['total_comments']
                data.append({
                    "title": title,
                    "video_id": video_id,
                    "like_count": like_count,
                    "comment_count": comment_count
                    
                })
            return Response(data,status=status.HTTP_200_OK)
        else:
            return Response("No videos found for the given channel name.", status=status.HTTP_404_NOT_FOUND)

    def get_channel_videos(self, channel_name):
        youtube = build('youtube', 'v3', developerKey=API_KEY)

        try:
            search_request = youtube.search().list(
                part='snippet',
                q=channel_name,
                type='channel'
            )
            search_response = search_request.execute()

            if not search_response['items']:
                return None

            channel_id = search_response['items'][0]['id']['channelId']

            channel_request = youtube.channels().list(
                part='contentDetails',
                id=channel_id
            )
            channel_response = channel_request.execute()

            if not channel_response['items']:
                return None

            uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

            videos = []
            next_page_token = None

            while len(videos) < 10:
                playlist_request = youtube.playlistItems().list(
                    part='snippet',
                    playlistId=uploads_playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                )
                playlist_response = playlist_request.execute()

                videos.extend(playlist_response['items'])

                next_page_token = playlist_response.get('nextPageToken')

                if not next_page_token:
                    break

            for video in videos:
                video_id = video['snippet']['resourceId']['videoId']
                stats_request = youtube.videos().list(
                    part='statistics',
                    id=video_id
                )
                stats_response = stats_request.execute()
                statistics = stats_response['items'][0]['statistics']

                total_comments = 0
                next_page_token = None
                while True:
                    comments_request = youtube.commentThreads().list(
                        part='snippet',
                        videoId=video_id,
                        maxResults=100,
                        pageToken=next_page_token
                    )
                    comments_response = comments_request.execute()
                    total_comments += comments_response['pageInfo']['totalResults']
                    
                    next_page_token = comments_response.get('nextPageToken')
                    if not next_page_token:
                        break

                video['statistics'] = statistics
                video['total_comments'] = total_comments

            return videos

        except HttpError as e:
            print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
            return None
        