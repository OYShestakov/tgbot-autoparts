import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import lxml
from selenium import webdriver
import time, random

# headers = Headers(headers=True).generate()
# url = "https://shop-donavtopribor.ru/magazin/search?s%5Bname%5D=700.00.67.096"
# options = webdriver.ChromeOptions()
# options.add_argument(f"user-agent={headers}")
# options.add_argument("--headless")
# driver = webdriver.Chrome(executable_path="/Users/olegsestakov/Python/tgbot-template/chromedriver",
#                           options=options
#                           )
#
# driver.get(url=url)
# time.sleep(random.uniform(3, 6))
# _ = driver.page_source
# category_link = item
# category_html = driver.page_source
# soup = BeautifulSoup(category_html, "lxml")
# pagenation_count = int(soup.find("div", class_="col-sm-6 text-right").text.split(" ")[-2])

headers = Headers(headers=True).generate()
url = "https://baza.drom.ru/sell_spare_parts/?goodPresentState%5B%5D=present&query=5320-2205025"
req = requests.get(url, headers)
src = req.text
print(src)
data_parts_list = []
soup = BeautifulSoup(src, "lxml")
try:
    data_parts = soup.find("tbody", class_="native").find_all("tr", class_="bull-item bull-item_inline -exact bull-item bull-item_inline")
    print(data_parts)
except Exception as ex:
    print(ex)

# for item_drom in data_parts:
#     try:
#         parts_link = "https://baza.drom.ru" + item_drom.find("div", class_="bull-item-content__subject-container").find("a").get("href")
#     except:
#         parts_link = "Ссылка отсутствует"
#     try:
#         parts_name = item_drom.find("div", class_="bull-item-content__subject-container").text.strip()
#     except:
#         parts_name = "Имя не указано"
#     try:
#         parts_price = item_drom.find("div", class_="price-block__price price-per-quantity").find("span", class_="price-per-quantity__price")
#     except:
#         parts_price = "Цена не указана"
#
#     data_parts_list.append(
#         {
#             "postavshik": "Белагро (Москва)",
#             "link": parts_link,
#             "name": parts_name,
#             "price": parts_price
#         }
#     )
#
# print(data_parts_list)
# print(len(data_parts_list))