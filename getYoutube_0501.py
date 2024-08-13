'''
<< 목적 >>
YouTube Data API를 사용하여 일주일 전의 조회수를 추정하는 방법.
비디오를 게시한 날짜와 현재 날짜 사이의 날짜별 조회수 증가 추세를 분석.
이를 통해 일주일 전 조회수를 추정.
정확한 결과를 제공하지는 않지만 근사치를 얻을 수 있습니다.

<< 진행상황 >>
일주일전에 조회수 가져오는것 완료

<< 할일 >>
이전 코드를 함수로 만들어 여기에 보관하여 0415_ok(가칭)에서 불러서 쓰도록 만들어보자.
그렇게 코드를 정리하며 api를 최대한 적게 불러서 테스트 할수 있도록 수정하자.

- 이후에 인기도에 대한 내용을 다시 시작하자.
최근 일주일 평균 조회수가 이전한달편균 조회수보다 높은경우 라고 생각하는데
gpt 에게 물어봐서 보완하자.

그러나 이 방법에는 몇 가지 한계가 있다.

1. 조회수의 증가가 항상 균등하지 않을 수 있습니다.
일부 동영상은 게시된 후 바로 인기를 얻지만, 일부는 시간이 지남에 따라 점차 인기를 얻습니다.
이런 경우에는 평균 일일 조회수를 사용한 추정이 정확하지 않을 수 있습니다.
2. 동영상이 일주일 미만인 경우, 이 함수는 오류를 발생시킵니다. 일주일 미만의 동영상에 대해 조회수 추정을 하려면, 다른 방법을 사용해야 합니다.
3.이 함수는 YouTube API에 대한 요청을 많이 필요로 합니다. 많은 수의 동영상에 대해 이 함수를 실행하면, YouTube API의 일일 할당량을 초과할 수 있습니다.



'''
import datetime
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from tool.make_youtube_api import build_youtube_api


# 조회수 추이를 분석해 일주일 전 조회수를 추정합니다.
# 조회수 추이를 분석해 일주일 전 조회수를 추정하는 함수입니다.
def estimate_views_a_week_ago(youtube, video_id):
    try:
        # YouTube Data API를 사용하여 비디오 정보를 가져옵니다.
        response = youtube.videos().list(
            part='snippet,statistics',
            id=video_id
        ).execute()

        # 가져온 비디오 정보를 처리합니다.
        video_data = response['items'][0]
        published_at = datetime.datetime.fromisoformat(video_data['snippet']['publishedAt'].rstrip('Z'))
        total_views = int(video_data['statistics']['viewCount'])

        # 현재 시간을 구하고, 비디오 게시일로부터 경과된 일 수를 계산합니다.
        now = datetime.datetime.utcnow()
        days_since_published = (now - published_at).days
        if days_since_published < 7:
            raise ValueError("The video is less than a week old. Can't estimate views a week ago.")

        # 평균 일일 조회수를 계산합니다.
        average_daily_views = total_views / days_since_published
        # 일주일 전 조회수를 추정합니다.
        estimated_views_a_week_ago = total_views - (average_daily_views * 7)

        # 추정된 조회수를 반환합니다. 값이 음수이면 0을 반환합니다.
        return max(0, estimated_views_a_week_ago)

    except HttpError as error:
        print(f"An HTTP error {error.resp.status} occurred: {error.content}")
        return None

# 메인 함수
def main():
    video_id = '2hCLRHxEVEo' # 비디오 ID를 입력하세요.
    # 현재 조회수 : 247832
    # title(제목) : 세키로 보스전 모음
    # 링크: https://www.youtube.com/watch?v=2hCLRHxEVEo
    # 0501 에 일주일 전 조회수 : 246670.0281312793 다시 만들때 참고하자. 

    # 'tool/make_youtube_api.py'에서 정의된 함수를 사용하여 YouTube API 클라이언트를 생성합니다.
    youtube = build_youtube_api()
    # 일주일 전 조회수를 추정하는 함수를 호출합니다.
    estimated_views = estimate_views_a_week_ago(youtube, video_id)

    if estimated_views is not None:
        print(f"Estimated views a week ago: {estimated_views}")

if __name__ == '__main__':
    main()
