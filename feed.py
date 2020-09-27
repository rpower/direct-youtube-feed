import os
import feedparser
import youtube_dl
from youtube_dl.utils import DateRange
from feedgen.feed import FeedGenerator

# Read channel IDs from text file
text_file_name = 'channel_ids.txt'
with open(text_file_name) as f:
    channel_ids_list = f.readlines()
channel_ids_list = [x.strip() for x in channel_ids_list]
channel_ids_list = [x.replace('https://www.youtube.com/channel/', '') for x in channel_ids_list]

def download_yt_video(video_url):
    ydl_opts = {
        'ignoreerrors': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(video_url, download = False)
        video_file_url = meta['requested_formats'][0]['url']
        return video_file_url

for yt_channel_id in channel_ids_list:
    max_videos_per_channel = 10
    yt_feed = feedparser.parse(f'https://www.youtube.com/feeds/videos.xml?channel_id={yt_channel_id}')

    yt_videos_list = yt_feed.entries
    yt_account_username = yt_videos_list[0].author_detail.name
    yt_channel_url = yt_videos_list[0].author_detail.href

    fg = FeedGenerator()
    fg.title(yt_account_username)
    fg.description(yt_account_username)
    fg.link(href = yt_channel_url)

    for video in yt_videos_list[:max_videos_per_channel]:
        try:
            yt_video_url = download_yt_video(video.link)
        except:
            yt_video_url = video.link

        yt_video_title = video.title
        yt_video_id = video.yt_videoid
        yt_video_publish_time = video.published

        fe = fg.add_entry()
        fe.id(yt_video_url)
        fe.title(yt_video_title)
        fe.link(href = yt_video_url)
        fe.pubDate(yt_video_publish_time)

        os.chdir('../../public_html/yt_rss_feeds')
        fg.rss_file(f'feeds/{yt_channel_id}.xml')