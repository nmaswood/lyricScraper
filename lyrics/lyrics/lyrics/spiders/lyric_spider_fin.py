from scrapy import Spider
from scrapy.selector import Selector
from scrapy import Request


from lyrics.items import LyricsItem
from lyrics.items import FullLyricsItem

class LyricsSpiderFin(Spider):

    name = "lyrics_fin"

    start_urls = [ "http://lyrics.wikia.com/wiki/Draco_And_The_Malfoys:Draco_And_The_Malfoys_(2005)",]

    allowed_domains = ["lyrics.wikia.com"]

    def parse(self, response):

        urls = response.xpath("//div[@id='mw-content-text']//ol//li//a//@href").extract()

        for index, url in enumerate(urls):

            urls[index] = response.urljoin(url)

        for url in urls:

            yield Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):

        lyric_box  = response.xpath("//div[@id='mw-content-text']//div[@class='lyricbox']").extract()

        script_less=  ''.join(lyric_box).split("</script>")

        lyrics = script_less[1].split("<!--")[0].replace("<br>", " ")

        lyric_info =script_less[0].split("adunit_id")[0]
        lyric_info = lyric_info.split("{")[-1].split(",")

        artist = lyric_info[0]
        song = lyric_info[1]

        artist = artist.split(":")[-1].replace("\"", "").strip()
        song_name =  song.split(":")[-1].replace("\"", "").strip()


        print response.url
        print artist
        print song_name

        print "\n\n\n\n\n\n"

        full_lyrics_item = FullLyricsItem()

        full_lyrics_item["url_one"]= "this is a test value"
        full_lyrics_item["url_two"] = response.url
        full_lyrics_item["title"] =  "this is a test value"
        full_lyrics_item["genre"] =  "this is a test value"
        full_lyrics_item["lyrics"] = lyrics
        full_lyrics_item["song_name"] = song_name
        full_lyrics_item["year"] = "this is a test value"

        yield full_lyrics_item
