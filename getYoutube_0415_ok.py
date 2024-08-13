'''

<< 현재 진행상황 >>
먼저 검색어에 대한 YouTube 검색 API를 사용하여 비디오 ID 목록을 가져옵니다.
각 비디오 ID에 대해 YouTube 비디오 API를 사용하여 채널 ID를 가져옵니다.
가져온 채널 ID에 대해 YouTube 채널 API를 사용하여 구독자 수를 가져옵니다.
구독자 수가 10만 이하인 채널의 비디오 ID를 추출합니다.

<< 이후 할일 >>
1. 현재까지 키워드를 입력하면 유튜브 구독자 5000명 미만 채널의 영상중 조회수 1만 이상의 영상을 출력할수 있게 되었음
***** 어떤코드를 만들지 정하고 지피티에 백업내용을 알려준후에 시작하자

2. 지금도 계속해서 조회수가 상승하는지의 여부
3. 해당영상의 제목과 링크를 가져와 엑셀 파일로 저장

'''
import datetime
import argparse
from tool.getYoutubeStatistics import get_popularity_score
from tool.make_youtube_api import build_youtube_api
from tool.get_youtube_info import youtube_serch_list

# 검색어와 관련된 동영상 검색
'''
<order 매개변수에 값들>
date: 업로드 날짜순으로 정렬합니다. (기본값)
rating: 좋아요 순으로 정렬합니다.
relevance: 검색어와 관련도가 높은 순으로 정렬합니다.
title: 제목 순으로 정렬합니다.
videoCount: 채널의 동영상 갯수순으로 정렬합니다.
viewCount: 조회수가 많은 순으로 정렬합니다.

videoDefinition='high', # 화질 (high, standard 중 선택)
videoDimension='3d', # 2D/3D 여부 (2d, 3d 중 선택)
videoDuration='any', # 동영상 길이 (long, medium, short 중 선택)
order='viewCount', # 정렬 기준 (date, rating, viewCount 중 선택)
fields='items(id(videoId),snippet(title,channelId))', # 가져올 필드 목록

'''

# API 정보와 함께 인자 분석을 설정합니다.
parser = argparse.ArgumentParser()
parser.add_argument('--query', help='검색할 유튜브 비디오 검색어', default='Google Developers')
args = parser.parse_args()

youtube = build_youtube_api()
keyword = '힙업거들'


# 검색어에 대한 유튜브 list API를 사용하여 비디오 정보를 가져온다.
keyword_search_info = youtube_serch_list(youtube, keyword)

# 각 비디오 ID에 대해 YouTube 비디오 API를 사용하여 채널 ID를 가져옵니다.
channel_ids = []
video_titles = []


video_ids = []  # 키워드로 검색된 영상들의 아이디들
for search_result in keyword_search_info.get('items', []):
    video_ids.append(search_result['id']['videoId'])
    

'''
youtube.videos().list()를 사용하여 비디오의 정보를 가져오면, 해당 비디오의 아이디, 제목, 업로드 일시, 조회수, 좋아요 수, 댓글 수 등의 정보를 확인할 수 있습니다.
'''
for video_id in video_ids:
    video_response = youtube.videos().list(
        id=video_id,
        part='snippet'
    ).execute()
    channel_id = video_response['items'][0]['snippet']['channelId']
    video_title = video_response['items'][0]['snippet']['title']
    channel_ids.append(channel_id)
    video_titles.append(video_title)

'''
youtube.channels().list()는 채널의 정보를 가져오기 위한 API 메소드이며, youtube.videos().list()는 비디오의 정보를 가져오기 위한 API 메소드입니다.
youtube.channels().list()를 사용하여 채널의 정보를 가져오면, 해당 채널의 아이디, 채널명, 구독자 수 등의 정보를 확인할 수 있습니다.
'''
# 가져온 채널 ID에 대해 YouTube 채널 API를 사용하여 구독자 수를 가져옵니다.
sub_counts = []
for channel_id in channel_ids:
    channel_response = youtube.channels().list(
        id=channel_id,
        part='statistics'
    ).execute()
    sub_count = int(channel_response['items'][0]['statistics']['subscriberCount'])
    sub_counts.append(sub_count)

print(sub_counts)

