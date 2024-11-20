# -*- coding: utf-8 -*-
"""YoutubeProject.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kB-NkcHmctVP6sKjqw4IFUfWEvIJAetx
"""

# Required Libraries
# Run these in Google Colab before starting
#pip install google-api-python-client streamlit mysql-connector-python pandas

# Import necessary libraries
import os
import pandas as pd
import streamlit as st
import mysql.connector
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set up YouTube API credentials
# IMPORTANT: Replace with your actual API key
YOUTUBE_API_KEY = 'AIzaSyCbsylYsnG56BFGVfSB739_h4WCEaooMRA'

# Create YouTube API client
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def get_channel_details(youtube, channel_id):
    """
    Retrieve detailed information for a YouTube channel
    """
    channel_response = youtube.channels().list(
        part='snippet,statistics,contentDetails',
        id=channel_id
    ).execute()

    if not channel_response['items']:
        return None

    channel_data = channel_response['items'][0]

    channel_info = {
        'channel_id': channel_id,
        'channel_name': channel_data['snippet']['title'],
        'subscribers': channel_data['statistics'].get('subscriberCount', 'Not Available'),
        'total_videos': channel_data['statistics'].get('videoCount', 'Not Available'),
        'playlist_id': channel_data['contentDetails']['relatedPlaylists']['uploads']
    }

    return channel_info

def get_video_details(youtube, playlist_id):
    """
    Retrieve video details from a channel's upload playlist
    """
    video_details = []
    next_page_token = None

    while True:
        playlist_response = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in playlist_response['items']:
            video_id = item['snippet']['resourceId']['videoId']

            video_stats = youtube.videos().list(
                part='statistics,snippet',
                id=video_id
            ).execute()

            video_info = video_stats['items'][0]

            video_data = {
                'video_id': video_id,
                'channel_id': item['snippet']['channelId'],
                'video_title': item['snippet']['title'],
                'published_at': item['snippet']['publishedAt'],
                'likes': video_info['statistics'].get('likeCount', 0),
                'comments': video_info['statistics'].get('commentCount', 0)
            }

            video_details.append(video_data)

        next_page_token = playlist_response.get('nextPageToken')
        if not next_page_token:
            break

    return video_details

def create_mysql_connection():
    """
    Establish MySQL connection
    """
    connection = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace with your MySQL username
        password='Shriyantra@01',  # Replace with your MySQL password
        database='youtube_data'  # Database name
    )
    return connection

def create_tables(connection):
    """
    Create necessary tables in MySQL
    """
    cursor = connection.cursor()

    # Create Channels Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS channels (
        channel_id VARCHAR(255) PRIMARY KEY,
        channel_name VARCHAR(255),
        subscribers INT,
        total_videos INT,
        playlist_id VARCHAR(255)
    )
    ''')

    # Create Videos Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS videos (
        video_id VARCHAR(255) PRIMARY KEY,
        channel_id VARCHAR(255),
        video_title VARCHAR(255),
        published_at DATETIME,
        likes INT,
        comments INT,
        FOREIGN KEY (channel_id) REFERENCES channels(channel_id)
    )
    ''')

    connection.commit()
    cursor.close()

import streamlit as st

def main():
    st.title('YouTube Channel Data Analysis')

    # Sidebar for channel input
    st.sidebar.header('Channel Data Collection')
    channel_ids = st.sidebar.text_area('Enter YouTube Channel IDs (one per line)')

    if st.sidebar.button('Collect Channel Data'):
        # Split channel IDs and process
        channels = [ch.strip() for ch in channel_ids.split('\n') if ch.strip()]

        if len(channels) > 10:
            st.error('Maximum 10 channels allowed!')
            return

        collected_data = []

        # Collect data for each channel
        for channel_id in channels:
            channel_info = get_channel_details(youtube, channel_id)
            if channel_info:
                videos = get_video_details(youtube, channel_info['playlist_id'])

                # Store in MySQL
                connection = create_mysql_connection()
                cursor = connection.cursor()

                # Insert channel data
                cursor.execute('''
                    INSERT INTO channels
                    (channel_id, channel_name, subscribers, total_videos, playlist_id)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (
                    channel_info['channel_id'],
                    channel_info['channel_name'],
                    channel_info['subscribers'],
                    channel_info['total_videos'],
                    channel_info['playlist_id']
                ))

                # Insert video data
                for video in videos:
                    cursor.execute('''
                        INSERT INTO videos
                        (video_id, channel_id, video_title, published_at, likes, comments)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    ''', (
                        video['video_id'],
                        video['channel_id'],
                        video['video_title'],
                        video['published_at'],
                        video['likes'],
                        video['comments']
                    ))

                connection.commit()
                cursor.close()
                connection.close()

                collected_data.append(channel_info)

            st.success(f'Data collected for {len(collected_data)} channels')

    # Data Exploration Section
    st.sidebar.header('Data Exploration')
    exploration_option = st.sidebar.selectbox('Choose Exploration Type', [
        'View Channels',
        'View Videos',
        'Channel Video Count',
        'Top Liked Videos'
    ])

    # Add more detailed exploration queries here based on selected option

if __name__ == '__main__':
    main()

