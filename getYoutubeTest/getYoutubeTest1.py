

#


# import pytube
import os
import openai
import re
from pytube import YouTube
from pytube import Search
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi



from urllib.parse import urlparse, parse_qs

# Get the YouTube video URL from the user
# 입력한 키워드로 유튜브페이지 상단에 있는 영상을 가져온다.
query = input("Enter a search term to find the top video on YouTube: ")
search_results = Search(query).results

if not search_results:
    print(f"No results found for '{query}'")
    exit()

video_url = None
for result in search_results:
    try:
        video = YouTube(result.watch_url)
        video_url = result.watch_url
        break
    except:
        pass

if not video_url:
    print(f"No results in search results for '{query}'")
    exit()

title = video.title
#print(f"video : {video}")
print(f"title :  {title}")
print(f"video_url :  {video_url}")

#대본 가져올때 1차는 영어, 2차는 한글로 가져오라고 함
transcript = YouTubeTranscriptApi.get_transcript(video.video_id,languages=['en', 'ko'])

transcript_text = ''
for entry in transcript:
    transcript_text += entry['text'] + ''

# 검색한키워드로 파일명을 만들었음
filename = f"{query}.txt"
filepath = os.path.join(r'c:\Users\miso\Desktop\down', filename) #User에서 에러가 나므로 문자열이란 뜻으로 'r'을 붙였음
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(f"title:{title}\n")
    f.write(f"transcript:{transcript_text}\n")

print(f"Saved title and transcript of video to {filepath}")

# openai 관련
openai.api_key = "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"

# 텍스트파일을 읽는다.
with open(filepath, 'r', encoding='utf-8') as file:
    text = file.read()

# use openai to summarize the text
summary = openai.Completion.create(
    engine = "davinci",
    prompt = (f"please summarize the following text: \n{text}\n\nSummary:"),
    max_tokens = 100
)["choices"][0]["text"].strip()

# use openai to paraphrase the text
paraphrased = openai.Completion.create(
    engine = "davinci",
    prompt = (f"please paraphrase the following text: \n{summary}\n\nParaphrase:"),
    max_tokens = 100
)["choices"][0]["text"].strip()

# clean th summary and paraphrased text
summary = re.sub(r'[^\w\s]', '', summary)
paraphrased = re.sub(r'[^\w\s]', '', paraphrased)

# save the results to a new file

newfilepath = os.path.join(r'c:\Users\miso\Desktop\down', "new.txt") #User에서 에러가 나므로 문자열이란 뜻으로 'r'을 붙였음

with open(newfilepath, 'w', encoding='utf-8') as file:
    file.write(f'Summary:\n{summary}\n\nParaphrase:\n{paraphrased}')



"""
일단 가져온 대본을 요약하고 재배열하여 파일로 저장하는것까지는 완료. 
여기까지하고..

가져오는 부분!!!
구독자는 낮은대 조회수가 많이 나온영상을 가져오는 코드를 만들어보자.
그리고 그런 영상들을 엑셀로 저장할수 있게 만들자. 
챗지피티로 답은 나왔는데 분석해서 내코드에 적용해보자.  

"""


"""
results = pytube.Search(search_term)
video_url = results[0].watch_url

# Parse the video ID from the URL
query = urlparse(video_url).query
video_id = parse_qs(query)["v"][0]

# Use the pytube library to retrieve the video metadata
video = pytube.YouTube(video_url)
video_title = video.title
video_thumbnail = video.thumbnail_url
video_script = video.description

# Print the results
print("Video Title:", video_title)
print("Thumbnail URL:", video_thumbnail)
print("Video Transcript:", video_script)




openai 대답 가져오는 또다른 형식
def ask_gpt(text: str):
    openai.api_key = f"{openai_key}"
    res = openai.Completion.create( #[Object].[Class].[Method]
        engine = "text-davinci-003", prompt=text, temperature=0.6, max_tokens=150
    )
    return res.choices[0].text

def main():
    while True:
        query = input("Ask a question: ")
        res = ask_gpt(query)
        print(f"{res}\n")
"""
