import requests
from bs4 import BeautifulSoup
import string
import os

def write(dir, writelist):
    if not os.path.exists(dir):
        os.mkdir(dir)

    for item in writelist:
        filename, link = item
        link = "https://www.nature.com" + link
        r = requests.get(link, headers={'Accept-Language': 'en-US,en;q=0.5'})
        if r.status_code != 200:
            return
        soup = BeautifulSoup(r.content, 'html.parser')
        body = soup.body
        div = body.find("div", {"class" : "article__body"})
        if div is None:
            div = body.find("div", {"class" : "article-item__body"})
        text = div.get_text()
        path = os.path.join(dir, filename) 
        file = open(path, "w", encoding="utf-8")
        file.write(text)
        file.close()

def scrape_page(pageno, article_type):
    url = f"https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page={pageno}"
    r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    if r.status_code != 200:
        return
    soup = BeautifulSoup(r.content, 'html.parser')
    articles = soup("article")
    writelist = []
    for article in articles:
        span = article.find('span', {"data-test" : "article.type"})
        if span.get_text().replace("\n", "") == article_type:
            title = article.a.get_text().replace("\n", "")
            title = title.translate(str.maketrans("", "", string.punctuation))
            title = title.strip()
            title = title.replace(" ", "_")
            title += ".txt"
            link = article.a.get("href")
            writelist.append([title, link])
    dir = f"Page_{pageno}"
    write(dir, writelist)

pages = int(input())
article_type = input()

for i in range(pages):
    scrape_page(i + 1, article_type)
