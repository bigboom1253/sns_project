import scrapy
import json
from SNS import FileMaker, FileSearch, Profiling
import pandas as pd
import re

from ..middlewares import TooManyRequestsRetryMiddleware
import os, sys

# Target User Cralwer
class InstaSpider(scrapy.Spider):

    name = "target_post"
    
    js = FileSearch.JsonSearch()
    fl = js.search('Target_Data')
    fn = FileMaker.JsonMaker('./Target_Data/')
    
    def __init__(self, TARGET_ID=''):
        self.TARGET_ID = TARGET_ID

    def start_requests(self):
        InstaSpider.fn.create_folder(self.TARGET_ID)
        InstaSpider.fn.write_file()
        url =  'https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables={"id":"' + str(self.TARGET_ID) + '","first":36}'
        yield scrapy.Request(url = url, callback= self.parse)
    
    
    def close(self, reason):
        InstaSpider.fn.close_file()
        print('Target : {} 크롤링 종료'.format(self.TARGET_ID))
        # 전처리 실행
        Profiling.Text_Pre(self.TARGET_ID)
    
    end_cursor = True
    def parse(self, response):
        sources = json.loads(response.text)['data']['user']['edge_owner_to_timeline_media'] #필요한 데이터

        for source in sources['edges']:
            try:
                yield InstaSpider.fn.add_data({
                    'insta_id' : str(source['node']['owner']['id']),
                    'content' : source['node']['edge_media_to_caption']['edges'][0]['node']['text'], #게시글
                    'post_id' : str(source['node']['shortcode']),
                    })
            except:
                pass

        InstaSpider.end_cursor = sources['page_info']['end_cursor'] #Next Page 확인
       
        if InstaSpider.end_cursor != None:
            yield scrapy.Request('https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables={"id":"' + str(self.TARGET_ID) + '","first":36,"after":"'+InstaSpider.end_cursor+'"}', callback=self.parse)
