import json
import os
from googleapiclient.discovery import build

# ======================
# CONFIG
# ======================
API_KEY = "AIzaSyChrMYb4zMwGyGyToPGvO0W2DLbsuCFcpQ"  # Replace with your real API key
CHANNEL_NAME = "Veritasium"       # Replace with your desired channel name
CHANNEL_STAT_DATA_FILE = "channel_data.json" # Local file to store analysis data
TOP_RANK_CREATORS_FILE = "list_top_ranked_creators.json"

NUM_CHANNELS_ANALYZED = 5

# ======================
# INITIATE YOUTUBE CLIENT
# ======================
youtube = build("youtube", "v3", developerKey=API_KEY)

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

def get_channel_statistics(channel_id):
    """Get channel stats like subscriber count, views, etc."""
    request = youtube.channels().list(
        part="snippet,statistics,contentDetails",
        id=channel_id
    )
    response = request.execute()
    if response["items"]:
        return response["items"][0]
    else:
        raise Exception("Unable to fetch channel data.")

def save_to_file(data, filename):
    """Save data as JSON for local analysis."""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")




# Helper method - Collect the Top-{Number of Channels} most popular videos on the given channel
def get_most_popular_videos(page_token=None):
    request = youtube.channels().list(
        part='snippet',
        chart='mostPopular',
        maxResults=NUM_CHANNELS_ANALYZED,
        regionCode='US',
        pageToken=page_token
    )
    return request.execute()


try:
    top_yt_creator_list_data = get_most_popular_videos()


    # Display / Save the Data of the formatted list of Top-Ranked YouTubers
    print(f"Top YouTube creators - Ranked - retrieved from API:\n\n {top_yt_creator_list_data}")
    save_to_file(top_yt_creator_list_data, TOP_RANK_CREATORS_FILE)

    #
    channel_id = search_channel_id(CHANNEL_NAME)
    print(f"\n\nFound Channel ID:\n\n{channel_id}")
    data = get_channel_statistics(channel_id)
    save_to_file(data, CHANNEL_STAT_DATA_FILE)

except Exception as e:
    print(f"Error: {e}")

