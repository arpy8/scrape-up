import requests
from bs4 import BeautifulSoup
import json


class Video:
   
    def __init__(self, video_url):
        self.video_url = video_url

    def getDetails(self):
        
        url = self.video_url
        try:
            res = requests.get(url)
            soup = BeautifulSoup(res.text, "html.parser")
            video_data = {"video_data": []}

            scripts = soup.find_all("script")
            req_script = scripts[44].text.strip()
            script = req_script[20:-1]
            data = json.loads(script)

            base = data["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"]

            first = base[0]["videoPrimaryInfoRenderer"]
            title = first["title"]["runs"][0]["text"].strip().encode("ascii", "ignore").decode()
            views = first["viewCount"]["videoViewCountRenderer"]["viewCount"]["simpleText"]
            date = first["dateText"]["simpleText"]

            channel_data = base[1]["videoSecondaryInfoRenderer"]["owner"]["videoOwnerRenderer"]
            avatar = channel_data["thumbnail"]["thumbnails"][2]["url"]
            name = channel_data["title"]["runs"][0]["text"]
            channel_url = channel_data["title"]["runs"][0]["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"]
            subs = channel_data["subscriberCountText"]["accessibility"]["accessibilityData"]["label"]
            
            desc = base[1]["videoSecondaryInfoRenderer"]["attributedDescription"]["content"].strip().encode("ascii", "ignore").decode()
            comment_count = base[2]["itemSectionRenderer"]["contents"][0]["commentsEntryPointHeaderRenderer"]["commentCount"]["simpleText"]
                                    
            video_data["video_data"].append(
                {
                    "title": title,
                    "description": desc[:200]+"...",
                    "views_count": views,
                    "upload_date": date,
                    "comment_count": comment_count,
                    "channel_name": name,
                    "channel_avatar": avatar,
                    "subscriber_count": subs,
                    "channel_url": "https://youtube.com" + channel_url,
                }
            )
            res_json = json.dumps(video_data)
            return res_json
        except:
            error_message = {
                "message": "Can't fetch any articles from the topic provided."
            }
            ejson = json.dumps(error_message)
            return ejson

vid = Video("https://www.youtube.com/watch?v=bc0g7rNUMCE")
print(vid.getDetails())