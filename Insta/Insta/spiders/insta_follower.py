import scrapy
import json
import pandas as pd
from SNS import FileMaker
from ..middlewares import TooManyRequestsRetryMiddleware

class InstaSpider(scrapy.Spider):
    
    name = "insta_follower"

    def __init__(self, INSTA_ID = ''):
        self.INSTA_ID = INSTA_ID
    
    cookies = {
        # 'ig_did':'FB9150AA-A5D9-453B-8333-EDC9B2D6011F', 
        # 'mid':'XtmvJwALAAHl9lyoJfP-qGCRTCQb',
        # 'csrftoken':'smONbCv8IJ6N5F5tPy1EibH4UxCwnlgt', 
        # 'ds_user_id':'7779828642',
        # 'sessionid':'7779828642%3AcVuB3nhkO9AkXT%3A9', 
        # 'shbid':'12875', 
        # 'shbts':'1598311471.9713743', 
        # 'rur':'ASH', 
        # 'urlgen':'"{\"222.107.238.25\": 4766}:1kALpQ:sHl_0N-nCZb2KzEvOs3D4XpjLRs"'
    }
    
    def start_requests(self):
        url = 'http://instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":"{}","first":36}'.format(self.INSTA_ID)
        InstaSpider.fm = FileMaker.JsonMaker()
        InstaSpider.fm.create_folder()
        InstaSpider.fm.write_file()
        yield scrapy.Request(url, callback=self.parse, cookies=InstaSpider.cookies)

    def parse(self, response):
        sources = json.loads(response.text)['data']['user']['edge_followed_by'] #필요한 데이터

        for source in sources['edges']:
            try:
                yield InstaSpider.fm.add_data({
                    'user_id' : str(self.INSTA_ID),
                    'follower_id' : str(source['node']['id']),
                    'follower_username' : str(source['node']['username']),
                    'follower_full_name' : str(source['node']['full_name'])
                })
            except:
                pass

        end_cursor = sources['page_info']['end_cursor'] #Next Page 확인
        
        if end_cursor != None:
            yield scrapy.Request('http://instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":"{}","first":36,"after":"{}"}'.format(self.INSTA_ID, end_cursor), callback=self.parse, cookies=InstaSpider.cookies)
            return

    def close(self, reason):
        InstaSpider.fm.close_file()
