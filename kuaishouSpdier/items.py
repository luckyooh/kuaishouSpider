# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

class KuaishouspdierItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class KuaishouItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

# 账户item
class AccountItem(scrapy.Item):
    user_id = scrapy.Field()
    source_channel = scrapy.Field()
    user_name = scrapy.Field()
    remark = scrapy.Field()
    dept_name = scrapy.Field()
    search_word = scrapy.Field()

# 话题item
class TopicItem(scrapy.Item):
    topic_id = scrapy.Field()
    source_channel = scrapy.Field()
    topic_name = scrapy.Field()
    remark = scrapy.Field()
    dept_name = scrapy.Field()
    search_word = scrapy.Field()

# 小视频item
class MiniVideoItem(scrapy.Item):
    publish_time = scrapy.Field()
    mode = scrapy.Field()
    item_id = scrapy.Field()
    title = scrapy.Field()
    type = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    user_id = scrapy.Field()
    source = scrapy.Field()
    old_cont_url = scrapy.Field()
    duration = scrapy.Field()
    video_description = scrapy.Field()
    old_video_url = scrapy.Field()
