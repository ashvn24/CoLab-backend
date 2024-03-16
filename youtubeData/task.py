import time
from celery import shared_task

from backend.settings import BASE_DIR
from .youtube_utils import get_authenticated_service
from django.conf import settings
import boto3
import os
from googleapiclient.http import MediaFileUpload


@shared_task
def upload_to_youtube(video_data):
         # Get authenticated Youtube service
        try:
        # Get authenticated Youtube service
            youtube = get_authenticated_service("./owner_credentials.json")  # Use owner's credentials
            
            # Get video data
            video_title = video_data.get('title')
            video_description = video_data.get('description')
            video_tags = video_data.get('tags')
            
            # AWS S3 configuration
            s3 = boto3.client('s3',
                            aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
                            region_name=settings.AWS_S3_REGION_NAME)
            
            # Get the video file from S3
            video_file_key = video_data.get('vid_key')  # Key of the video file in S3 bucket
            print('file key-------',video_file_key)
            video_temp_path = os.path.join(BASE_DIR, 'youtubeData', 'temp', 'video.mp4')  # Temporary path to store the downloaded video file
            s3.download_file(settings.AWS_STORAGE_BUCKET_NAME, video_file_key, video_temp_path)
            
            # Prepare the request body for Youtube upload
            request_body = {
                'snippet': {
                    'title': video_title,
                    'description': video_description,
                    'tags': video_tags
                },
                'status': {
                    'privacyStatus': 'public',
                },
            }
            
            # Create media file upload object
            media_file_upload = MediaFileUpload(video_temp_path, chunksize=-1, resumable=True)
            
            # Execute Youtube video insert request
            videos_insert_response = youtube.videos().insert(
                part='snippet,status',
                body=request_body,
                media_body=media_file_upload
            ).execute()

            # Get video ID
            video_id = videos_insert_response['id']
            print('id',video_id)
            # Close the media file upload object
            media_file_upload.stream().close()
            if video_id:
                os.remove("./owner_credentials.json")
                return video_id

        except Exception as e:
            print(f"Error uploading video: {e}")
            return None

        finally:
            # Attempt to delete the temporary file
            time.sleep(30)  # Adjust the delay as needed
            try:
                os.remove(video_temp_path)
            except Exception as e:
                print(f"Error deleting temporary file: {e}")