# 구독자 수가 10만 이하인 채널의 비디오 ID를 추출합니다.
result_video_ids = []
result_video_titles = []
for i, sub_count in enumerate(sub_counts):
    if sub_count <= 100000:
        result_video_ids.append(video_ids[i])
        result_video_titles.append(video_titles[i])


# 각 비디오의 제목과 링크를 출력합니다.
print("<<< 10만이하의 채널들의 제목과 링크 >>>")
for i, video_id in enumerate(result_video_ids):
    video_url = f'https://www.youtube.com/watch?v={video_id}'
    print(f'{result_video_titles[i]}: {video_url}')

print("<<< 구독자가 10만이하, 조회수 5만이상 >>>")
#이런 경우에는 10만 이하인 채널에서 가져온 동영상 ID 목록에서 각 동영상의 조회수를 가져와야 합니다. 조회수를 가져오는 방법
result_videos_10_list = [] # 위내용 필터링된 영상

for video_id in result_video_ids:
    video_response = youtube.videos().list(
        id=video_id,
        part='snippet,statistics'
    ).execute()
    view_count = int(video_response['items'][0]['statistics']['viewCount'])
    if view_count >= 10000:
        video_title = video_response['items'][0]['snippet']['title']
        video_link = f'https://www.youtube.com/watch?v={video_id}'
        print(f'>> 구독자가 10만이하, 조회수 5만이상 영상들 >> 제목: {video_title}, 링크: {video_link}')

        # 여기까지 필터링된 영상들이 통계에 들어감
        result_videos_week = []

        channel_id = video_response['items'][0]['snippet']['channelId']
        view_count = int(video_response['items'][0]['statistics']['viewCount'])
        published_at = datetime.datetime.fromisoformat(video_response['items'][0]['snippet']['publishedAt'][:-1])
        title = video_response['items'][0]['snippet']['title']
        video_url = f'https://www.youtube.com/watch?v={video_id}'

        print('>> video_id(비디오아이디) : ' + video_id)
        print('>> channel_id(채널아이디) : ' + channel_id)
        print('>> view_count(조회수) : ' + str(view_count))
        print('>> published_at(업로드날짜) : ' + str(published_at))
        print('>> title(제목) : ' + title)


        is_higher = get_popularity_score(youtube,video_id)
        print(is_higher)




























'''
        맞습니다.youtube.videos().list()는
        publishedAfter파라미터를
        지원하지 않습니다.
        publishedAfter파라미터는 youtube.search().list()에서 사용할 수있습니다.

        따라서, youtube.videos().list()로
        해당 비디오의 정보를 가져온 후에는, 해당 비디오가 업로드된시간을 확인하여
        1주일 전의 시간을 계산하고, 다시
        youtube.search().list()를 사용하여 일주일 전의
        비디오 정보를 가져올 수있습니다.
        
        이내용을 바탕으로 다시한번 만들어보자. 
        
        '''


'''
        #### 현재 시간 구하기
        now = datetime.datetime.now()

        # 1주일(7일) 전 시간 구하기
        week_ago = now - datetime.timedelta(weeks=1)
        print(f' now : {now}')
        print(f' week_ago : {week_ago}')
        print(f' week_ago.isoformat() : {week_ago.isoformat()}')
        weeka = week_ago.strftime('%Y-%m-%dT%H:%M:%S%z')

        print(f' weeka : {weeka}')

        week_ago_response = youtube.search().list(
            type="video",
            part="id,snippet",
            fields="items(id(videoId),snippet(publishedAt,channelId,title))",
            channelId=video_id,
            publishedAfter=weeka,
            publishedBefore=weeka
        ).execute()
        
'''

'''
        # 일주일 전 비디오 정보 가져오기
        week_ago_response = youtube.search().list(
            id=video_id,
            part='statistics',
            fields='items(statistics(viewCount))',
            publishedAfter=weeka
        ).execute()
'''

        # 일주일 전 조회수 가져오기
        #week_ago_view_count = int(week_ago_response['items'][0]['statistics']['viewCount'])

        # 현재 조회수와 일주일 전 조회수 출력하기
        #print(f'현재 조회수: {view_count}')
        #print(f'일주일 전 조회수: {week_ago_view_count}')

'''
print(">> 위의 필터링된 내용을 리스트로 출력 <<")
#여기까지 필터링 된 영상을 result_videos_10_list 에 저장했음
for video_response in result_videos_10_list:
    video_title = video_response['items'][0]['snippet']['title']
    video_link = f'https://www.youtube.com/watch?v={video_id}'
    print(f'제목: {video_title}, 링크: {video_link}')
'''

    # 리스트에 담긴내용을 일단 출력해보자.


