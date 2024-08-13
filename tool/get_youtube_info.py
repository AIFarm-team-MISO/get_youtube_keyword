'''
 * sort_videos : 조회수 또는 구독자 순서로 정렬 
 매개변수  
 - video_info 리스트
 - 정렬 기준('views' 또는 'subscribers')
    'views'(조회수순) 'subscribers'(구독자순)             
 - 정렬 방식('asc' 또는 'desc') 
    'asc'(오름차순) 'desc'(내림차순)

    # 조회수가 적은 순서로 정렬
    sorted_video_info_asc_views = sort_videos(subscriber_videos, 'views', 'asc')
    # 조회수가 많은 순서로 정렬
    sorted_video_info_desc_views = sort_videos(subscriber_videos, 'views', 'desc')
    # 구독자 수가 적은 순서로 정렬
    sorted_video_info_asc_subscribers = sort_videos(subscriber_videos, 'subscribers', 'asc')
    # 구독자 수가 많은 순서로 정렬
    sorted_video_info_desc_subscribers = sort_videos(subscriber_videos, 'subscribers', 'desc')
'''


def sort_videos(video_info, sort_by='views', order='asc'):
    if sort_by == 'views':
        index = 6
    elif sort_by == 'subscribers':
        index = 4
    else:
        raise ValueError("Invalid sort_by value. Please use 'views' or 'subscribers'.")

    if order == 'asc':
        return sorted(video_info, key=lambda x: int(x[index]))
    elif order == 'desc':
        return sorted(video_info, key=lambda x: int(x[index]), reverse=True)
    else:
        raise ValueError("Invalid order value. Please use 'asc' or 'desc'.")

"""
<이 함수의 목적>
    이 함수는 각 비디오의 조회수 대비 구독자 수의 비율을 계산
    만약 threshold = 10로 정했다는 것은? : 해당 영상의 조회수가 자신이 보유한 구독자 수의 10배 이상일 경우를 필터링한다는 의미
    즉, 만약 한 영상의 조회수가 해당 채널의 구독자 수의 10배 이상이면, 이 영상은 threshold 값인 10보다 큰 view_subscriber_ratio 값을 가지게 됩니다. 따라서 이런 영상들만 선택하여 필터링하는 것입니다.
    예를 들어, 한 영상의 조회수가 10,000회이고, 해당 채널의 구독자 수가 1,000명이라면, 이 영상의 view_subscriber_ratio 값은 10,000 / 1,000 = 10이 됩니다. 이 경우, 이 영상은 threshold 값인 10과 같으므로 필터링에 포함됩니다.
    반면, 조회수가 9,000회이고, 구독자 수가 1,000명인 영상의 view_subscriber_ratio 값은 9,000 / 1,000 = 9로, threshold 값인 10보다 작으므로 이 영상은 필터링에서 제외됩니다.
"""
def calculate_view_subscriber_ratio(videos):
    """
    비디오 ID를 키로, 계산된 비율을 값으로 하는 딕셔너리를 반환합니다.

    :param videos: 비디오 정보를 담은 리스트. 각 요소는 (비디오 ID, 채널 ID, 비디오 제목, 채널 제목, 구독자 수, 썸네일 URL, 조회수) 형태의 튜플입니다.
    :return: 비디오 ID를 키로, 조회수 대비 구독자 수의 비율을 값으로 하는 딕셔너리
    """
    view_subscriber_ratios = {}  # 조회수 대비 구독자 수의 비율을 저장할 딕셔너리
    for video in videos:
        video_id, channel_id, video_title, channel_title, subscriber_count, thumbnail_url, view_count = video
        if int(subscriber_count) > 0:  # 구독자 수가 0인 경우를 방지
            ratio = int(view_count) / int(subscriber_count)  # 조회수 대비 구독자 수의 비율 계산
            view_subscriber_ratios[video_id] = ratio  # 계산된 비율을 딕셔너리에 저장
    return view_subscriber_ratios


