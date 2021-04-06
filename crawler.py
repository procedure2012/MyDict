import requests
from bs4 import BeautifulSoup

class MyDict:
    def __init__(self, url):
        self.headers = {"User-Agent": "User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}
        self.url = url + "{}"
    
    def get_web_result(self, url, word):
        t = url.format(word)
        r = requests.get(t, headers=self.headers)
        return BeautifulSoup(r.text, 'lxml')
    
    def lookup(self, word):
        pass
