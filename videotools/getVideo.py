import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import os

def download_video(url, save_path):
    response = requests.get(url, stream=True)
    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

def crawl_and_download_videos(url, save_directory):
    response = requests.get(url)
    html_content = response.content

    base_url = response.url  # 获取基本URL

    soup = BeautifulSoup(html_content, 'html.parser')

    video_tags = soup.find_all('video')

    for i, video_tag in enumerate(video_tags):
        video_url = video_tag['src']
        full_video_url = urljoin(base_url, video_url)  # 构建完整的视频URL
        print(video_tag)
        video_name = video_tag.get('src', f'video{i+1}.mp4')[7:]  # 获取视频名字，如果没有则使用默认值
        print(f'Found video {video_name} at {full_video_url}')
        save_path = os.path.join(save_directory, video_name)
        print(f'save video {video_name} ')
        download_video(full_video_url, save_path)
        print(f'Video {i+1} downloaded successfully.')

# 输入网站URL和保存视频的目录
website_url = 'https://sea-thru-nerf.github.io/'
save_directory = 'videos'

# 创建保存视频的目录
os.makedirs(save_directory, exist_ok=True)

# 爬取并下载视频
crawl_and_download_videos(website_url, save_directory)