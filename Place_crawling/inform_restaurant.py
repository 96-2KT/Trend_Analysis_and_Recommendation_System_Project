import requests
import pandas as pd
import scrapy
from scrapy.http import TextResponse
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs
import urllib.request as ur
import numpy as np


def inform_restaurant(url):
    html = ur.urlopen(url)
    soup = bs(html.read(), "html.parser")

    # 이름,별점,블로그,방문자 리뷰
    title = soup.find("span", "_3XamX").text  # 제목
    sort = soup.find("span", "_3ocDE").text  # 곰탕,설렁탕 < 같은 설명

    # tag = soup.find("div", "_1kUrA")

    tag = soup.find("div", "_37n49")
    star, visit, blog = 0, 0, 0

    if tag.find("span", "_1Y6hi _1A8_M"):
        star = tag.find("span", "_1Y6hi _1A8_M").text[2:][:-2]

    if tag.find_all("span", "_1Y6hi"):
        for i in tag.find_all("span", "_1Y6hi"):
            if i.find("a"):
                href = i.find("a").get("href")
                if href.split("/")[-1] == "visitor":
                    visit = int(i.text.split()[-1].replace(",", ""))
                else:
                    blog = int(i.text.split()[-1].replace(",", ""))

    # 메뉴
    menu_url = url[:-4] + "menu/list"
    menu_html = ur.urlopen(menu_url)
    menu_soup = bs(menu_html.read(), "html.parser")

    menu_ = menu_soup.find_all("li", "_3j-Cj")
    price_list = []
    menu_list = []
    for i in menu_:
        name = i.find("span", "_3yfZ1").text  # 메뉴명
        price = i.find("div", "_3qFuX").text  # 메뉴 가격
        menu_list.append(name)
        if price != "변동" and "원" in price:

            price_list.append(int(price[:-1].replace(",", "")))
    mean_price = int(np.mean(price_list))  # 평균 가격

    # 리뷰
    review_url = url[:-4] + "review/visitor"
    review_html = ur.urlopen(review_url)
    review_soup = bs(review_html.read(), "html.parser")
    people_give_score = review_soup.find_all("span", "_1fvo3")

    people_give_score = people_give_score[1].text.split()
    people_give_score = int(people_give_score[2].replace("명", "").replace(",", ""))

    # 딕셔너리 정의하기
    inform = {}
    inform["name"] = title
    inform["sort"] = sort
    inform["main_menu"] = ",".join(menu_list)
    inform["mean_price"] = mean_price
    inform["score"] = star
    inform["review_count"] = blog + visit
    inform["people_give_score"] = people_give_score
    return inform
