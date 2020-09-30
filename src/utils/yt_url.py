import re
import pafy
from urllib.request import urlopen


class YoutubeUrl:
    def __init__(self, query):
        self.query = "+".join(query.split())
        self.search_url = f"https://www.youtube.com/results?search_query={self.query}"

    def get_video_url(self):
        '''Extracts the firt url from youtube search result'''
        html = urlopen(self.search_url).read().decode()
        video_ids = re.findall(r"watch\?v=(\S{11})", html)
        if not video_ids:
            return None
        video_url = f"https://www.youtube.com/watch?v={video_ids[0]}"
        return video_url

    def get_video_info(self, url):
        '''Extracts the song info from the given url'''
        if not url:
            return None
        video = pafy.new(url)
        thumbnail = video.thumb
        title = video.title
        duration = video.duration
        return {'url': url, 'title': title, 'thumbnail': thumbnail, 'duration': duration}
