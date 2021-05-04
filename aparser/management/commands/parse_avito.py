import datetime
from collections import namedtuple
import requests
import bs4
from django.core.management.base import BaseCommand

from aparser.models import Product

InnerBlock = namedtuple('Block', 'title, price, url')


class Block(InnerBlock):
    def __str__(self):
        return f"{self.title} : {self.price} : {self.url}"


s = {
}
proxies = {
    'http': 'http://51.158.123.35:9999'
}


class AvitoParser:
    def __init__(self):
        self.url = s['url']
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/90.0.4430.85 Safari/537.36 '
        }
        self.session.proxies.update(proxies)

    def get_page(self, page: int = None):
        params = {
        }
        if page and page > 1:
            params['p'] = page

        r = self.session.get(self.url, params=params)
        return r.text

    # TO-DO исправить дату
    @staticmethod
    # def get_date(item: str):
    #     params = item.strip().split(' ')
    #     month_map = {
    #         'января': 1,
    #         'февраля': 2,
    #         'марта': 3,
    #         'апреля': 4,
    #         'мая': 5,
    #         'июня': 6,
    #         'июля': 7,
    #         'августа': 8,
    #         'сентября': 9,
    #         'октября': 10,
    #         'ноября': 11,
    #         'декабря': 12,
    #     }
    #     if len(params) == 3:
    #         if params[1] == 'дня':
    #             delta = int(params[0])
    #             date = datetime.datetime.today() - datetime.timedelta(days=delta)
    #         elif params[1] == 'секунд':
    #             if params[0] == 'Несколько':
    #                 delta = 1
    #             else:
    #                 delta = int(params[0])
    #             date = datetime.datetime.today() - datetime.timedelta(seconds=delta)
    #
    #         elif params[1] == 'минуты':
    #             delta = int(params[0])
    #             date = datetime.datetime.today() - datetime.timedelta(minutes=delta)
    #
    #         elif params[1] == 'минут':
    #             delta = int(params[0])
    #             date = datetime.datetime.today() - datetime.timedelta(minutes=delta)
    #
    #         elif params[1] == 'минуту':
    #             delta = int(params[0])
    #             date = datetime.datetime.today() - datetime.timedelta(minutes=delta)
    #
    #         elif params[1] == 'день':
    #             delta = int(params[0])
    #             date = datetime.datetime.today() - datetime.timedelta(days=delta)
    #
    #         elif params[1] == 'дней':
    #             delta = int(params[0])
    #             date = datetime.datetime.today() - datetime.timedelta(days=delta)
    #
    #         elif params[1] == 'часов':
    #             delta = int(params[0])
    #             date = datetime.datetime.today() - datetime.timedelta(hours=delta)
    #
    #         elif params[1] == 'часа':
    #             delta = int(params[0])
    #             date = datetime.datetime.today() - datetime.timedelta(hours=delta)
    #         elif params[1] == 'час':
    #             delta = int(params[0])
    #             date = datetime.datetime.today() - datetime.timedelta(hours=delta)
    #
    #         elif params[1] == 'неделю':
    #             delta = int(params[0])
    #             date = datetime.datetime.today() - datetime.timedelta(weeks=delta)
    #         elif params[1] == 'недели':
    #             delta = int(params[0])
    #             date = datetime.datetime.today() - datetime.timedelta(weeks=delta)
    #         elif month_map.get(params[1]):
    #             d_time = params[2].split(':')
    #             hour = int(d_time[0])
    #             minute = int(d_time[1])
    #             day = int(params[0])
    #             month_hru = params[1]
    #
    #             month = month_map.get(month_hru)
    #             today = datetime.datetime.today()
    #             date = datetime.datetime(month=month, day=day, year=today.year, hour=hour, minute=minute)
    #         else:
    #             print(params)
    #             date = None
    #         return date.strftime("%Y-%m-%d %H:%M:%S")
    def parse_block(item):
        url_block = item.find('div', class_='iva-item-titleStep-2bjuh').find('a').get('href')
        url_block = 'https://www.avito.ru' + url_block

        title = item.find('div', class_='iva-item-titleStep-2bjuh').find('a').find('h3').text

        price = item.find('div', class_='iva-item-priceStep-2qRpg').find('span', class_='price-text-1HrJ_').text
        # date = None
        # try:
        #     date_block = item.find('div', class_='iva-item-dateInfoStep-2xJEa').find('div',
        #                                                                              class_='date-text-2jSvU').text
        # except:
        #     date_block = None
        # if date_block:
        #     try:
        #         date = self.get_date(item=date_block)
        #     except:
        #         date = None
        try:
            p = Product.objects.get(url=url_block)  # не создает дублей
            p.title = title
            p.price = price
            p.save()
        except Product.DoesNotExist:
            p = Product(
                url=url_block,
                title=title,
                price=price,
            ).save()
        print(f'product {p}')

        return Block(
            url=url_block,
            title=title,
            price=price,
        )

    def get_pagination(self):
        text = self.get_page()
        soup = bs4.BeautifulSoup(text, 'lxml')

        pag = soup.find_all('span', class_='pagination-item-1WyVp')
        print(pag)
        last_page = pag[-2].text
        return int(last_page)

    def get_blocks(self, page: int = None):
        text = self.get_page(page=page)
        soup = bs4.BeautifulSoup(text, 'lxml')
        container = soup.find_all('div', class_='iva-item-root-G3n7v')
        i = 0
        for item in container:
            block = self.parse_block(item=item)
            print(block)
            i = i + 1
        print('Всего: ', i)

    def parse_all(self):
        last = self.get_pagination()
        if last == 'Доступ с Вашего IP временно ограничен':
            print('Доступ с Вашего IP временно ограничен')
        else:
            if last is None:
                last = 0
            print('Всего страниц:', last)
            for i in range(1, last + 1):
                self.get_blocks(page=i)


class Command(BaseCommand):
    help = 'Парсинг авито'

    def add_arguments(self, parser):
        parser.add_argument('url_parse')

    def handle(self, *args, **options):
        s['url'] = options['url_parse']
        p = AvitoParser()
        p.parse_all()
