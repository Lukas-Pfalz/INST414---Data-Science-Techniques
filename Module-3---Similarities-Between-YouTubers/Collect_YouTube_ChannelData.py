import json
import os
from googleapiclient.discovery import build
import time

# Define Configuration - Using API Key
API_KEY = "AIzaSyChrMYb4zMwGyGyToPGvO0W2DLbsuCFcpQ"  # Replace with your real API key
# CHANNEL_NAME = "Veritasium"       # Replace with your desired channel name

# Local file to store analysis data
OUTPUT_FILE = "youtube_creator_data.json"
NUM_CHANNELS_ANALYZED = 50

# Initialize YouTube API client
youtube = build("youtube", "v3", developerKey=API_KEY)

# initialize data storage variables
channel_data = {}
video_ids = set()


# Helper method - Collect the Top-{Number of Channels} most popular videos on the given channel
def get_most_popular_videos(page_token=None):
    request = youtube.videos().list(
        part='snippet',
        chart='mostPopular',
        maxResults=NUM_CHANNELS_ANALYZED,
        regionCode='US',
        pageToken=page_token
    )
    return request.execute()


# Helper method - collecting Channel Data
def get_channels_data(channel_ids):
    request = youtube.channels().list(
        part='snippet,statistics',
        id=','.join(channel_ids),
        maxResults=50
    )
    return request.execute()

def search_channel_id(channel_name):
    """Search for a channel and return the channel ID."""
    request = youtube.search().list(
        part="snippet",
        q=channel_name,
        type="channel",
        maxResults=1
    )
    response = request.execute()
    if response["items"]:
        return response["items"][0]["snippet"]["channelId"]
    else:
        raise Exception("Channel not found.")

# Collect YouTube Channel - Data
next_page_token = None
while len(channel_data) < 1000:
    popular_response = get_most_popular_videos(next_page_token)

    channel_ids = []
    for video in popular_response['items']:
        vid_id = video['id']
        if vid_id not in video_ids:
            video_ids.add(vid_id)
            channel_id = video['snippet']['channelId']
            if channel_id not in channel_data:
                channel_ids.append(channel_id)

    if channel_ids:
        channels_response = get_channels_data(channel_ids)
        for item in channels_response['items']:
            cid = item['id']
            channel_data[cid] = {
                'title': item['snippet']['title'],
                'description': item['snippet'].get('description', ''),
                'publishedAt': item['snippet']['publishedAt'],
                'subscriberCount': item['statistics'].get('subscriberCount', '0'),
                'videoCount': item['statistics'].get('videoCount', '0'),
                'viewCount': item['statistics'].get('viewCount', '0'),
            }

    next_page_token = popular_response.get('nextPageToken')
    if not next_page_token:
        break

    time.sleep(1)  # Prevent quota overuse

yt_channels = list(channel_data.values())
