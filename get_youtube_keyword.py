'''
GPT가 생각한 '보석영상'을 찾는법

1. 조회수 대비 구독자 수의 비율을 계산하여, 이 비율이 높은 영상들을 선별
- 상대적으로 조회수가 높고 구독자 수가 적은 영상들을 찾아낼 수 있습니다.

2. 좋아요, 싫어요, 댓글 등 다른 지표들을 함께 고려
- 영상의 인기와 관련된 정보를 얻을 수 있습니다.

3. 특정 주제나 카테고리에 대해 집중하여 검색하고 분석하여, 관심 있는 영상들에 대한 정보를 얻을 수 있습니다.

4. 채널의 연령 확인: 채널이 얼마나 오래된 채널인지를 확인하여 최근에 시작된 채널인지, 아니면 오래된 채널인지를 파악
- 최근에 시작된 채널일수록 구독자 수가 적을 가능성이 높습니다.

5. 채널의 콘텐츠 개수: 채널이 제공하는 영상의 개수를 확인
- 적은 수의 콘텐츠를 가지고 있는 채널인지 아닌지를 판단할 수 있습니다. 콘텐츠 개수가 적은 채널은 아직 구독자를 많이 모으지 못한 것일 수 있습니다.

6. 채널의 업로드 주기: 채널의 영상 업로드 주기를 확인하여, 꾸준한 영상 업로드를 하는지 여부를 판단
- 업로드 주기가 길거나 불규칙한 채널은 구독자 수가 적을 수 있습니다.

7. 채널의 소셜 미디어 활동: 해당 채널의 소셜 미디어 활동을 확인하여, 채널의 홍보 노력이 어느 정도인지를 파악
- 활발한 소셜 미디어 활동을 하는 채널일수록 더 많은 구독자를 얻을 가능성이 있습니다.

<< 내가 생각한 '보석영상'을 찾는법 >>
보석영상을 찾기위해 이영상과 해당채널의 영상들의 평균조회수의 상관관계를 파악하는 것은 어떤가.

<< 진행상황 >>
키워드를 통해 조회된 100개의 영상중 구독자가 1만이하 이고 조회수가 5000이상인 영상을 정렬하여 출력하도록 만들었음
0508 : 출력할때 해당영상의 썸네일링크를 추가 하였음
0510 : 출력할때 10만이하의 영상들을 모두 출력하고 이후에 1만이하의 영상들이 출력되도록 변경하였음
        그리고 어떤코드를 만들지 정하고 지피티에 백업내용을 알려준후에 시작해야됨
0512 : 구독자 대비 조회수 항목을 필터에 추가하였음
0515 : 구독자 대비 조회수 항목의 출력부분을 하나의 함수로 출력할수 있게 되었음. 출력부분을 소수점을 제외하고 정수(~배)로 출력되도록 변경
       10만이하의 채널들도 view_subscriber_ratio 값을 리스트에 반환해서 출력할수 있도록 변경되었음.
       라이브영상은 배제되도록 수정하였음. ( 하지만 실제로 그런지는 테스트가 되어있지 않으니 언젠가 기회가 될때 혹은 앞으로 영상들을 확인하여 판단하자)

0516 : 썸네일을 직접 출력하려 했으나 불가능하고 쥬피터 노트북에 띄우는건 가능 -> 이건 나중에 그래프등과 함께 생각해보자.
       평균조회수와 평균좋아요와 그 비율을 측정하는 함수와 그비율에서 벗어나는 영상은 제외하는 함수를 추가하는중....

0519 : get_video_view_and_like_counts함수가 조회수와 좋아요를 반환하도록 수정함
       그래서 해당영상의 비율을 알게되었고 출력하게 되었지만 이자료를 비교할 '비율'이 없음
       그래서 최초 검색된 영상들의 채널에서 정보를 가져올때 '평균조회수'와 '평균좋아요' 를 구해 비율(또는 기준)을 만들기로 함
       그래서 get_channels_info를 수정하는 코드를 받았지만 아직 코드에 적용하진 않음

0523 : get_channels_info를 수정하는 코드를 적용하려 했지만 시간이 많이 걸리고 api호출이 많아 일단 이전코드로 다시 돌아옴



<<현재 만들고 있는 코드 >>
* 최초 그리고 어떤코드를 만들지 정하고 *
* 지피티에 백업내용을 알려준후에 시작해야됨 *

- 해당 채널의 평균 좋아요 비율을 확인하여 해당영상이 이 비율보다 좋아요 비율보다 현저히 낮으면 광고를 집행했을 가능성이 높다.
  반대로 비율보다 현저히 높은 비율은 외부에서 들어오도록 유도(팬덤)했을 가능성이 높다.
  평균좋아요 비율 확인 방법 : 평균조회수 대비 평균 좋아요의 비율
  get_channels_info에서 채널이름, 구독자수에 더해 평균조회수 대비 평균 좋아요의 비율을 반환하도록 수정하는 코드를 적용해보자.

  적용되는 코드가 좋지 않아 설계를 다시 하든 아니면 광고영상에 대한 부분은 빼든 생각해봐야 겠다. ...
  아니면 새롭게 만든 get_channels_info코드를 다른 함수로 만들어서 테스트 해보자.
  그리고 일단 코드가 너무 복잡하니 픽스된 부분은 info 쪽으로 옮기는 정리를 좀 하자.

##########################################################################################################
- 해당키워드의 볼륨을 알아내자.
 썸네일의 내용(일단 생각중) : 썸네일의 출력이 가능한가? 아이면 각썸네일을 키워드에 맞게 폴더에 저장해서 확인해볼것인가. ... 흠...
- 채널의 정보로 판단 : 채널의 콘텐츠 개수가 몇개인가? (50개 이하라면 유의미 할거라 대답함 .. 흠.. 필터링의 요소로 넣을만 한가?)
                    필터링된 영상이 해당영상의 채널의 영상들의 평균 조회수보다 높은가.
- 지금도 인기있는 영상인가.
- 검색된 내용들(조회수, 제목, 썸네일)을 어떻게 저장 할것인가 흠...
#############################################################################################################

'''