# 각 비디오 ID에 대해 YouTube 비디오 API를 사용하여 채널 ID와 통계 정보를 가져옵니다.
'''
view_count_week = []
for video_id in result_video_ids:
    video_response = youtube.videos().list(
        id=video_id,
        part='snippet, statistics'
    ).execute()

    
    channel_id = video_response['items'][0]['snippet']['channelId']
    view_count = int(video_response['items'][0]['statistics']['viewCount'])
    published_at = datetime.datetime.fromisoformat(video_response['items'][0]['snippet']['publishedAt'][:-1])
    title = video_response['items'][0]['snippet']['title']
    video_url = f'https://www.youtube.com/watch?v={video_id}'

    print('channel_id : ' + channel_id)
    print('view_count : ' + str(view_count))
    print('published_at : ' + str(published_at))
    print('title : ' + title)
    



    # 영상이 일주일 전에 업로드되었는지 확인합니다.
    if (datetime.datetime.now() - published_at).days <= 360: # 1년이내업로드
        # 일주일 전에 업로드된 영상이라면, 이전 주에 비해 조회수가 증가했는지 확인합니다.
        week_ago = published_at - datetime.timedelta(weeks=4) #4주전
        week_ago_view_count = youtube.videos().list(
            id=video_id,
            part='statistics',
            fields='items(statistics(viewCount))'
        ).execute()['items'][0]['statistics']['viewCount']
        week_ago_view_count = int(week_ago_view_count) if week_ago_view_count else 0
        if view_count - week_ago_view_count > 0:
            result_videos_week.append((title, video_url, view_count))

# 구독자 수가 10만 이하이면서 조회수가 1만 이상이고, 일주일간 조회수가 증가한 비디오들을 출력합니다.
for title, video_url, view_count in result_videos_week:
    print(f'{title} ({video_url}) - {view_count} views (last week)')

'''



'''

<<< OAuth 클라이언트 >>>

클라이언트 ID
112823576119-ee88o9973m1uiqeu4otj3kc031jvhspt.apps.googleusercontent.com

클라이언트 보안 비밀번호
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


<<<API KEY>>>
AIzaSyDZfPV3PIFTZJCEWB69OuL4dKHq7zENp9c

YouTube Data API를 사용하려면 Google API Console에서 프로젝트를 만들고
해당 프로젝트에 YouTube Data API를 활성화하고 인증 정보를 생성해야 합니다.
이 과정에서 서비스 계정을 만들고 인증 파일을 다운로드하여 사용해야 합니다.
인증 파일은 Google Cloud Console에서 제공하는 서비스 계정 키(JSON) 파일입니다.
이 파일을 사용하여 YouTube Data API 요청을 보낼 수 있습니다. 인증 파일이 없으면 API를 사용할 수 없습니다.
위 과정을 위해 만들었음
서비스 이름 계정 및 서비스 계정 ID : misotube-project


'''


