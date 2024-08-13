'''
<<< 프로젝트 목적 >>>
신우사이트에 callenge2000-n2 로 로그인하여 상품명 가격 등 이셀러스에 업로드하기 위한 엑셀의 내용을 크롤링하여
엑셀파일을 만들어 보는것

<< 진행상황 >>
1. 현재 신우사이트를 띄우는 것까지 되었음 - 모든게 정상실행되면 백그라운드에서 실행되도록 변경할예정
2. 로그인 시도 - 그러기 위해서 웹에서 어떤 컴포넌트를 어떻게 입력해야되는지 확인해야됨



'''

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import os

driver_folder = 'driver_tool'
current_directory = os.getcwd()  # 현재 작업 디렉토리 경로 가져오기
driver_path = os.path.join(current_directory, driver_folder, 'chromedriver')  # 드라이버 경로 설정
service = Service(executable_path=driver_path)


# 크롬 옵션 설정
chrome_options = Options()
# chrome_options.add_argument('--headless') 나중에 테스트가 끝나고 백그라운드에서 실행할때 주석지우고 실행하면 됨

# 웹 드라이버 경로 설정 및 크롬 옵션 추가
driver_path = 'path/to/your/chromedriver'  # 웹 드라이버의 경로를 입력하세요.
browser = webdriver.Chrome(service=service, options=chrome_options)


# 웹사이트 접속 및 로그인
url = 'https://www.sinwoo.com/'  # 로그인 페이지 URL을 입력하세요.
browser.get(url)
time.sleep(2)

print('드라이버 성공')

# 로그인 정보 입력
username = browser.find_element_by_id('username')  # 아이디 입력 부분의 HTML id를 입력하세요.
password = browser.find_element_by_id('password')  # 비밀번호 입력 부분의 HTML id를 입력하세요.

username.send_keys('your_username')  # 실제 아이디를 입력하세요.
password.send_keys('your_password')  # 실제 비밀번호를 입력하세요.

# 로그인 버튼 클릭
login_button = browser.find_element_by_id('login_button')  # 로그인 버튼의 HTML id를 입력하세요.
login_button.click()
time.sleep(2)

# 크롤링할 페이지로 이동
target_page = 'https://example.com/target_page'  # 크롤링할 페이지 URL을 입력하세요.
browser.get(target_page)
time.sleep(2)

# 웹 페이지 소스 가져오기 및 BeautifulSoup 객체 생성
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')

# 데이터 크롤링 (예: 테이블 크롤링)
table = soup.find('table', {'class': 'example_class'})  # 테이블의 클래스를 입력하세요.
rows = table.find_all('tr')

data = []
for row in rows:
    cols = row.find_all('td')
    cols = [col.text.strip() for col in cols]
    data.append(cols)

# 데이터를 데이터프레임으로 변환
df = pd.DataFrame(data)

# 첫 번째 행을 열 이름으로 설정하고, 첫 번째 행을 삭제
df.columns = df.iloc[0]
df = df.drop(0)

# 엑셀 파일로 저장
df.to_excel('output.xlsx', index=False)

# 웹 브라우저 종료
browser.quit()
