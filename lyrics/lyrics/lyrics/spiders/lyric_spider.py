from scrapy import Spider
from scrapy.selector import Selector
from scrapy import Request


from lyrics.items import LyricsItem

class LyricsSpider(Spider):

    name = "lyrics"

    start_urls = ["http://lyrics.wikia.com/wiki/Category:Genre",
                 "http://lyrics.wikia.com/wiki/Category:Genre?subcatfrom=French+Pop%0AGenre%2FFrench+Pop#mw-subcategories",
                 "http://lyrics.wikia.com/wiki/Category:Genre?subcatfrom=Progressive+Folk%0AGenre%2FProgressive+Folk#mw-subcategories",
                 ]

    allowed_domains = ["lyrics.wikia.com"]

    def parse(self, response):

                data =  response.xpath('//body//div[@id="mw-subcategories"]')

                urls = data.xpath("//td//a/@href").extract()

                for index, url in enumerate(urls):

                    urls[index] = response.urljoin(url)

                for url in urls:

                    yield Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):

        genre_text =  response.xpath("//body//div[@id='mw-pages']//h2//span//text()").extract()

        if type(genre_text) == type(list()):

            genre_text = genre_text[0]

        genre = genre_text.split("Genre/")[-1].strip('"')

        artists = response.xpath('//body//div[@id="mw-pages"]//div[@class="mw-content-ltr"]')
        artists = artists.xpath('//tr//ul//li//a')

        for sel in artists:

            item =  LyricsItem()
            url = sel.xpath('@href').extract()[0]
            url = response.urljoin(url)

            title = sel.xpath('@title').extract()[0]
            item["url"] = url
            item["title"] =  title
            item["genre"] = genre

            yield item

