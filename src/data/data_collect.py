from bs4 import BeautifulSoup as bs
from time import sleep

from tqdm import tqdm as tq
import requests

from src.data.utils import bbc_content

link, author, date, text, images = [], [], [], [], []


def information_extraction(
    json_content=None, ind=None, content=None, inp_type=None
):
    if inp_type == "json":
        try:
            link.append(json_content[ind]["url"])
            try:
                images.append(
                    [
                        json_content[ind]["image"]["ichefHref"].replace(
                            "{width}", "240"
                        )
                    ]
                )
            except:
                images.append(["nan"])
            text.append([json_content[ind]["title"]])
        except:
            pass
    else:
        width = content.find("div", {"class": "gs-o-media-island"}).find(
            "img"
        )["src-widths"][1:4]
        images.append(
            [
                content.find("div", {"class": "gs-o-media-island"})
                .find("img")["src-src"]
                .replace("{width}", width)
            ]
        )
        link.append(content.find("a")["href"])
        text.append([content.find("a").text])


def news_scraping(path):
    article = requests.get(path + "/news/science-environment-56837908")
    soup = bs(article.content, "html.parser")
    (
        main1,
        main2,
        Global_cont,
        climate_cont,
        features_cont,
        api,
        class1,
        class2,
        sub_class2,
    ) = bbc_content(soup)

    topics = [Global_cont, climate_cont, features_cont]

    images.append([main1.find("img")["src"]])
    text.append([main1.find("a").text])
    link.append(main1.find("a")["href"])

    for c in class1:
        content = main2.findAll("div", {"class": c})
        if len(content) == 1:
            information_extraction(content=content[0])
        else:
            for i in range(len(content)):
                information_extraction(content=content[i])

    for topic in topics:
        for c in class2:
            content = topic.findAll("div", {"class": c})
            if len(content) == 1:
                for j in sub_class2:
                    sub_content = content[0].find("div", {"class": j})
                    information_extraction(content=sub_content)
            else:
                for i in range(len(content)):
                    information_extraction(content=content[i])

    print('loop over pages:')
    for i in tq(range(0, 50, 3)):
        url = (
            api[0]
            + api[1]
            + str(i)
            + api[2]
            + api[1]
            + str(i + 1)
            + api[2]
            + api[1]
            + str(i + 2)
            + api[3]
        )
        s = requests.Session()
        res = s.get(url)
        res.raise_for_status()

        data = res.json()["payload"]

        for k in range(3):
            json_content = data[k]["body"]["results"]
            for ind in range(len(json_content)):
                information_extraction(
                    json_content=json_content, ind=ind, inp_type="json"
                )


def news_page_scraping(path):
    for i in link:
        if "https" in i:
            index = link.index(i)
            del link[index]
            del text[index]
            del images[index]
    print('loop over news links:')

    for i in tq(range(len(link))):
        url = link[i]
        try:
            article = requests.get(path + url)
            soup = bs(article.content, "html.parser")
            head = soup.find(
                "header", {"class": "ssrcss-hrw5ob-HeadingWrapper e1nh2i2l5"}
            )

            try:
                date.append(head.find("time")["datetime"])
            except:
                date.append("nan")

            try:
                author.append(head.find("p").find("strong").text)
            except:
                author.append("nan")

            IMG = soup.findAll("div", {"src-component": "image-block"})
            for j in range(len(IMG)):
                images[i].append(
                    list(IMG[j].find("img")["srcset"].split(" "))[0]
                )
            TEXT = soup.findAll("div", {"src-component": "text-block"})
            for j in range(len(TEXT)):
                text[i].append(TEXT[j].find("p").text)
        except:
            sleep(10)
            continue

    return  link, author, date, text, images

def data_collection():
    path = "https://www.bbc.com"
    print("Scrape news links:")
    news_scraping(path)

    print('Scrape content of news pages:')
    return news_page_scraping(path)

