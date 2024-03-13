from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from googleapiclient.http import MediaFileUpload
from .youtube_utils import get_authenticated_service

# Create your views here.

API_KEY = 'AIzaSyARxrS95japYaJM1IOiK9F8RgEE00DzI_Y'   
#API_KEY = 'AIzaSyBFH7YLCVwTf0j3CZSBa9OfAxslBLllksA'
#<<<<<<<<<<<<<<<<<<<<<<<--------------------------Channel Details---------------------------->>>>>>>>>>>>>>>>>>>>>>>
class GetAnalytics(APIView):
    def get(self, request):
        # Your YouTube Data API key
        api_key = API_KEY

        # Channel name of the YouTube channel you want to retrieve details for
        channel_name = self.request.query_params.get('channel_name',None)
        if not channel_name:
            return Response("Please provide a channel_name parameter in the request.", status=status.HTTP_400_BAD_REQUEST)

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
                    part='statistics,snippet',  # Include snippet part for channel's title and thumbnail
                    id=channel_id
                ).execute()

                # Extract statistics and snippet (including profile image) from the response
                if 'items' in channel_response:
                    channel_data = channel_response['items'][0]
                    channel_stats = channel_data['statistics']
                    channel_snippet = channel_data['snippet']

                    subscriber_count = channel_stats.get('subscriberCount', 0)
                    video_count = channel_stats.get('videoCount', 0)
                    view_count = channel_stats.get('viewCount', 0)
                    profile_image_url = channel_snippet.get('thumbnails', {}).get('default', {}).get('url', '')

                    # Construct the response data
                    response_data = {
                        'subscriber_count': subscriber_count,
                        'video_count': video_count,
                        'view_count': view_count,
                        'profile_image_url': profile_image_url
                    }

                    return Response(response_data)
                else:
                    return Response({'error': 'Channel statistics not found'}, status=404)
            else:
                return Response({'error': 'Channel not found'}, status=404)

        except Exception as e:
            return Response({'error': str(e)}, status=500)

        

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<-----------------Channel videos details---------------->>>>>>>>>>>>>>>>>>>>>>>>>
class ChannelVideosView(APIView):
    def get(self, request, format=None):
        channel_name = self.request.query_params.get('channel_name',None)
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
                view_count = video['view_count']
                data.append({
                    "title": title,
                    "video_id": video_id,
                    "like_count": like_count,
                    "comment_count": comment_count,
                    "view_count":view_count
                    
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

                view_count = statistics.get('viewCount', 0)

                video['statistics'] = statistics
                video['total_comments'] = total_comments
                video['view_count'] = view_count

            return videos

        except HttpError as e:
            print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
            return None

#<<<<<<<<<<<<<<<<---------------------------- Upload video directly------------------------------>>>>>>>>>>>>>>>>>>>>



class VideoUploadView(APIView):
    def post(self, request, *args, **kwargs):
        
        # Upload video to YouTube
        video_id = self.upload_to_youtube(request.data)

        if video_id:
            return Response({'video_id': video_id}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Failed to upload video'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def upload_to_youtube(self, video_data):
        youtube = get_authenticated_service("./owner_credentials.json")  # Use owner's credentials

        request_body = {
            'snippet': {
                'title': video_data.get('title'),
                'description': video_data.get('description'),
                'tags': video_data.get('tags')
            },
            'status': {
                'privacyStatus':'public',
            },
        }

        # Get the temporary file path
        video_file = video_data.get('video_file')
        video_path = video_file.temporary_file_path()

        media_file_upload = MediaFileUpload(video_path, chunksize=-1, resumable=True)

        try:
            videos_insert_response = youtube.videos().insert(
                part='snippet,status',
                body=request_body,
                media_body=media_file_upload
            ).execute()

            video_id = videos_insert_response['id']
            
            if video_id:
                os.remove("./owner_credentials.json")

            return Response (video_id, stattus=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error uploading video: {e}")
            return None
