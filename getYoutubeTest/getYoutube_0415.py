"""
<API KEY>
AIzaSyDZfPV3PIFTZJCEWB69OuL4dKHq7zENp9c


YouTube Data API를 사용하려면 Google API Console에서 프로젝트를 만들고
해당 프로젝트에 YouTube Data API를 활성화하고 인증 정보를 생성해야 합니다.
이 과정에서 서비스 계정을 만들고 인증 파일을 다운로드하여 사용해야 합니다.
인증 파일은 Google Cloud Console에서 제공하는 서비스 계정 키(JSON) 파일입니다.
이 파일을 사용하여 YouTube Data API 요청을 보낼 수 있습니다. 인증 파일이 없으면 API를 사용할 수 없습니다.
위 과정을 위해 만들었음
서비스 이름 계정 및 서비스 계정 ID : misotube-project

"""

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

creds = None
creds_file = '../auth/pythonprojectyoutubetest-05151c0268b2.json'  # 인증 파일 경로
if os.path.exists(creds_file):
    creds = service_account.Credentials.from_service_account_file(
        creds_file, scopes=SCOPES)

youtube = build('youtube', 'v3', credentials=creds)

# 검색어 입력 받기
query = input("검색어를 입력하세요: ")

# 검색 실행
search_response = youtube.search().list(
        q=query,
        type='video',
        part='id,snippet',
        maxResults=10  #숫자변경으로 가져오는 갯수 설정
    ).execute()

# 검색 결과 출력
for search_result in search_response.get('items', []):
    video_id = search_result['id']['videoId']
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    video_title = search_result['snippet']['title']
    print(f"{video_title}: {video_url}")