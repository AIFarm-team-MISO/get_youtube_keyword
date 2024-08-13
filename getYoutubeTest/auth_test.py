from google.oauth2 import service_account
import os

# 서비스 계정 키 파일 경로
KEY_FILE_LOCATION = "../auth/client_secret_112823576119-ee88o9973m1uiqeu4otj3kc031jvhspt.apps.googleusercontent.com.json"

# 서비스 계정 키 파일 경로 설정
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'client_secret_112823576119-ee88o9973m1uiqeu4otj3kc031jvhspt.apps.googleusercontent.com.json'

# Credentials 객체 생성
creds = service_account.Credentials.from_service_account_file('client_secret_112823576119-ee88o9973m1uiqeu4otj3kc031jvhspt.apps.googleusercontent.com.json', scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])


# 필요한 권한(scope)을 지정하여 자격 증명 객체를 만듦
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
#creds = None
#creds = service_account.Credentials.from_service_account_file(KEY_FILE_LOCATION, scopes=SCOPES)

from googleapiclient.discovery import build


# 자격 증명 객체를 이용하여 YouTube API 클라이언트를 빌드함
api_service_name = 'youtube'
api_version = 'v3'
youtube = build(api_service_name, api_version, credentials=creds)

# 채널 정보를 가져오는 API 요청을 호출함
channel_response = youtube.channels().list(
    part='snippet,statistics',
    id='UC_x5XG1OV2P6uZZ5FSM9Ttw'
).execute()

# 채널 정보 출력
print(channel_response['items'][0]['snippet']['title'])
print(channel_response['items'][0]['statistics']['subscriberCount'])