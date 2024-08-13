'''

조회수, 좋아요수, 싫어요수, 댓글 수 등을 모두 종합하여 지표를 만들어 판별하는 방법

이러한 지표들을 종합하여 인기도 점수를 계산하고, 이 점수가 높은 동영상을 판별하는 방법입니다.
구독자 수 대비 조회수 비율을 사용하여 판별하는 방법

구독자 수 대비 조회수 비율이 높은 동영상을 판별하는 방법입니다. 이 방법은 구독자 수와는 상관없이, 단기간 동안 많은 사람들에게 인기가 있는 동영상을 찾아낼 수 있습니다.
동영상이 언급된 뉴스나 블로그 등의 외부 매체 수를 사용하여 판별하는 방법

동영상이 많이 언급되고 공유된 외부 매체 수가 많을수록 인기 있는 동영상으로 판별하는 방법입니다. 이 방법은 동영상이 얼마나 인기 있는지에 대한 외부적인 평가를 기반으로 판별할 수 있습니다.
동영상이 검색어로 검색되는 빈도수를 사용하여 판별하는 방법

동영상이 검색어로 검색되는 빈도수가 많을수록 인기 있는 동영상으로 판별하는 방법입니다. 이 방법은 동영상이 얼마나 많은 사람들에게 검색되는지를 기반으로 판별할 수 있습니다.

'''
import datetime


import pytz
from googleapiclient.errors import HttpError


def get_popularity_score(youtube,video_id):
    try:
        video_response = youtube.videos().list(
            part="statistics",
            id=video_id
        ).execute()

        # 조회수, 좋아요수, 싫어요수, 댓글 수를 가져옴
        stats = video_response['items'][0]['statistics']
        view_count = int(stats['viewCount'])
        like_count = int(stats.get('likeCount', 0))
        dislike_count = int(stats.get('dislikeCount', 0))
        comment_count = int(stats.get('commentCount', 0))

        if view_count < 1000:
            return '인기도 지표 계산 불가'

        # view_weight : 조회수의 가중치를 계산합니다. 조회수가 10만 이하일 경우 그대로 사용하고, 10만을 넘어가는 경우 1.0으로 사용
        # like_weight : 좋아요 수와 싫어요 수를 이용하여 좋아요의 비율을 계산합니다. 좋아요와 싫어요가 모두 0인 경우에는 0을 사용
        # comment_weight : 댓글 수의 비율을 계산
        # score : 각 가중치를 이용하여 인기도 점수를 계산, 조회수와 좋아요 수, 댓글 수가 모두 고려되며, 좋아요와 댓글이 조회수에 비해 중요도가 높기 때문에 더 높은 가중치를 부여
        view_weight = min(1.0, view_count / 100000) # 지금은 일단 10만 조회수를 기준으로 좋은지 나쁜지를 판단하였음
        like_weight = like_count / (like_count + dislike_count) if (like_count + dislike_count) > 0 else 0
        comment_weight = comment_count / view_count
        score = (view_weight * 0.4 + like_weight * 0.4 + comment_weight * 0.2) * 100

        print(f' score : {score}')




        print(f' view_count : {view_count}')
        print(f' like_count(좋아요) : {like_count}')
        print(f' dislike_count(싫어요) : {dislike_count}')
        print(f' comment_count(댓글) : {comment_count}')

        # 잘이해할수 없는 부분이라 일단 주석체크
        # popularity_score = (view_count + score) / view_count * 100
        # score_percentage = round(score,2)



       #이곳은 해당점수에 따라 알기쉽게 표현한 부분임

        if 50 <= score < 60:
           return f"{score:.2f}% (평균 이상)"
        elif 61 <= score < 80:
           return f"{score:.2f}% (좋음)"
        elif score >= 81:
           return f"{score:.2f}% (아주 좋음)"
        else:
           return '인기도 지표 계산 불가'

        round(score, 2)


        return f'{score_percentage}%'

        ''' 
        이 값이 높을수록 해당 비디오는 더 인기가 많다는 것을 나타냅니다. 
        이 값이 얼마나 높아야 하는지는 산출된 인기도 점수가 해당 채널의 특성과 관련이 있으므로 일반적인 기준은 없습니다. 
        따라서 적절한 기준은 해당 채널의 역사적인 데이터와 비교하여 결정해야 합니다.
        --> 이곳에 이영상의 조회수가 채널의 영상들의 평균조회수보다 높은지를 판별(일단 2배정도)  
        '''



    except IndexError:
        print("비디오에 대한 데이터가 없음")
        return 0

    except HttpError as error:
        print(f"An HTTP error {error.resp.status} occurred:\n{error.content}")
        return 0

'''
    def get_week_ago_views(youtube,video_id):
        # 현재 시간을 UTC timezone으로 가져옴
        utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    
        # 한국 timezone으로 변경
        kst = pytz.timezone('Asia/Seoul')
        kst_now = utc_now.astimezone(kst)
        # 일주일 전의 datetime 객체 생성
        week_ago = kst_now - datetime.timedelta(days=7)
    
        # videoStatistics에서 일주일 전의 조회수를 가져옵니다.
        response = youtube.videos().list(
            part='statistics',
            id=video_id
        ).execute()
        statistics = response['items'][0]['statistics']
        view_count = int(statistics['viewCount'])
    
        print(f' view_count : {view_count}')
    
        # video에 대한 상세 정보를 가져와서 video publishedAt을 비교합니다.
        video_response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()
        publishedAt = video_response['items'][0]['snippet']['publishedAt']
        publishedAt = datetime.datetime.fromisoformat(publishedAt.replace('Z', '+00:00'))
    
        print(f' publishedAt : {publishedAt}')
    
    
        # video publishedAt이 일주일 전보다 이후인 경우에만 조회수를 반환합니다.
        if publishedAt > week_ago:
            return 'video가 일주일 전에 업로드되지 않았습니다.'
        else:
            return view_count 
'''