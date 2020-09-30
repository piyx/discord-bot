from googleapiclient.discovery import build


class Youtube:
    def __init__(self, query):
        self.query = query
        self.youtube_api_key = "AIzaSyC4w-IhAzlfR7t2WJv-TLid3PYUiOq8dLY"
        self.api_service_name = "youtube"
        self.api_version = "v3"

    def search(self):
        youtube = build(self.api_service_name, self.api_version,
                        developerKey=self.youtube_api_key)

        request = youtube.search().list(
            q=self.query,
            part="id, snippet",
            maxResults=1
        )
        response = request.execute()

        items = response['items']
        if not items:
            return None
        try:
            items = items[0]
            url = f"https://www.youtube.com/watch?v={items['id']['videoId']}"
            thumnail = items['snippet']['thumbnails']['default']['url']
            title = items['snippet']['title']

        except Exception as e:
            return None

        return {'url': url, 'thumbnail': thumnail, 'title': title}
