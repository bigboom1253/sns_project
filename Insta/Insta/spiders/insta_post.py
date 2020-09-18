import scrapy
from datetime import datetime
import json
from SNS import FileMaker
import pandas as pd
from ..middlewares import TooManyRequestsRetryMiddleware

class InstaSpider(scrapy.Spider):

    name = "insta_post"

    def __init__(self, INSTA_ID = ''):
        self.INSTA_ID = INSTA_ID

    def start_requests(self) :
        InstaSpider.fm = FileMaker.JsonMaker()
        InstaSpider.fm.create_folder()
        InstaSpider.fm.write_file()
        yield scrapy.Request('https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables={"id":"{}","first":36}'.format(self.INSTA_ID), callback= self.parse)
    
    def parse(self, response):
        sources = json.loads(response.text)['data']['user']['edge_owner_to_timeline_media'] #필요한 데이터

        for source in sources['edges']:
            try:
                yield InstaSpider.fm.add_data({
                    'post_date' : datetime.fromtimestamp(source['node']['taken_at_timestamp']).strftime('%Y-%m-%d %H:%M:%S'),
                    'insta_id' : str(source['node']['owner']['id']),
                    'content' : source['node']['edge_media_to_caption']['edges'][0]['node']['text'], #게시글
                    'image_url' : str(source['node']['display_url']),
                    'like_count' : int(source['node']['edge_media_preview_like']['count']),
                    'url' : InstaSpider.short_url + str(source['node']['shortcode']),
                    'post_id' : str(source['node']['shortcode']),
                    })
            except:
                pass

        end_cursor = sources['page_info']['end_cursor'] #Next Page 확인
        if end_cursor != None:
            yield scrapy.Request('https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables={"id":"{}","first":36,"after":"{}"}'.format(self.INSTA_ID, end_cursor), callback=self.parse)

    def close(self, reason):
        InstaSpider.fm.close_file()
