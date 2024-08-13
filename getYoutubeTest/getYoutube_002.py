'''
OAuth 클라이언트

클라이언트 ID
112823576119-ee88o9973m1uiqeu4otj3kc031jvhspt.apps.googleusercontent.com

클라이언트 보안 비밀번호
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

'''



import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# Youtube API 인증 및 클라이언트 생성
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "../auth/client_secret_112823576119-ee88o9973m1uiqeu4otj3kc031jvhspt.apps.googleusercontent.com.json"



# Youtube API 클라이언트를 생성합니다.
def create_youtube_client():
    # 인증 흐름을 수행합니다.
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    #credentials = flow.run_console()
    creds = flow.run_local_server(port=0)

    # Youtube API 클라이언트를 생성합니다.
    youtube_client = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=creds)
    return youtube_client

# 검색어를 입력 받습니다.
search_word = input("검색어를 입력하세요: ")

# Youtube API 클라이언트를 생성합니다.
youtube = create_youtube_client()

# 검색 결과를 가져오기 위한 API 요청을 생성합니다.
request = youtube.search().list(
        part="id",
        q=search_word,
        type="video",
        maxResults=50,
        fields="items(id(videoId))"
)

# API 요청을 실행하고 검색 결과를 가져옵니다.
response = request.execute()

# 검색 결과에서 비디오 ID를 추출합니다.
video_ids = [item['id']['videoId'] for item in response['items']]

# 비디오 ID로부터 채널 ID를 추출합니다.
channel_ids = []
for video_id in video_ids:
    request = youtube.videos().list(
            part="snippet",
            id=video_id,
            fields="items(snippet(channelId))"
    )
    response = request.execute()
    channel_id = response['items'][0]['snippet']['channelId']
    channel_ids.append(channel_id)

# 채널 ID로부터 구독자 수를 추출합니다.
low_subscriber_channels = []
for channel_id in channel_ids:
    request = youtube.channels().list(
            part="statistics",
            id=channel_id,
            fields="items(statistics(subscriberCount))"
    )
    response = request.execute()
    subscriber_count = int(response['items'][0]['statistics']['subscriberCount'])
    if subscriber_count <= 100000:
        low_subscriber_channels.append(channel_id)

# 구독자 수가 10만 이하인 채널의 비디오 ID를 가져옵니다.
low_subscriber_videos = []
for channel_id in low_subscriber_channels:
    request = youtube.search().list(
            part="id",
            channelId=channel_id,
            type="video",
            maxResults=10,
            fields="items(id(videoId))"
    )
    response = request.execute()
    video_ids = [item['id']['videoId'] for item in response['items']]
    low_subscriber_videos.extend(video_ids)

# 결과 출력
print("구독자 수가 10만 이하인 채널의 비디오 ID:")
print(low_subscriber_videos)
