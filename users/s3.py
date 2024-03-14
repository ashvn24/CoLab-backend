import boto3
from django.conf import settings
import uuid

def store_video_in_s3(video_file):
    s3 = boto3.client('s3',
                      aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
                      region_name=settings.AWS_S3_REGION_NAME)
    
    # Define S3 bucket and key prefix
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    key_prefix = 'work/'

    # Generate a unique key for the video file
    video_key = generate_unique_key()

    # Upload the video file to S3
    s3.upload_fileobj(video_file, bucket_name, f'{key_prefix}{video_key}')

    return f'{key_prefix}{video_key}'

def generate_unique_key():
    # Generate a random UUID as the unique key
    unique_key = str(uuid.uuid4())
    return unique_key

def download_video_from_s3(vid_key):
    s3 = boto3.client('s3',
                      aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
                      region_name=settings.AWS_S3_REGION_NAME)
    
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    # Download the video file from S3
    response = s3.get_object(Bucket=bucket_name, Key=vid_key)
    video_file = response['Body'].read()

    return video_file