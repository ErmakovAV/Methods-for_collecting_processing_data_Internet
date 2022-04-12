# Модуляция в ChroPath: работаем с новостями Яндекс. Для выбора конкретной вкладки
# правой кнопкой выбираем толко её конечный адрес.
# 1. Выбор первого элемента: //ol/li[1]
# 2. Выбор последнего элемента: //ol/li[last()]
# 3. Выбор предпоследнего элемента: //ol/li[last()-1]
# 4. Выбор всех кроме первого, срез: //ol/li[position()>1]
# 5. Топ три: //ol/li[position()<4]
# 6. Выбираем вторую и третью новости: //ol/li[position()<4 and position()>1]
# 7. Выбираем первую и четвёртую новости: //ol/li[position()=4 or position()=1]
# 8. Выбор тэга <div class="weather__temp xpath="1">+5</div>
# тэг с температурой сейчас: </div>//div[@class='weather__temp']
# 9. Выберем биржевые котировки: //div[@class='stocks__item-title']
# 10. Выделим картинку иконки погод <div class="weather__icon weather__icon_ovc" title="пасмурно" xpath="1"></div>,
# атрибут класса нужно задавать полностью с пробелами от кавычки до кавычки:
# //div[@class='weather__icon weather__icon_ovc']
# 11. Поиск по любой части вхождения в класс: //div[contains(@class,'_icon weath')] здесь - кусок погоды

# Парсим сайт CIAN.ru
# Выберем квартиры 3-ёх комнатные и выведем их тэги:
# 0. Выводит 277 элемента: //a[contains(@class,'--link--')]
# Выводит 253 элемента: //div/a[contains(@class,'--link--')]
# 1. Выводит 28 элементов: //div[@data-name='LinkArea']/a[contains(@class,'--link--')]
# 2. Контейнер с классом линк не нужен, мы получаем те же значения 28 эл-ов: //div[@data-name='LinkArea']/a
# для выборки по нашей задаче достаточно только внешнего контейнера и элемента "а"
# 3. Список из 28 ссылок: //div[@data-name='LinkArea']/a/@href
# 4. Выборка текста дала 0 результатов, его просто нет: //div[@data-name='LinkArea']/a/text()


# теперь поработаем с сайтом ebay.com сделаем выборку по наручным часам
from lxml import html
import requests
from pprint import pprint

url = 'https://ru.ebay.com/b/Wristwatches/31387/bn_2408451'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        '/100.0.4896.75 Safari/537.36'}

response = requests.get(url, headers=header)

# поработаем с текстовой строкой
dom = html.fromstring(response.text)

# html код мы получить не можем, а только тэги, <Element h3 at 0x1ff36c136f0> типа такого:
# names = dom.xpath("//h3[@class='s-item__title']")
# в тэгах есть текст - добавим текстовые узлы:
names = dom.xpath("//h3[@class='s-item__title']/text()")
# pprint(names)
# print(len(names))
# //h3[@class='s-item__title']/.. получим родителя ссылки, поднявшись на шаг наверх
# //h3[@class='s-item__title']/../@href теперь соберём наши адреса: href="https://www.ebay.com/
# itm/362768766864?hash=item5476b41790:g:qo0AAOSwENVdkCzN&var=631923551054"
links = dom.xpath(".//h3[@class='s-item__title']/../@href")
# pprint(links)
# выделим текст из тэга цены, получим только 11 результатов, нужно анализировать написание цены.
# Мы анализировали только детей, а в некоторых прайсах есть ещё вложения разделяющие
# на мин-макс цену или добавляющие написание цены курсивом!
price = dom.xpath("//span[@class='s-item__price']/text()")
# Добавим ещё один слэш и будем искать текст среди всех потомков, а не только среди детей,
# теперь получим не 48 цен, а 60:
price = dom.xpath("//span[@class='s-item__price']//text()")
#pprint(price)
#pprint(len(price))
# Проблема в том, что в некоторых позициях 2 цены и текст. от и до
info = dom.xpath("//span[contains(@class,'s-item__hotness')]/span/text()")
# pprint(info)
# Мы получили значения ссылок на оставшееся количество товара, но к какому именно товару они относятся - не понятно!


# Изменим подход к решению запдачи.
# Выделим корневые папки для каждой единицы часов:
watches_list = dom.xpath("//li[contains(@class,'s-item')]")

watches = []
for watch in watches_list:
    watch_info = {}
    name = watch.xpath(".//h3[@class='s-item__title']/text()")
    link = watch.xpath(".//h3[@class='s-item__title']/../@href")
    price = watch.xpath(".//span[@class='s-item__price']//text()")
    info = watch.xpath(".//span[contains(@class,'s-item__hotness')]/span/text()")
# (.) точка перед слэшем ограничивает работу контейнера, так соберём контейнеры,
    # иначе они будуд скомпанованы поимённо, отдельно имя, отдельно линк и т.д.
    watch_info['name'] = name[0]
    watch_info['link'] = link[0]
    watch_info['price'] = price
    watch_info['info'] = info

    watches.append(watch_info)

pprint(watches)