from  scrapy import Field, Item

class LyricsItem(Item):

    title = Field()
    url = Field()
    genre = Field()
