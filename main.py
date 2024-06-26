import requests
from bs4 import BeautifulSoup
import sys
import json

APP_KEY = ""

api_url = "https://jwc.hdu.edu.cn/xkjs/list.htm"
response = requests.get(api_url, timeout=10)
response.encoding = "utf-8"
if response.status_code != 200:
    print("Net Error.")
    sys.exit(0)

soup = BeautifulSoup(response.text, "html.parser")
result = soup.find("ul", class_="news_list list2")
title = result.find_all("a")
date = result.find_all("div", class_="fr date")
# for i in range(len(title)):
#     print(date[i].text, title[i].get("title"), title[i].get("href"))

content: str = ""
count: int = 0
_json: dict = {}

with open("./jwc.json", "r", encoding="utf-8") as file:
    records = file.read()
    _json = json.loads(records)
    for i in range(len(title)):
        if date[i].text not in _json:
            _json[date[i].text] = []
        if title[i].get("title") not in _json[date[i].text]:
            _json[date[i].text].append(title[i].get("title"))
            count += 1
            content += (
                "<a href=https://jwc.hdu.edu.cn"
                + title[i].get("href")
                + ">"
                + str(count)
                + ". "
                + title[i].get("title")
                + "</a><br><br>"
            )

print("count=", count)
if count == 0:
    sys.exit(0)

print(content)

with open("./jwc.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(_json))

params = {
    "appkey": APP_KEY,
    "title": "教务处通知" + str(count) if count > 1 else "",
    "content": content,
}
resp = requests.get("https://cx.super4.cn/push_msg", params=params)
