import json
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ReplyKeyboardRemove
from tg_bot.keybords.memu import menu
from tg_bot.misc.states import SearchArticle
from aiogram.dispatcher import FSMContext
from bs4 import BeautifulSoup
import requests
import lxml
from fake_headers import Headers
from aiogram.utils.markdown import hbold, hlink


async def show_menu(message: types.Message):
    await message.answer("Выберите вариант поиска из меню ниже", reply_markup=menu)


async def search_articles(message: types.Message):
    await message.answer("Введите артикулы через запятую", reply_markup=ReplyKeyboardRemove())
    await SearchArticle.step1.set()


async def input_article(message: types.Message, state: FSMContext):
    articles = message.text.split(",")
    json_file_number = message.from_user.id

    with open(f"data/file_{json_file_number}.json", "w") as file:
        ...

    headers = Headers(headers=True).generate()
    data_parts_list = []
    for item in articles:
        url = f"https://kspecmash.su/products/?search={item}"
        req = requests.get(url, headers)
        src = req.text
        soup = BeautifulSoup(src, "lxml")
        try:
            result_search = soup.find("div", class_="text search-legend").text.split(" ")[-2]
        except:
            pass
        if result_search == 0:
            pass
        else:
            data_parts = soup.find_all("div", class_="goods__item")
            for item_21_vek in data_parts:
                try:
                    parts_link = item_21_vek.find("a").get("href")
                except:
                    parts_link = "Ссылка отсутствует"
                try:
                    parts_name = item_21_vek.find("a", class_="lnk goods__name").text
                except:
                    parts_name = "Наименование отсутствует"
                try:
                    parts_price = item_21_vek.find("span", class_="price price_existing p_price").find("span",
                                                                                                       class_="price__value notranslate").text

                except:
                    parts_price = "Цена отсутствует"
                data_parts_list.append(
                    {
                        "postavshik": "21 век (Москва)",
                        "link": parts_link,
                        "name": parts_name,
                        "price": parts_price
                    }
                )

        # Теперь отправляем запросы на сайт agro-shop
        headers = Headers(headers=True).generate()
        url = f"https://agro-shop.ru/catalog/index.php?q={item}"
        req = requests.get(url, headers)
        src = req.text

        soup = BeautifulSoup(src, "lxml")
        try:
            data_parts = soup.find_all("div", class_="col-12 tovar-card-horizontal")
        except:
            pass

        for item_agro_shop in data_parts:
            try:
                parts_link = "https://agro-shop.ru" + item_agro_shop.find("div", class_="col-5 col-sm-6 col-md-5 col-lg-5 d-flex flex-column card-footer").find( "a").get("href")
            except:
                parts_link = "Ссылка отсутствует"
            try:
                parts_name = item_agro_shop.find("div",
                                                 class_="col-5 col-sm-6 col-md-5 col-lg-5 d-flex flex-column card-footer").find(
                    "div", class_="card-title h6").text.strip()
            except:
                parts_name = "Имя не указано"
            try:
                parts_price = "https://agro-shop.ru" + item_agro_shop.find("div", class_="card-price").find("img",
                                                                                                            class_="mobile").get(
                    "src")
            except:
                parts_price = "Цена не указана"

            data_parts_list.append(
                {
                    "postavshik": "Агрошоп (Барнаул)",
                    "link": parts_link,
                    "name": parts_name,
                    "price": parts_price
                }
            )
#Делаем запрос на альфатрейд Питер
        headers = Headers(headers=True).generate()
        url = f"https://alfatradespb.ru/shop?search={item}"
        req = requests.get(url, headers)
        src = req.text
        soup = BeautifulSoup(src, "lxml")
        try:
            data_parts = soup.find_all("div", class_="oe_product oe_list oe_product_cart")
        except Exception as ex:
            print(ex)

        for item_alfatrade in data_parts:
            try:
                parts_link = "https://alfatradespb.ru" + item_alfatrade.find("h6").find("a").get("href")
            except:
                parts_link = "Ссылка отсутствует"
            try:
                parts_name = item_alfatrade.find("h6").text.strip()
            except:
                parts_name = "Имя не указано"
            try:
                parts_price = item_alfatrade.find("span", class_="oe_currency_value").text
            except:
                parts_price = "Цена не указана"

            data_parts_list.append(
                {
                    "postavshik": "Альфа-трейд (Питер)",
                    "link": parts_link,
                    "name": parts_name,
                    "price": parts_price
                }
            )