from tool.make_youtube_api import build_youtube_api
from tool.get_youtube_info import sort_videos
from tool.get_youtube_info import print_video_info
from tool.get_youtube_info import calculate_view_subscriber_ratio
from tool.get_youtube_info import get_video_view_counts
from tool.get_youtube_info import get_video_like_counts


"""
        << 주어진 비디오들의 조회수와 좋아요 수를 반환>>

        :param youtube: youtube API 클라이언트
        :param video_ids: 비디오 ID 리스트
        :return: 조회수와 좋아요 수를 담은 딕셔너리. 키는 비디오 ID, 값은 (조회수, 좋아요 수) 형태의 튜플
        """
def get_video_view_and_like_counts(youtube, video_ids):
    try:
        video_response = youtube.videos().list(
            id=",".join(video_ids),
            part="statistics",
            fields = "items(id,statistics(viewCount,likeCount))"  # 좋아요 수를 추가로 조회

        ).execute()


        view_and_like_counts = {}
        for item in video_response['items']:
            video_id = item['id']
            view_count = item['statistics'].get('viewCount', '0')
            like_count = item['statistics'].get('likeCount', '0')  # 좋아요 수를 추가로 저장
            view_and_like_counts[video_id] = (int(view_count), int(like_count))  # (조회수, 좋아요 수) 형태의 튜플로 저장



        #video_view_counts = {video['id']: video['statistics']['viewCount'] for video in video_response['items']}
        return view_and_like_counts
    except Exception as e:
        print(f"Error occurred while getting video view counts: {e}")
        return {}

# 각 채널에 대한 정보를 가져옵니다.
def get_channels_info(youtube, channel_ids):
    # YouTube Channels API를 사용하여 각 채널의 정보를 가져옴
    '''
    << 채널의 정보를 반환 >>
    1. 채널이름
    2. 채널구독자수
    3. 채널 평균조회수
    4. 채널 평균 좋아요수

    fields 매개변수
    items: API 응답에서 items 필드를 포함시킵니다. 여기에는 각 채널의 정보가 포함되어 있습니다.
    id: 각 채널 항목의 id 필드를 포함시킵니다. 이것은 채널의 고유 식별자입니다.
    snippet(title): 각 채널 항목의 snippet 필드에서 title 필드만 포함시킵니다. 이것은 채널의 제목입니다.
    statistics(subscriberCount): 각 채널 항목의 statistics 필드에서 subscriberCount 필드만 포함시킵니다. 이것은 해당 채널의 구독자 수입니다.
    '''

    try:
        channel_response = youtube.channels().list(
            id=",".join(channel_ids),
            part="snippet,statistics",
            fields = "items(id,snippet(title),statistics(subscriberCount))"
        ).execute()

        channel_info = {}
        for channel in channel_response['items']:
            channel_id = channel['id']
            channel_title = channel['snippet']['title']
            subscriber_count = channel['statistics']['subscriberCount']
            # thumbnail_url = channel['snippet']['thumbnails']['default']['url']  # 썸네일 링크 추가, 아직은 필요하지 않아 주석처리함
            channel_info[channel_id] = (channel_title, subscriber_count)

        return channel_info

    except Exception as e:
        print(f"Error occurred while getting channel info: {e}")
        return {}

    return channel_info





