from acquisition.video_id import extract_video_id


url = "https://ok.ru/video/248244667877"

video_id = extract_video_id(url)

print(f"URL      : {url}")
print(f"Video ID : {video_id}")