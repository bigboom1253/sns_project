import scrapy
import json
import pandas as pd
from SNS import FileMaker
from ..middlewares import TooManyRequestsRetryMiddleware

class InstaSpider(scrapy.Spider):

    name = "insta_follow"

    def __init__(self, INSTA_ID = ''):
        self.INSTA_ID = INSTA_ID

    cookies = {
    #     'ig_did':'72BDF73A-FB8F-4B27-883B-AEA3CF55D654', 
    #     'mid':'XzzUVQALAAE6BTDfbBXndfduewfo',
    #     'csrftoken':'UuAZg4Kvd17km4lmdLzWVlEbNKU316CZ', 
    #     'ds_user_id':'2159978789',
    #     'sessionid':'2159978789%3AsnqWqG04ZZBvGl%3A16', 
    #     'shbid':'8668', 
    #     'shbts':'1598258553.0701873', 
    #     'rur':'ASH', 
    #     'urlgen':'"{\"222.107.238.25\": 4766}:1kA83q:KGSwmHTPsTWw9AjJPF2ui3DGWRI"'
    }

    def start_requests(self):
        InstaSpider.fm = FileMaker.JsonMaker()
        InstaSpider.fm.create_folder()
        InstaSpider.fm.write_file()
        yield scrapy.Request('http://instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables={"id":"{}","first":36}'.format(self.INSTA_ID), callback=self.parse, cookies=InstaSpider.cookies)

    def parse(self, response):
        sources = json.loads(response.text)['data']['user']['edge_follow'] #필요한 데이터

        for source in sources['edges']:
            try:
                yield InstaSpider.fm.add_data({
                    'user_id' : str(self.INSTA_ID),
                    'follow_id' : str(source['node']['id']),
                    'follow_name' : str(source['node']['username']),
                    'follow_fullname' : str(source['node']['full_name'])
                })
            except:
                pass

        end_cursor = sources['page_info']['end_cursor'] #Next Page 확인
        
        if end_cursor != None:
            yield scrapy.Request('http://instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables={"id":"{}","first":36,"after":"{}"}'.format(str(self.INSTA_ID), end_cursor), callback=self.parse, cookies=InstaSpider.cookies)

    def close(self, reason):
        InstaSpider.fm.close_file()