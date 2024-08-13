'''
이코드는 '카카오스토리' 에 글을 작성하기 위해 인증정보를 자동화 하는 프로그램임
현재 카카오보드(뷰)에 글을 올리기 위한 api는 카카오에서 제공하지 않기 때문에 일단 패스 ..
나중에 시간나면 카카오뷰 자동발행 글을읽고 시도해보자.


<< api 정보 >>
네이티브 앱 키 :	7e24952584048488b6d6c0289f2c7148
REST API 키 :	2e8db4c5c492c66d3d56398a224134a0
JavaScript 키 :	a2f812e427223e5cb281001ed1407786
Admin 키 :	30c2f5842deac92d82713d8ef62c7092
앱 ID : 897603

<< 인가 code 받기 >>
웨사이트에서 밑의 url로 들어간다.
https://kauth.kakao.com/oauth/authorize?client_id=2e8db4c5c492c66d3d56398a224134a0&redirect_uri=https://example.com/oauth&response_type=code
이후 로그인 후 나온 페이지의 링크를 살펴본다.
밑의 링크같이 나오고 [code=] 이후의 값을 사용하면 된다.
https://example.com/oauth?code=zGu8ZR2Y6KVAjvQzCjwmIL_wVBETfmVVe5umuT43L2EwuvGGfUZ1WywQOUUi_4KuRA4Ifgo9cxcAAAGH0IjfWw

<< 인가코드  04-30 >>
code=zGu8ZR2Y6KVAjvQzCjwmIL_wVBETfmVVe5umuT43L2EwuvGGfUZ1WywQOUUi_4KuRA4Ifgo9cxcAAAGH0IjfWw
rest_api_key(CLIENT_ID) = 2e8db4c5c492c66d3d56398a224134a0
Client Secret : YX4dhhl0RA7XXz4zSvfdeZKfLinX46Cf

<< 엑세스 토큰 - 0420 >>
{'access_token': '1C5My4djvC5gkOZIh4mMvH41JfRhICwvdsXWIERNCinJYAAAAYee9q4X', 'token_type': 'bearer', 'refresh_token': 'ee1HIwT2jVfmH6n_OmZcl0qBU-8SXutAwT-1oeUsCinJYAAAAYee9q4R', 'expires_in': 21599, 'refresh_token_expires_in': 5183999}


'''


import requests
import json
from os import path
import os

CLIENT_ID = '2e8db4c5c492c66d3d56398a224134a0'
CLIENT_SECRET = 'YX4dhhl0RA7XXz4zSvfdeZKfLinX46Cf'
REDIRECT_URI = 'https://example.com/oauth'
CODE = 'zGu8ZR2Y6KVAjvQzCjwmIL_wVBETfmVVe5umuT43L2EwuvGGfUZ1WywQOUUi_4KuRA4Ifgo9cxcAAAGH0IjfWw'
TOKEN_FILE = os.path.join("kakaoTool", "access_token.json")



# 액세스 토큰 정보를 JSON 파일에 저장
def save_access_token(token_data):
    with open(TOKEN_FILE, 'w') as f:
        json.dump(token_data, f)


# JSON 파일에서 액세스 토큰 정보를 불러옴
def load_access_token():
    if not path.exists(TOKEN_FILE):
        return None

    with open(TOKEN_FILE, 'r') as f:
        return json.load(f)


# 새로운 액세스 토큰을 발급받음
def get_new_access_token():
    url = "https://kauth.kakao.com/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": CODE,
    }

    response = requests.post(url, data=payload)
    token_data = response.json()

    if 'access_token' not in token_data:
        raise Exception("새 액세스 토큰을 가져오지 못했습니다. 응답: " + str(token_data))

    print('새로운 토큰 발행 완료 ')

    save_access_token(token_data)
    return token_data["access_token"]


# 리프레시 토큰을 사용하여 액세스 토큰을 갱신함
def refresh_access_token(refresh_token):
    url = "https://kauth.kakao.com/oauth/token"
    payload = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": refresh_token,
    }
    response = requests.post(url, data=payload)
    token_data = response.json()

    if 'access_token' not in token_data:
        raise Exception("액세스 토큰을 갱신하지 못했습니다. 응답: " + str(token_data))

    save_access_token(token_data)
    return token_data["access_token"]


# 저장된 액세스 토큰을 가져오거나 새로 발급받음
def get_access_token():
    token_data = load_access_token()

    if token_data is None:
        return get_new_access_token()

    access_token = token_data["access_token"]
    refresh_token = token_data["refresh_token"]

    # 토큰 만료 확인
    url = "https://kapi.kakao.com/v1/user/access_token_info"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        access_token = refresh_access_token(refresh_token)

    print('토큰만료확인 완료')

    return access_token

# 카카오스토리에 글을 게시함
def post_story(access_token, content):
    url = "https://kapi.kakao.com/v1/api/story/post/note"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    payload = {
        "content": content,
    }
    response = requests.post(url, headers=headers, data=payload)
    response_data = response.json()
    if response.status_code == 200:
        print("성공적으로 게시되었습니다!")
        print(response_data)
    else:
        print("게시에 실패하였습니다.")
        print(response_data)


if __name__ == "__main__":
    try:
        access_token = get_access_token()
        content = "카카오스토리에 업로드할 글입니다."
        post_story(access_token, content)
    except Exception as e:
        print("오류 발생:", e)
