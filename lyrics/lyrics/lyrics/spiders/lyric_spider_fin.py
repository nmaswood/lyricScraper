from scrapy import Spider
from scrapy.selector import Selector
from scrapy import Request
from scrapy.conf import settings

from lyrics.items import LyricsItem
from lyrics.items import FullLyricsItem
import pymongo

class LyricsSpiderFin(Spider):


    name = "lyrics_fin"

    connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
            )
    db = connection[settings['MONGODB_DB']]
    connection =  db["lyrics_data"]

    data = connection.find()


    allowed_domains = ["lyrics.wikia.com"]

    start_urls = list()

    for d in data:

        start_urls.append(d['url'])


    def parse(self, response):

        base_url = response.url

        urls = response.xpath("//div[@id='mw-content-text']//ol//li//a//@href").extract()

        for index, url in enumerate(urls):

            urls[index] = response.urljoin(url)

        for url in urls:

            yield Request(url, callback=self.parse_dir_contents, meta =  {
                "base_url" : base_url
                })

    def parse_dir_contents(self, response):

        lyric_box  = response.xpath("//div[@id='mw-content-text']//div[@class='lyricbox']").extract()

        script_less=  ''.join(lyric_box).split("</script>")

        
        lyrics = script_less[1].split("<!--")[0].replace("<br>", " ")
        lyric_info =script_less[0].split("adunit_id")[0]
        lyric_info = lyric_info.split("{")[-1].split(",")

        #try:

        print lyric_info[0]

        print "\n\n\n"
        artist = lyric_info[0]
        song = lyric_info[1]
        artist = artist.split(":")[-1].replace("\"", "").strip()
        song_name =  song.split(":")[-1].replace("\"", "").strip()
        #except:
        #   artist = ""
        #    song_name = ""

        full_lyrics_item = FullLyricsItem()

        full_lyrics_item["url_one"]=  response.meta["base_url"]
        full_lyrics_item["url_two"] = response.url
        full_lyrics_item["lyrics"] = lyrics
        full_lyrics_item["song_name"] = song_name
        full_lyrics_item["artist"] = artist

        yield full_lyrics_item
