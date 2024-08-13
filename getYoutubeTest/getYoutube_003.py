import os
import google.auth
from googleapiclient.discovery import build

from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
creds = None
creds_file = '../auth/pythonprojectyoutubetest-05151c0268b2.json'  # 인증 파일 경로
if os.path.exists(creds_file):
    creds = service_account.Credentials.from_service_account_file(
        creds_file, scopes=SCOPES)

youtube = build('youtube', 'v3', credentials=creds)

# Youtube API client initialization
youtube = build('youtube', 'v3', credentials=creds)

# Keyword to search for
keyword = '세키로'

# Search for videos with given keyword and get the channel ids
search_response = youtube.search().list(
    q=keyword,
    type='video',
    part='id,snippet',
    maxResults=10
).execute()

video_ids = []
channel_ids = []

for search_result in search_response.get('items', []):
    if search_result['id']['kind'] == 'youtube#video':
        video_ids.append(search_result['id']['videoId'])
        channel_ids.append(search_result['snippet']['channelId'])

# Get channel statistics and filter channels with less than 100k subscribers
channels_statistics = youtube.channels().list(
    part='statistics',
    id=','.join(channel_ids)
).execute()


channels = []
for channel in channels_statistics['items']:
    if int(channel['statistics']['subscriberCount']) <= 100000:
        channels.append(channel['id'])

# Get video ids from the filtered channels
video_ids_filtered = []
for video_id in video_ids:
    video_response = youtube.videos().list(
        part='snippet,statistics',
        id=video_id
    ).execute()

    channel_id = video_response['items'][0]['snippet']['channelId']
    if channel_id in channels:
        video_ids_filtered.append(video_id)

# Print the filtered video ids
print(video_ids_filtered)


'''

youtube.channels().list()는 채널의 정보를 가져오기 위한 API 메소드이며, youtube.videos().list()는 비디오의 정보를 가져오기 위한 API 메소드입니다.

youtube.channels().list()를 사용하여 채널의 정보를 가져오면, 해당 채널의 아이디, 채널명, 구독자 수 등의 정보를 확인할 수 있습니다. 반면에, youtube.videos().list()를 사용하여 비디오의 정보를 가져오면, 해당 비디오의 아이디, 제목, 업로드 일시, 조회수, 좋아요 수, 댓글 수 등의 정보를 확인할 수 있습니다.

'''