from  scrapy import Field, Item

class LyricsItem(Item):

    title = Field()
    url = Field()
    genre = Field()

class FullLyricsItem(Item):

    url_one = Field()
    url_two = Field()
    song_name = Field()
    artist = Field()
    lyrics = Field()
