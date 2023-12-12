from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv

target_url = "https://wikiwiki.jp/nijisanji/%E3%83%A1%E3%83%B3%E3%83%90%E3%83%BC%E3%83%87%E3%83%BC%E3%82%BF%E4%B8%80%E8%A6%A7/YouTube%E3%83%81%E3%83%A3%E3%83%B3%E3%83%8D%E3%83%AB"

def get_channel_urls():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(target_url)

    soup = BeautifulSoup(driver.page_source.encode("utf-8"), "html.parser")
    channel_names = [
        v.text for v in soup.find_all("a", attrs={"class": "ext"})
    ][3:]
    channel_URLs = [
        v["href"] for v in soup.find_all("a", attrs={"class": "ext"})
        if "youtube.com" in v["href"]
    ]

    f = open('channel_urls.csv', 'w', newline='')
    data = [channel_names, channel_URLs]
    writer = csv.writer(f)
    writer.writerows(data)
    f.close()

if __name__ == "__main__":
    get_channel_urls()