def print_video_info(video_info):
    # 결과를 원하는 형식으로 출력
    for index, info in enumerate(video_info, start=1):  # start=1 : 인덱스를 0이 아닌 1부터시작 ( 지금 번호를 매겨 출력하기 때문에 추가되었음)
        video_id, channel_id, video_title, channel_title, subscriber_count, thumbnail_url, view_count, view_subscriber_ratio = info
        print(f"{index}.  {video_title}")
        print(f"\t구독자: # {subscriber_count} #")
        print(f"\t조회수: << {view_count} >>")
        print(f"\t영상링크: https://www.youtube.com/watch?v={video_id}, 영상썸네일링크: {thumbnail_url}")
        print(f"\t채널이름: {channel_title}")  # 채널링크 추가하자.
        #print(f"\t조회수 대비 구독자 수의 비율: {view_subscriber_ratio}\n")
        print(f"\t구독자 대비 조회수 비율: {round(view_subscriber_ratio)}배\n")  # 조회수 대비 구독자 수의 비율을 반올림한 정수로 변환하고, '배'를 출력



def get_video_view_counts(youtube, video_ids):
    """주어진 동영상 ID에 대한 조회수를 반환합니다.

    Args:
        youtube (googleapiclient.discovery.Resource): YouTube API 클라이언트
        video_ids (list of str): 조회할 동영상 ID 리스트

    Returns:
        dict: 각 동영상 ID를 키로 하고, 해당 동영상의 조회수를 값으로 하는 딕셔너리
    """
    try:
        video_response = youtube.videos().list(
            id=",".join(video_ids),
            part="statistics",
            fields="items(id,statistics(viewCount))"
        ).execute()

        video_view_counts = {}
        for video in video_response['items']:
            video_id = video['id']
            view_count = video['statistics']['viewCount']
            video_view_counts[video_id] = int(view_count)

        return video_view_counts

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_video_like_counts(youtube, video_ids):
    """주어진 동영상 ID에 대한 좋아요 수를 반환합니다.

    Args:
        youtube (googleapiclient.discovery.Resource): YouTube API 클라이언트
        video_ids (list of str): 조회할 동영상 ID 리스트

    Returns:
        dict: 각 동영상 ID를 키로 하고, 해당 동영상의 좋아요 수를 값으로 하는 딕셔너리
    """
    try:
        video_response = youtube.videos().list(
            id=",".join(video_ids),
            part="statistics",
            fields="items(id,statistics(likeCount))"
        ).execute()

        video_like_counts = {}
        for video in video_response['items']:
            video_id = video['id']
            like_count = video['statistics'].get('likeCount', 0)  # 'likeCount' 가 없는 경우 0으로 처리
            video_like_counts[video_id] = int(like_count)

        return video_like_counts

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


'''

"""주어진 채널 ID에 대한 정보를 반환합니다.

        Args:
            youtube (googleapiclient.discovery.Resource): YouTube API 클라이언트
            channel_ids (list of str): 조회할 채널 ID 리스트

        Returns:
            dict: 각 채널 ID를 키로 하고, 해당 채널의 제목, 구독자 수, 평균 조회수, 평균 좋아요 수, 좋아요/조회수 비율을 값으로 하는 딕셔너리
        """
    try:
        channel_response = youtube.channels().list(
            id=",".join(channel_ids),
            part="snippet,statistics",
            fields="items(id,snippet(title),statistics(subscriberCount))"
        ).execute()

        channel_info = {}
        for channel in channel_response['items']:
            channel_id = channel['id']
            channel_title = channel['snippet']['title']
            subscriber_count = channel['statistics']['subscriberCount']

            # 채널의 모든 동영상 조회
            video_response = youtube.search().list(
                channelId=channel_id,
                part="id",
                maxResults=100,
                type="video"
            ).execute()

            video_ids = [item['id']['videoId'] for item in video_response['items']]

            # 각 동영상의 조회수와 좋아요 수를 가져옴
            video_view_counts = get_video_view_counts(youtube, video_ids)
            video_like_counts = get_video_like_counts(youtube, video_ids)

            # 평균 조회수와 평균 좋아요 수를 계산
            average_view_count = sum(video_view_counts.values()) / len(video_view_counts)
            average_like_count = sum(video_like_counts.values()) / len(video_like_counts)

            like_view_ratio = 0
            if average_view_count != 0:  # 0으로 나누는 것을 방지
                like_view_ratio = average_like_count / average_view_count

            channel_info[channel_id] = (
            channel_title, subscriber_count, average_view_count, average_like_count, like_view_ratio)





    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
'''