from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
import time
import pandas as pd

koushiki_url = "https://wikiwiki.jp/nijisanji/%E5%85%AC%E5%BC%8F%E3%83%A9%E3%82%A4%E3%83%90%E3%83%BC"
target_url = "https://wikiwiki.jp/nijisanji/%E6%B4%BB%E5%8B%95%E5%A0%B4%E6%89%80"

def get_youtube_twitter_urls():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(target_url)
    soup = BeautifulSoup(driver.page_source.encode("utf-8"), "html.parser")
    # ライバー名一覧リスト、jsonで{ライバー名、YoutubeのURL, TwitterのURL}
    # youtube辞書、twitter辞書 and
    liver_twitter_dict = {}
    liver_youtube_dict = {}
    for ul in soup.find_all("ul", attrs={"class": "list1"}):
        for li in ul.find_all("li"):
            if '：' in li.text:
                text = li.text.split('：')[0]
                twitter = [
                    v['href'] for v in li.find_all("a", attrs={"class": "ext"})
                    if "twitter.com" in v['href']
                ]
                if len(twitter) > 0:
                    liver_twitter_dict[text] = twitter[0]

                youtube = [
                    v['href'] for v in li.find_all("a", attrs={"class": "ext"})
                    if "youtube.com/channel/" in v['href']
                ]
                if len(youtube) > 0:
                    liver_youtube_dict[text] = youtube[0]
                    

    # 結合
    liver_twitter_keys = list(liver_twitter_dict.keys())
    liver_youtube_keys = list(liver_youtube_dict.keys())
    liver_name_list = list(set(liver_twitter_keys) & set(liver_youtube_keys))
    liver_list = []
    for liver in liver_name_list:
        liver_dict = {'name': liver, 'youtube': liver_youtube_dict[liver], 'twitter': liver_twitter_dict[liver]}
        liver_list.append(liver_dict)

    df = pd.json_normalize(liver_list)
    df.to_csv("liver_info.csv", encoding="utf-8")
    df.T.to_csv("liver_info_line.csv", encoding="utf-8")

def a():
    driver_child = webdriver.Chrome(chrome_options=options)
    driver_child.get("https://wikiwiki.jp/"+item['href'])
    soup_child = BeautifulSoup(driver_child.page_source.encode("utf-8"), "html.parser")
    youtube = [
        v['href'] for v in soup_child.find_all("a", attrs={"class": "ext"})
        if "youtube.com" in v['href']
    ]
    twitter = [
        v['href'] for v in soup_child.find_all("a", attrs={"class": "ext"})
        if "twitter.com" in v['href']
    ]
    liver_map = {'name': item['title'], 'wiki': item['href'], 'youtube': youtube, 'twitter': twitter}
    liver_list.append(liver_map)

    df = pd.json_normalize(liver_list)
    df.to_csv("liver_info.csv", encoding="utf-8")

    # ファイルに書き出し、行ごとにライバー名、YoutubeのURL, TwitterのURL
    f = open('liver_info_line.csv', 'w', newline='')
    name_list = [d.get('name') for d in liver_list]
    wiki_list = [d.get('wiki') for d in liver_list]
    youtube_list = [d.get('youtube') for d in liver_list]
    twitter_list = [d.get('twitter') for d in liver_list]
    data = [name_list, wiki_list, youtube_list, twitter_list]
    writer = csv.writer(f)
    writer.writerows(data)
    f.close()

if __name__ == "__main__":
    get_youtube_twitter_urls()