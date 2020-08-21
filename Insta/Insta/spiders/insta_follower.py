import scrapy
from datetime import datetime
import json
import time

# Insta Cralwer
class InstaSpider(scrapy.Spider):
    
    name = "insta_follower"

    id_list = '40561677463 40561677463'.split()
    id_number = 0
    now_follower = 0
    follower_max = 6000
    
    
    start_urls = [
        'http://instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":"' + id_list[id_number] + '","first":12}'
    ]

    end_cursor = True
    def parse(self, response):
        sources = json.loads(response.text)['data']['user']['edge_followed_by'] #필요한 데이터

        for source in sources['edges']:
            try:
                yield {

                    'follower_id' : str(source['node']['id']),
                    'follower_username' : str(source['node']['username']),
                    'follower_full_name' : str(source['node']['full_name'])
                    
                }
            except:
                yield {
                    'error' : response.url,
                    'source' : source
                }


        time.sleep(0.1)
        
        InstaSpider.now_follower += len(sources['edges'])

        InstaSpider.end_cursor = sources['page_info']['end_cursor'] #Next Page 확인
        if InstaSpider.now_follower > InstaSpider.follower_max:    # 7천개에서 에러가 남, 6천으로하고 다음으로 넘어가기 전에 10분 텀을 준다
            time.sleep(600)
            InstaSpider.now_follower = 0

        if InstaSpider.end_cursor != None:
            yield scrapy.Request('http://instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":"' + InstaSpider.id_list[InstaSpider.id_number] + '","first":12'+',"after":"'+InstaSpider.end_cursor+'"}', callback=self.parse)
            return
        
        InstaSpider.id_number += 1
        if InstaSpider.id_number < len(InstaSpider.id_list):
            yield scrapy.Request('http://instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":"' + InstaSpider.id_list[InstaSpider.id_number] + '","first":12}', callback=self.parse)
