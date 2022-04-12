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
db = client['mail_ru_news']
news = db.news


url = 'https://news.mail.ru/'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        '/100.0.4896.75 Safari/537.36'}
response = requests.get(url, headers=header)
dom = html.fromstring(response.text)
news_list = list(set(dom.xpath(".//div [@data-logger='news__MainTopNews']//@href")))


for news_link in news_list:
    news_table = {}
    response2 = requests.get(news_link, headers=header)
    dom2 = html.fromstring(response2.text)
    news_title = dom2.xpath("//h1[@class='hdr__inner']/text()")
    news_date = dom2.xpath(".//span[@class='note__text breadcrumbs__text js-ago']/@datetime")
    news_parent = dom2.xpath(".//a[@class='link color_gray breadcrumbs__link']//text()")
    news_parent_site = dom2.xpath(".//a[@class='link color_gray breadcrumbs__link']//@href")

    news_table['news_title'] = news_title
    news_table['news_parent'] = news_parent,news_parent_site
    news_table['news_date'] = news_date[0].replace('T', ' ')
    news_table['news_link'] = news_link
    news_table['_id'] = hashlib.md5(str(news_table).encode('utf-8')).hexdigest()

    try:
            news.insert_one(news_table)
    except DuplicateKeyError:
            print(f"Document  {news_table['news_title']} already exist")


result = list(news.find({}))
pprint(result)

# Новостной портфель:
# [{'_id': '1e49cf66c73f6981bef01b0e8da50b00',
#   'news_date': '2022-04-12 17:46:33+03:00',
#   'news_link': 'https://news.mail.ru/incident/50855586/',
#   'news_parent': [['Ведомости'], ['https://www.vedomosti.ru/']],
#   'news_title': ['Лукашенко назвал события в Буче спецоперацией '
#                  'Великобритании']},
#  {'_id': 'bb921062a97ba62ac11c1294e476e575',
#   'news_date': '2022-04-12 16:27:30+03:00',
#   'news_link': 'https://news.mail.ru/politics/50853519/',
#   'news_parent': [['© РИА Новости'], ['http://www.ria.ru']],
#   'news_title': ['Путин назвал Украину, Россию и Белоруссию триединым '
#                  'народом']},
#  {'_id': 'd7aa65e3f328890fb037c75589785649',
#   'news_date': '2022-04-12 16:00:42+03:00',
#   'news_link': 'https://news.mail.ru/politics/50853506/',
#   'news_parent': [['© РИА Новости'], ['http://www.ria.ru']],
#   'news_title': ['Лукашенко призвал США «вспомнить лидера, который хотел '
#                  'изменить мир»']},
#  {'_id': '89492b8f794f0701cb6fd0fa63b7c5c2',
#   'news_date': '2022-04-12 15:16:57+03:00',
#   'news_link': 'https://news.mail.ru/economics/50852479/',
#   'news_parent': [['Ведомости'], ['https://www.vedomosti.ru/']],
#   'news_title': ['Минэкономики Германии подготовило законопроект о '
#                  'национализации энергокомпаний']},
#  {'_id': 'cdc52bc1ec51ce587e4f651ac9af5a3d',
#   'news_date': '2022-04-12 10:45:26+03:00',
#   'news_link': 'https://news.mail.ru/economics/50844935/',
#   'news_parent': [['ИА REGNUM'], ['http://regnum.ru/']],
#   'news_title': ['Банк России запланировал модернизацию денежных купюр']},
#  {'_id': '3e6cb28e7b72000b42b870088edfa5fe',
#   'news_date': '2022-04-12 17:01:59+03:00',
#   'news_link': 'https://news.mail.ru/incident/50854995/',
#   'news_parent': [['РБК'], ['https://www.rbc.ru/']],
#   'news_title': ['В метро Нью-Йорка произошла стрельба']},
#  {'_id': '9c235f56bf9f7e31e9b2b69186cdfc7b',
#   'news_date': '2022-04-12 10:23:41+03:00',
#   'news_link': 'https://news.mail.ru/incident/50846820/',
#   'news_parent': [['© РИА Новости'], ['http://www.ria.ru']],
#   'news_title': ['Российская армия пресекла попытку украинских военных '
#                  'покинуть Мариуполь']},
#  {'_id': 'fcf103da1e1fe75e0c4542b9841d3d4e',
#   'news_date': '2022-04-12 17:14:28+03:00',
#   'news_link': 'https://news.mail.ru/politics/50855121/',
#   'news_parent': [['Коммерсантъ'], ['http://www.kommersant.ru']],
#   'news_title': ['Путин заявил, что Украина отошла от достигнутых в Стамбуле '
#                  'договоренностей']},
#  {'_id': 'f0672c6a7714550761a1d844b91bdfd6',
#   'news_date': '2022-04-12 13:10:54+03:00',
#   'news_link': 'https://news.mail.ru/incident/50850397/',
#   'news_parent': [['© РИА Новости'], ['http://www.ria.ru']],
#   'news_title': ['В Одессе начала работать группа НАТО, сообщил источник']},
#  {'_id': '8ccf987c9c1c3012df6aaebf843d91e1',
#   'news_date': '2022-04-12 15:35:13+03:00',
#   'news_link': 'https://sportmail.ru/news/hockey/50853134/',
#   'news_parent': [['ТАСС'], ['http://www.tass.ru/']],
#   'news_title': ['Умер олимпийский чемпион 1988 года по хоккею Сергей Яшин']},
#  {'_id': '18759f30b4a15f78c9fca0c67e10ca9f',
#   'news_date': '2022-04-12 12:48:48+03:00',
#   'news_link': 'https://news.mail.ru/incident/50849319/',
#   'news_parent': [['ТАСС'], ['http://www.tass.ru/']],
#   'news_title': ['В России семь дней подряд регистрируют менее 300 смертей '
#                  'из-за коронавируса в сутки']}]