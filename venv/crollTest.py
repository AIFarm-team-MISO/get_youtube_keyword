from pytube import YouTube
from urllib.parse import urlparse, parse_qs

# Get the YouTube video URL from the user
search_term = input("Enter a search term to find the top video on YouTube: ")

# Use the pytube library to search for videos on YouTube
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