# 주어진 키워드를 사용하여 YouTube 비디오 목록을 검색하고, 각 비디오에 대한 정보를 반환
def youtube_search_list(youtube, keyword):
    search_response = youtube.search().list(
        q=keyword,
        part="snippet",
        type="video",
        maxResults=MAX_RESULTS #키워드를 통해 조회할 영상의 갯수 지정.
    ).execute()

    # 검색된 비디오들 중 라이브 방송이 아닌 비디오만 선택합니다.
    search_response['items'] = [item for item in search_response['items'] if
                                item['snippet']['liveBroadcastContent'] not in ['live', 'upcoming']]



    # 검색된 비디오들의 채널 ID를 추출합니다.
    channel_ids = [item['snippet']['channelId'] for item in search_response['items']]

    # 각 채널의 정보를 가져옵니다. - 검색된 영상채널의 이름, 구독자수, 평균조회수, 평균좋아요수, 좋아요/조회수 비율
    channel_info = get_channels_info(youtube, channel_ids)

    print(f" channel_info :  {channel_info}")

    # 조회수를 조회하기전 모든 영상의 아이디를 저장
    video_ids = [item['id']['videoId'] for item in search_response['items']]

    # 한 번의 호출로 모든 비디오의 조회수와 좋아요 수를 가져옵니다.
    video_view_and_like_counts = get_video_view_and_like_counts(youtube, video_ids)

    # 조회수와 좋아요 수 딕셔너리를 각각의 딕셔너리로 분리합니다.
    video_view_counts = {video_id: counts[0] for video_id, counts in video_view_and_like_counts.items()}
    video_like_counts = {video_id: counts[1] for video_id, counts in video_view_and_like_counts.items()}

    # 좋아요 대비 조회수 비율을 계산합니다.
    like_view_ratios = calculate_like_view_ratio(video_like_counts, video_view_counts)

    print(f" 좋아요 대비 조회수 비율 :  {like_view_ratios}")

    '''
    # 좋아요 대비 조회수 비율을 계산합니다.
    like_view_ratios = calculate_like_view_ratio(video_like_counts, video_view_counts)

    # 좋아요 대비 조회수 비율을 기준으로 비디오를 필터링합니다.
    search_response['items'] = filter_videos_by_like_view_ratio(search_response['items'], like_view_ratios)
    
    '''

    # 비디오 정보 목록을 생성합니다.
    subscriber_filtered_videos = []  # 구독자 수가 10만 이하인 채널의 영상
    view_filtered_videos = []  # 구독자 수가 10만 이하이고 조회수가 1만 이하인 영상
    ratio_filtered_videos = []  # 조회수 대비 구독자 수의 비율이 특정 임계값 이상인 영상

    #먼저 10만 이하의 구독자를 가진 모든 비디오에 대해 조회수 대비 구독자 수의 비율을 계산하고,
    # 그 다음에 이 비율을 사용하여 조회수가 5만 이상인 비디오 중에서 비율이 특정 임계값 이상인 비디오만 필터링하려는 것
    for search_result in search_response.get('items', []):
        video_id = search_result['id']['videoId']
        channel_id = search_result['snippet']['channelId']
        video_title = search_result['snippet']['title']
        thumbnail_url = search_result['snippet']['thumbnails']['default']['url']  # 영상 썸네일 링크 추가

        # 채널 정보에서 채널 제목, 구독자 수 및 썸네일 링크를 가져옴
        channel_title, subscriber_count = channel_info[channel_id]  # 썸네일 링크 추가

        #channel_title, subscriber_count, avg_views, avg_likes, avg_like_view_ratio = channel_info[channel_id]

        # 각영상의 조회수
        view_count = video_view_counts[video_id]

        # 구독자 수가 10만 이하인 채널만 선별
        if int(subscriber_count) <= MAX_SUBSCRIBERS:
            subscriber_filtered_videos.append(
                (video_id, channel_id, video_title, channel_title, subscriber_count, thumbnail_url, str(view_count)))


    # 이곳에 '구독자 10만이하채널의 영상들' 의 조회수 대비 구독자 수의 비율을 확인하여 데이터 샘플을 얻는다.
    # get_youtube_info.py의 calculate_view_subscriber_ratio() 함수를 사용하여 조회수 대비 구독자 수의 비율을 계산합니다.
    # view_subscriber_ratios 값이 57.17816091954023이라는 것은 한 영상의 조회수가 해당 영상 채널의 구독자 수의 약 57.18배임을 의미합니다.
    # view_subscriber_ratios는 조회수를 구독자 수로 나눈 값을 퍼센트로 표현한 것입니다.
    # 예를 들어, 영상이 10,000회 조회되었고, 해당 채널의 구독자 수가 1,000명일 경우, 조회수 대비 구독자 수의 비율은 10,000 / 1,000 = 10이 됩니다.
    # 이를 백분율로 변환하면 10 * 100 = 1000%가 됩니다.
    view_subscriber_ratios = calculate_view_subscriber_ratio(subscriber_filtered_videos)
    print(f" 구독자 10만 이하 구독자대피 조회수 비율 {view_subscriber_ratios}")

    # 10만이하채널의 영상에 대해 조회수 대비 구독자 수의 비율을 추가한 비디오 정보를 저장할 새로운 리스트 생성
    updated_subscriber_filtered_videos = []

