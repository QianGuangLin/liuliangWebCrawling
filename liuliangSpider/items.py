# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LiuliangspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

    pkg_sort = scrapy.Field()
    pkg_url = scrapy.Field()
    pkg_title = scrapy.Field()

    # job_pkg_sort = scrapy.Field()
    # job_pkg_url = scrapy.Field()
    # job_pkg_title = scrapy.Field()
    #
    # myVIP_pkg_sort = scrapy.Field()
    # myvip_pkg_url = scrapy.Field()
    # myvip_pkg_title = scrapy.Field()
    #
    # regularUser_pkg_sort = scrapy.Field()
    # regularUser_pkg_url = scrapy.Field()
    # regularUser_pkg_title = scrapy.Field()


    pkg_full_title = scrapy.Field()
    pkg_price = scrapy.Field()
    pkg_flow_size = scrapy.Field()
    pkg_content = scrapy.Field()

    pkg_image_urls = scrapy.Field()
    pkg_images = scrapy.Field()