#Отправляем запрос на сайт агрокомплект Белгород

        headers = Headers(headers=True).generate()
        url = f"https://agrokomplekt24.ru/catalog/?q={item}"
        req = requests.get(url, headers)
        src = req.text
        soup = BeautifulSoup(src, "lxml")
        try:
            data_parts = soup.find_all("div", class_="col-lg-3 col-md-4 col-sm-6 col-xs-6 col-xxs-12 item item-parent item_block")

        except Exception as ex:
            pass

        for item_agrokomplekt in data_parts:
            try:
                parts_link = "https://agrokomplekt24.ru" + item_agrokomplekt.find("div", class_="item-title").find("a").get("href")
            except:
                parts_link = "Ссылка отсутствует"
            try:
                parts_name = item_agrokomplekt.find("div", class_="item-title").find("span").text.strip()
            except:
                parts_name = "Имя не указано"
            try:
                parts_price = item_agrokomplekt.find("div", class_="price font-bold font_mxs").find("span", class_="price_value").text.strip()

            except:
                parts_price = "Цена не указана"

            data_parts_list.append(
                {
                    "postavshik": "Агрокомплект (Белгород)",
                    "link": parts_link,
                    "name": parts_name,
                    "price": parts_price
                }
            )

#Отправляем запрос на каскад агро Курск

        headers = Headers(headers=True).generate()
        url = f"https://cascad-agro.ru/catalog/?q={item}"
        req = requests.get(url, headers)
        src = req.text
        soup = BeautifulSoup(src, "lxml")
        try:
            data_parts = soup.find_all("div", class_="item_block col-4 col-md-3 col-sm-6 col-xs-6")
        except:
            pass

        for item_caskad in data_parts:
            try:
                parts_link = "https://cascad-agro.ru" + item_caskad.find("div", class_="image_wrapper_block").find("a").get("href")
            except:
                parts_link = "Ссылка отсутствует"
            try:
                parts_name = item_caskad.find("div", class_="item-title").find("span").text.strip()
            except:
                parts_name = "Имя не указано"
            try:
                parts_price = item_caskad.find("span", class_="price_value").text.strip()
            except:
                parts_price = "Цена не указана"

            data_parts_list.append(
                {
                    "postavshik": "Каскад-Агро (Курск)",
                    "link": parts_link,
                    "name": parts_name,
                    "price": parts_price
                }
            )

#Делаем запрос на сайт русагросеть москва

        headers = Headers(headers=True).generate()
        url = f"http://rusagroset.ru/search/index.php?q={item}"
        req = requests.get(url, headers)
        src = req.text
        soup = BeautifulSoup(src, "lxml")
        try:
            data_parts = soup.find_all("div", class_="search-item")
        except:
            pass

        for item_rusagro in data_parts:
            try:
                parts_link = "http://rusagroset.ru" + item_rusagro.find("h4").find("a").get("href")
            except:
                parts_link = "Ссылка отсутствует"
            try:
                parts_name = item_rusagro.find("div", class_="search-preview").text.strip()
            except:
                parts_name = "Имя не указано"

            data_parts_list.append(
                {
                    "postavshik": "Русагросеть (Москва)",
                    "link": parts_link,
                    "name": parts_name,
                    "price": "Для получения цены перейди по ссылке"
                }
            )

#Отправляем запрос на сайт Белагро

        headers = Headers(headers=True).generate()
        url = f"https://1belagro.com/search/?q={item}"
        req = requests.get(url, headers)
        src = req.text
        soup = BeautifulSoup(src, "lxml")
        try:
            data_parts = soup.find("div", class_="search_list").find_all("tr")
        except:
            pass

        for item_belagro in data_parts:
            try:
                parts_link = "https://1belagro.com" + item_belagro.find("td", class_="goods").find("a", class_="basket-name").get("href")
            except:
                parts_link = "Ссылка отсутствует"
            try:
                parts_name = item_belagro.find("td", class_="goods").find("a", class_="basket-name").text.strip()
            except:
                parts_name = "Имя не указано"
            try:
                parts_price = item_belagro.find("div", class_="buyer").find("span").find_next().text.strip()
            except:
                parts_price = "Цена не указана"

            data_parts_list.append(
                {
                    "postavshik": "Белагро (Москва)",
                    "link": parts_link,
                    "name": parts_name,
                    "price": parts_price
                }
            )


    with open(f"data/file_{json_file_number}.json", "a") as file:
        json.dump(data_parts_list, file, indent=4, ensure_ascii=False)

    with open(f"data/file_{json_file_number}.json") as file:
        data = json.load(file)

    for item_dict in data:
        card = f"{hlink(item_dict.get('postavshik'), item_dict.get('link'))}\n" \
               f"{hbold('Наименование - ')} {item_dict.get('name')}\n" \
               f"{hbold('Цена - ')} {item_dict.get('price')}"
        await message.answer(card, disable_web_page_preview=True)


async def search_names(message: types.Message):
    await message.answer(f"Вы выбрали {message.text}", reply_markup=ReplyKeyboardRemove())


def register_showing_menu(dp: Dispatcher):
    dp.register_message_handler(show_menu, Command("поиск"))
    dp.register_message_handler(search_articles, text="Поиск по артикулам")
    dp.register_message_handler(search_names, text="Поиск по названию")
    dp.register_message_handler(input_article, state=SearchArticle.step1)