'''

# 영상이 일주일 전에 업로드되었는지 확인합니다.
        if (datetime.datetime.now() - published_at).days <= 1825:  # 1년이내업로드
            # 일주일 전에 업로드된 영상이라면, 이전 주에 비해 조회수가 증가했는지 확인합니다.
            week_ago = published_at - datetime.timedelta(weeks=4)  # 4주전



            week_ago_video = youtube.videos().list(
                id=video_id,
                part='snippet',
                fields='items(snippet(publishedAt, title))'
            ).execute()['items'][0]

            week_ago_title = week_ago_video['snippet']['title']
            week_ago_published_at = datetime.datetime.strptime(week_ago_video['snippet']['publishedAt'],
                                                               '%Y-%m-%dT%H:%M:%SZ')


            print(f' week_ago_published_at : {week_ago_published_at}')

            week_ago_view_count = youtube.videos().list(
                id=video_id,
                part='statistics',
                fields='items(statistics(viewCount))'
            ).execute()['items'][0]['statistics']['viewCount']




           
            week_ago_view_count = youtube.videos().list(
                id=video_id,
                part='statistics',
                fields='items(statistics(viewCount)),statistics(startDate))'
            ).execute()['items'][0]['statistics']['viewCount']

            week_ago_start_date = youtube.videos().list(
                id=video_id,
                part='statistics',
                fields='items(statistics(viewCount),statistics(startDate))'
            ).execute()['items'][0]['statistics']['startDate']

            week_ago_start_date = datetime.datetime.strptime(week_ago_start_date, '%Y-%m-%dT%H:%M:%SZ')
            week_ago_view_count = int(week_ago_view_count) if week_ago_view_count else 0
            if view_count - week_ago_view_count > 0 and published_at >= week_ago_start_date:
                result_videos_week.append((title, video_url, view_count))
            

            print(f' week_ago_view_count : {week_ago_view_count}')
            print(f' week_ago : {week_ago}')


        for title, video_url, view_count in result_videos_week:
            print(f'{title} ({video_url}) - {view_count} views (last week)')




# 이전 주 조회수 week_ago_view_count
        week_ago_response = youtube.search().list(
            type="video",
            part="id,snippet",
            fields="items(id(videoId),snippet(publishedAt,channelId,title))",
            #q=video_id,
            channelId=channel_id,
            publishedAfter='2023-04-15T17:49:27+09:49',
            publishedBefore='2023-04-22T17:49:27+09:49'
        ).execute()

        if week_ago_response['items']:
            week_ago_video_id = week_ago_response['items'][0]['id']['videoId']
            week_ago_stats_response = youtube.videos().list(
                part="statistics",
                id=week_ago_video_id
            ).execute()

            week_ago_stats = week_ago_stats_response['items'][0]['statistics']
            week_ago_view_count = int(week_ago_stats['viewCount'])

            print(f'일주전 조회수 : {week_ago_view_count}')
            print(f'현재 조회수: {view_count}')


        else:
            print("No data available for the specified time period.")
            
            
            '''
'''
         <<<<  해당 비디오의 최근 한달간의 조회수 평균 >>
         비디오의 일주일전 조회수와 현재 조회수의 변화량을 구한다.
         변화량을 일주일로 나눈후 30을 곱해주면 최근 한달간의 조회수 평균을 구할수 있다. 
       
        # 현재 주 조회수 view_count

        # 오늘날짜 파라메터 만들기
        nowDay = now.strftime('%Y-%m-%dT%H:%M:%S%z')[:-2] + ':' + now.strftime('%M')
        # 이전 주 날짜 파라메터 만들기
        week_ago = now - datetime.timedelta(weeks=1)
        weekBefore = week_ago.strftime('%Y-%m-%dT%H:%M:%S%z')[:-2] + ':' + week_ago.strftime('%M')

        # weekAfter = (published_at - datetime.timedelta(weeks=8)).strftime('%Y-%m-%dT%H:%M:%S%z')

        print(f' nowDay : {nowDay}')
        print(f' weekBefore : {weekBefore}')

'''

'''
# 최근 한달간 업로드된 동영상을 검색합니다. /////////////////////////////////

        now = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
        # 최근 한달간 업로드된 동영상을 검색합니다.
        month_ago = now - datetime.timedelta(weeks=4)

        video_response = youtube.videos().list(
            id=video_id,
            part='snippet,statistics'
        ).execute()

        # video_id로 해당 영상의 조회수를 가져옵니다.
        view_count = int(video_response['items'][0]['statistics']['viewCount'])

        print('$$ 조회수 : ' + str(view_count))

        # video_id로 해당 영상의 업로드 날짜를 가져옵니다.
        published_at = datetime.datetime.fromisoformat(video_response['items'][0]['snippet']['publishedAt'][:-1])
        print('$$ 업로드날짜 : ' + str(published_at))


'''

'''
        # 지금날짜
        #weekAfter = (published_at - datetime.timedelta(weeks=8)).strftime('%Y-%m-%dT%H:%M:%S%z')
        after = now.strftime('%Y-%m-%dT%H:%M:%S%z')

        print(f' weekBefore : {weekBefore}')
        print(f' after : {after}')

        week_ago_stats = youtube.search().list(
            channelId=video_response['items'][0]['snippet']['channelId'],
            type='video',
            part='id',
            maxResults=50,
            publishedBefore=weekBefore,
            publishedAfter=after
        ).execute()
        week_ago_view_count = int(week_ago_stats['viewCount'])
        print(f' 일주전 조회수 : { week_ago_view_count}')

'''