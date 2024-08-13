from googleapiclient.discovery import build

# Google API 클라이언트를 빌드합니다.

import os

#api_key = os.getenv('API_KEY')
#api_key = 'AIzaSyDZfPV3PIFTZJCEWB69OuL4dKHq7zENp9c'
api_key = 'AIzaSyDOX3lrgtjw5ClyWTG2wmWTZwwtfvuHbXo'

def build_youtube_api():
    return build('youtube', 'v3', developerKey=api_key)