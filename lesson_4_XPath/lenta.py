# Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости. Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.
# Сложить собранные новости в БД
from lxml import html
import requests
from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient
import hashlib
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['lenta_ru_news']
news = db.news

url = 'https://lenta.ru'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        '/100.0.4896.75 Safari/537.36'}
response = requests.get(url, headers=header)
dom = html.fromstring(response.text)
big_news = dom.xpath(".//div[@class='topnews__first-topic']//@href")
news_list = dom.xpath("//a[@class='card-mini _topnews']//@href")
news_list.append(big_news)


for news_link in news_list:
    if news_link[0] == '/':
        news_link = str(url) + str(news_link)
        news_table = {}
        response2 = requests.get(news_link, headers=header)
        dom2 = html.fromstring(response2.text)
        news_title = dom2.xpath("//h1[@class='topic-body__titles']//text()")
        news_date = dom2.xpath(".//time[@class='topic-header__item topic-header__time']//text()")
        news_parent = dom2.xpath(".//a[@class='topic-header__item topic-header__rubric']/text()")
        news_parent_site = dom2.xpath(".//a[@class='topic-header__item topic-header__rubric']/@href")

        news_table['news_title'] = news_title
        news_table['news_parent'] = news_parent
        news_table['news_parent_site'] = str(url) + str(news_parent_site[0])
        news_table['news_date'] = news_date
        news_table['news_link'] = news_link
        news_table['_id'] = hashlib.md5(str(news_table).encode('utf-8')).hexdigest()

        try:
            news.insert_one(news_table)
        except DuplicateKeyError:
            print(f"Document  {news_table['news_title']} already exist")

result = list(news.find({}))
pprint(result)

# Новостной портфель:
# [{'_id': '6d3cf44a5c0c677682730b91867160c2',
#   'news_date': ['18:31, 12 апреля 2022'],
#   'news_link': 'https://lenta.ru/news/2022/04/12/kinokno/',
#   'news_parent': ['Культура'],
#   'news_parent_site': 'https://lenta.ru/rubrics/culture/',
#   'news_title': ['Одна из голливудских киностудий задумала возобновить прокат '
#                  'фильмов в России']},
#  {'_id': '9c6f9a29eda0464f8517c92cc3df4aec',
#   'news_date': ['18:30, 12 апреля 2022'],
#   'news_link': 'https://lenta.ru/news/2022/04/12/ochendeshevo/',
#   'news_parent': ['Путешествия'],
#   'news_parent_site': 'https://lenta.ru/rubrics/travel/',
#   'news_title': ['Названы направления для поездок на майские праздники с '
#                  'билетами до тысячи рублей']},
#  {'_id': '1e997525a7fe6c392ddb313ac4563734',
#   'news_date': ['18:29, 12 апреля 2022'],
#   'news_link': 'https://lenta.ru/news/2022/04/12/lukashenkospace/',
#   'news_parent': ['Бывший СССР'],
#   'news_parent_site': 'https://lenta.ru/rubrics/ussr/',
#   'news_title': ['Соответствие Лукашенко требованиям для полета в космос '
#                  'оценили']},
#  {'_id': '4d068665ad57be925342c42672c71c03',
#   'news_date': ['18:29, 12 апреля 2022'],
#   'news_link': 'https://lenta.ru/news/2022/04/12/belorusyuyos/',
#   'news_parent': ['Экономика'],
#   'news_parent_site': 'https://lenta.ru/rubrics/economics/',
#   'news_title': ['Белоруссия ввела ограничения на вывоз ряда продуктов']},
#  {'_id': 'd745f3e79c7fdf74ee439f234371b654',
#   'news_date': ['18:24, 12 апреля 2022'],
#   'news_link': 'https://lenta.ru/news/2022/04/12/arondondon/',
#   'news_parent': ['Силовые структуры'],
#   'news_parent_site': 'https://lenta.ru/rubrics/forces/',
#   'news_title': ['Обвиняемый в похищении и убийстве шансонье Дон ранил себя в '
#                  'суде']},
#  {'_id': '0ee12dc9b316a91a387d8d3b79f27547',
#   'news_date': ['18:22, 12 апреля 2022'],
#   'news_link': 'https://lenta.ru/news/2022/04/12/pakistan/',
#   'news_parent': ['Мир'],
#   'news_parent_site': 'https://lenta.ru/rubrics/world/',
#   'news_title': ['Путин поздравил победителя выборов премьер-министра '
#                  'Пакистана']},
#  {'_id': '224004fe71a271624f1469fa84eebfcb',
#   'news_date': ['18:20, 12 апреля 2022'],
#   'news_link': 'https://lenta.ru/news/2022/04/12/placcdarm/',
#   'news_parent': ['Россия'],
#   'news_parent_site': 'https://lenta.ru/rubrics/russia/',
#   'news_title': ['В Госдуме заявили о планах США сделать Украину плацдармом '
#                  'для борьбы с Россией']},
#  {'_id': '780b060cd827a6ef142d682b1681a35f',
#   'news_date': ['18:19, 12 апреля 2022'],
#   'news_link': 'https://lenta.ru/news/2022/04/12/svoda_radio/',
#   'news_parent': ['Интернет и СМИ'],
#   'news_parent_site': 'https://lenta.ru/rubrics/media/',
#   'news_title': ['«Радио Свобода» пригрозили многомиллионным штрафом']},
#  {'_id': '909968252b7063dadfc9051702f8a1d5',
#   'news_date': ['18:19, 12 апреля 2022'],
#   'news_link': 'https://lenta.ru/news/2022/04/12/britnem/',
#   'news_parent': ['Среда обитания'],
#   'news_parent_site': 'https://lenta.ru/rubrics/realty/',
#   'news_title': ['Главные экономики Европы соединятся «невидимой сетью»']},
#  {'_id': '249a587a9150647ec84f23a259608851',
#   'news_date': ['18:18, 12 апреля 2022'],
#   'news_link': 'https://lenta.ru/news/2022/04/12/argue/',
#   'news_parent': ['Бывший СССР'],
#   'news_parent_site': 'https://lenta.ru/rubrics/ussr/',
#   'news_title': ['Появились новые подробности о взрыве театра в Мариуполе']},
#  {'_id': '139ea857dcde9cfc829c924c6977b8c5',
#   'news_date': ['17:47, 12 апреля 2022'],
#   'news_link': 'https://lenta.ru/news/2022/04/12/zel_stain/',
#   'news_parent': ['Бывший СССР'],
#   'news_parent_site': 'https://lenta.ru/rubrics/ussr/',
#   'news_title': ['Зеленский отказался принимать Штайнмайера в Киеве']}]