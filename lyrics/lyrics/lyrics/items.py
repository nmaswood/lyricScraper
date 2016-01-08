from  scrapy import Field, Item

class LyricsItem(Item):

    title = Field()
    url = Field()
    genre = Field()

class FullLyricsItem(Item):

    title = Field()
    url_one = Field()
    url_two = Field()
    genre = Field()
    song_name = Field()
    year = Field()
    lyrics = Field()

