import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from pytube import YouTube
from bs4 import BeautifulSoup
import re


# 검색어 입력받기
search_word = input("검색어를 입력하세요: ")

# YouTube API 인증 정보 설정
api_service_name = "youtube"
api_version = "v3"
api_key = "AIzaSyDZfPV3PIFTZJCEWB69OuL4dKHq7zENp9c" # 본인의 API 키 입력

# 인증 파일 경로 설정
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
auth_file_path = "../auth/pythonprojectyoutubetest-05151c0268b2.json"  # 본인의 인증 파일 경로 입력

# 인증 파일을 이용하여 YouTube API 클라이언트 생성
credentials = service_account.Credentials.from_service_account_file(auth_file_path, scopes=scopes)
youtube = build(api_service_name, api_version, developerKey=api_key, credentials=credentials)


# 검색어와 관련된 동영상 검색
'''
<order 매개변수에 값들>
date: 업로드 날짜순으로 정렬합니다. (기본값)
rating: 좋아요 순으로 정렬합니다.
relevance: 검색어와 관련도가 높은 순으로 정렬합니다.
title: 제목 순으로 정렬합니다.
videoCount: 채널의 동영상 갯수순으로 정렬합니다.
viewCount: 조회수가 많은 순으로 정렬합니다.
'''

# 영상 제목과 링크를 저장할 리스트
titles = []
video_urls = []


# YouTube API를 사용하여 검색결과 가져오기
search_response = youtube.search().list(
    q=search_word, # 검색할 키워드
    type='video', # 검색할 리소스 유형 (video, channel, playlist 중 선택)
   # videoDefinition='high', # 화질 (high, standard 중 선택)
   # videoDimension='3d', # 2D/3D 여부 (2d, 3d 중 선택)
   # videoDuration='any', # 동영상 길이 (long, medium, short 중 선택)
   #  order='viewCount', # 정렬 기준 (date, rating, viewCount 중 선택)
    maxResults=2, # 검색결과 수 (최대 50까지 가능)
   # fields='items(id(videoId),snippet(title,channelId))', # 가져올 필드 목록
    part='snippet,id'  # 'part' 매개변수 추가

    ).execute()


# 검색된 동영상 중에서 구독자 수가 10,000명 이하인 채널에서만 가져오기
for search_result in search_response.get('items', []):
    # 검색 결과의 종류가 동영상일 경우에만 처리
    if 'kind' in search_result['id'] and search_result['id']['kind'] == 'youtube#video':
        # 채널 정보 요청
        channel_response = youtube.channels().list(
            id=search_result['snippet']['channelId'],
            part='snippet,statistics'
        ).execute()

        # 채널의 구독자 수가 10,000명 이하인 경우에만 처리
        subscriber_count = int(channel_response['items'][0]['statistics']['subscriberCount'])
        if subscriber_count <= 1000000:
            titles.append(search_result['snippet']['title'])
            video_urls.append(f"https://www.youtube.com/watch?v={search_result['id']['videoId']}")

# 결과 출력
for i in range(len(titles)):
    print(f"{i+1}. {titles[i]}")
    print(f"   {video_urls[i]}")
    

'''
for search_result in search_response.get('items', []):
    video_id = search_result['id']['videoId']
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    video_title = search_result['snippet']['title']
    print(f"{video_title}: {video_url}")
'''