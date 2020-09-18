import scrapy
import json
from SNS import FileMaker, Profiling
import pandas as pd
from ..middlewares import TooManyRequestsRetryMiddleware

# Target User Cralwer
class InstaSpider(scrapy.Spider):

    name = "target_post"
    
    fm = FileMaker.JsonMaker('./Target_Data/')
    
    def __init__(self, TARGET_ID=''):
        self.TARGET_ID = TARGET_ID
        
    def start_requests(self):
        InstaSpider.fm.create_folder(self.TARGET_ID)
        InstaSpider.fm.write_file()
        yield scrapy.Request('https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables={"id":"%s","first":36}' %self.TARGET_ID, callback= self.parse)
    
    
    def parse(self, response):
        sources = json.loads(response.text)['data']['user']['edge_owner_to_timeline_media'] #필요한 데이터

        for source in sources['edges']:
            try:
                yield InstaSpider.fm.add_data({
                    'insta_id' : str(source['node']['owner']['id']),
                    'content' : source['node']['edge_media_to_caption']['edges'][0]['node']['text'] #게시글
                    })
            except:
                pass

        end_cursor = sources['page_info']['end_cursor'] #Next Page 확인
       
        if end_cursor != None:
            yield scrapy.Request('https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables={"id":"%s","first":36,"after":"%s"}'%(self.TARGET_ID, end_cursor), callback=self.parse)

    def close(self, reason):
        InstaSpider.fm.close_file()
        print('Target : {} 크롤링 종료'.format(self.TARGET_ID))
        # 전처리 실행
        Profiling.Text_Pre(self.TARGET_ID)