# 구독자 10만 이상의 채널들만 가지고 다시 필터링
    for video in subscriber_filtered_videos:
        video_id, channel_id, video_title, channel_title, subscriber_count, thumbnail_url, view_count = video

        # video_id를 키로 사용하여 view_subscriber_ratios에서 해당 비율을 찾음
        view_subscriber_ratio = view_subscriber_ratios.get(video_id, 0)  # 만약 비율 정보가 없다면, 디폴트 값으로 0을 사용

        # 비율 정보를 튜플에 추가
        updated_video = video + (view_subscriber_ratio,)

        # 새로운 리스트에 업데이트된 비디오 정보 추가
        updated_subscriber_filtered_videos.append(updated_video)


        # 조회수가 5만 이상인 경우 추가로 선별
        if int(view_count) >= VIEW_COUNT_NUM:
            view_filtered_videos.append(
                (video_id, channel_id, video_title, channel_title, subscriber_count, thumbnail_url, str(view_count),view_subscriber_ratios[video_id]))


            # 필터링된 '조회수 1만이상의 영상들' 에 적용하기 위한 코드를 추가한다.
            # 이제 조회수 대비 구독자 수의 비율이 특정 임계값 이상인 비디오만 선택한 후 리스트에 비율값도 추가
            threshold = 10  # 예를 들어, 임계값을 10으로 설정해 봅니다.
            if view_subscriber_ratios[video_id] >= threshold:
                ratio_filtered_videos.append(
                    (video_id, channel_id, video_title, channel_title, subscriber_count, thumbnail_url, view_count,view_subscriber_ratios[video_id]))


    return updated_subscriber_filtered_videos, view_filtered_videos, ratio_filtered_videos

    # subscriber_videos : 구독자수 얼마이하의 영상리스트
    # view_videos : 구독자수 얼마이하이면서 조회수가 얼마이상인 영상리스트

# 이 함수는 각 비디오의 조회수 대비 구독자 수의 비율을 계산합니다.
def calculate_view_subscriber_ratio(videos):
    """
    이 함수는 각 비디오의 조회수 대비 구독자 수의 비율을 계산합니다.
    비디오 ID를 키로, 계산된 비율을 값으로 하는 딕셔너리를 반환합니다.
    """
    view_subscriber_ratios = {}
    for video in videos:
        video_id, channel_id, video_title, channel_title, subscriber_count, thumbnail_url, view_count = video
        if int(subscriber_count) > 0:  # 0으로 나누는 것을 방지
            ratio = int(view_count) / int(subscriber_count)
            view_subscriber_ratios[video_id] = ratio
    return view_subscriber_ratios

# 평균좋아요와 평균조회수를 구하고 그비율을 반환
def calculate_like_view_ratio(video_like_counts, video_view_counts):
    """
    비디오 ID를 키로, 계산된 좋아요 대 조회수 비율을 값으로 하는 딕셔너리를 반환합니다.

    :param videos: 비디오 정보를 담은 리스트. 각 요소는 (비디오 ID, 채널 ID, 비디오 제목, 채널 제목, 구독자 수, 좋아요 수, 썸네일 URL, 조회수) 형태의 튜플입니다.
    :return: 비디오 ID를 키로, 좋아요 대 조회수 비율을 값으로 하는 딕셔너리
    """
    like_view_ratios = {}  # 좋아요 대 조회수 비율을 저장할 딕셔너리
    for video_id, like_count in video_like_counts.items():
        view_count = video_view_counts[video_id]
        # 좋아요 수와 조회수가 모두 0이 아닐 때만 비율을 계산합니다.
        if like_count != 0 and view_count != 0:
            ratio = like_count / view_count
            like_view_ratios[video_id] = ratio
        else:
            like_view_ratios[video_id] = 0  # 좋아요 수 또는 조회수가 0인 경우 비율을 0으로 설정합니다.

    return like_view_ratios

