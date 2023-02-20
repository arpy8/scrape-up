import requests
from bs4 import BeautifulSoup


class Issue:

    def __init__(self, username: str, repository_name:str, pull_request_number:int):
        self.username = username
        self.repository = repository_name
        self.pr_number = pull_request_number

    def __scrape_page(self):
        data = requests.get(f"https://github.com/{self.username}/{self.repository}/pull/{self.pr_number}")
        data = BeautifulSoup(data.text,"html.parser")
        return data