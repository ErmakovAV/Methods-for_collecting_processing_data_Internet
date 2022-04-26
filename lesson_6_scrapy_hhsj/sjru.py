import scrapy
from scrapy.http import HtmlResponse
from jobs.items import JobsItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=Python']

    def parse(self, response: HtmlResponse):
        # response.status
        next_page = response.xpath('//a[contains(@class,"f-test-button-dalshe")]/@href').get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//div[@class="f-test-search-result-item"]//div/div/a/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)


    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath('//h1[@class = "_2L5ou _1TcZY mO3i1 dAWx1 Zruy6"]//text()').get()
        salary = response.xpath('//span[@class = "-gENC _1TcZY mO3i1 dAWx1"]/text()').get()
        url = response.url
        yield JobsItem(name=name, salary=salary, url=url)