def filter_videos(videos, lower_threshold, upper_threshold):
    """
    좋아요 대 조회수 비율이 주어진 범위 내에 있는 비디오만을 필터링하여 반환합니다.

    :param videos: 비디오 정보를 담은 리스트. 각 요소는 (비디오 ID, 채널 ID, 비디오 제목, 채널 제목, 구독자 수, 좋아요 수, 썸네일 URL, 조회수) 형태의 튜플입니다.
    :param lower_threshold: 필터링할 좋아요 대 조회수 비율의 하한 값
    :param upper_threshold: 필터링할 좋아요 대 조회수 비율의 상한 값
    :return: 필터링된 비디오 정보를 담은 리스트
    """
    like_view_ratios = calculate_like_view_ratio(videos)  # 각 비디오의 좋아요 대 조회수 비율을 계산

    filtered_videos = []  # 필터링된 비디오 정보를 저장할 리스트
    for video in videos:
        video_id, _, _, _, _, _, _, _ = video
        ratio = like_view_ratios[video_id]  # 비디오의 좋아요 대 조회수 비율
        if lower_threshold <= ratio <= upper_threshold:  # 비율이 주어진 범위 내에 있는 경우
            filtered_videos.append(video)  # 비디오를 필터링된 리스트에 추가

    return filtered_videos

def main(keyword):
    # 유튜브api 연결
    youtube = build_youtube_api()

    # 검색어에 대한 유튜브 list API를 사용하여 비디오 정보를 가져온다.
    subscriber_videos, view_filtered_videos, ratio_filtered_videos = youtube_search_list(youtube, keyword)

    '''
    결과값을 출력
    1. 구독자가 일정수 이하인 영상들만 출력
    2. 조회수가 일정수 이상인 영상들만 출력       
    '''
    # 구독자 수가 많은 순서로 정렬
    sorted_video_info_desc_subscribers = sort_videos(subscriber_videos, 'subscribers', 'desc')
    print(f"*영상총갯수: << {len(subscriber_videos)} >> 구독자 수가 많은 순서로 정렬되었음*")
    print(f"*구독자{MAX_SUBSCRIBERS}만 이하의 영상들을출력*")
    print_video_info(sorted_video_info_desc_subscribers)

    # 구독자 수가 많은 순서로 정렬
    sorted_video_info_desc_viewcount = sort_videos(view_filtered_videos, 'subscribers', 'desc')
    print(f"*영상총갯수: << {len(view_filtered_videos)} >> 구독자 수가 많은 순서로 정렬되었음*")
    print(f"*구독자{MAX_SUBSCRIBERS}만 이하이고 조회수{VIEW_COUNT_NUM}만 이상의 영상들을출력*")
    print_video_info(sorted_video_info_desc_viewcount)

    # 구독자 수가 많은 순서로 정렬
    sorted_video_info_desc_viewcount = sort_videos(ratio_filtered_videos, 'subscribers', 'desc')
    print(f"*영상총갯수: << {len(ratio_filtered_videos)} >> 구독자 수가 많은 순서로 정렬되었음*")
    print(f"*구독자{MAX_SUBSCRIBERS}만 이하이고 조회수{VIEW_COUNT_NUM}만 이상의 영상들중 구독자대비 조회수가 높은 영상을출력*")
    print_video_info(sorted_video_info_desc_viewcount)


MAX_RESULTS = 100  #조회할영상의 갯수
MAX_SUBSCRIBERS = 10000 #구독자수 : 구독자수는 낮을수록 좋다.
VIEW_COUNT_NUM = 10000  #조회수 : 조회수는 높을수록 좋다.


if __name__ == "__main__":
    keyword = '워터파크 슈즈'

    # 현재 키워드로 검색된 100개의 영상중 구독자 5만이하,  조회수 1만이상 의 영상만 판별함
    # 아래의 숫자로 변경가능 . 키워드에 따라 판별되지 않을경우 숫자를 변경해보자.
    # 키워드, 구독자수, 조회수          구독자는 낮아야되텐셀 팬티고 : 조회수는 높아야함
    main(keyword)