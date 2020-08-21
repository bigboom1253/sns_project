import scrapy
from datetime import datetime
import json
import time

# Insta Cralwer
class InstaSpider(scrapy.Spider):
    
    name = "insta_followee"

    id_list = '12897614243 2262288655'.split()
    id_number = 0
    now_followee = 0
    tmp = 0
    
    short_url = 'https://www.instagram.com/p/'

    start_urls = [
        'http://instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables={"id":"' + id_list[id_number] + '","first":12}'
    ]

    end_cursor = True
    def parse(self, response):
        sources = json.loads(response.text)['data']['user']['edge_follow'] #필요한 데이터

        for source in sources['edges']:
            try:
                yield {
                    'followee_id' : str(source['node']['id']),
                    'followee_name' : str(source['node']['username']),
                    'followee_fullname' : str(source['node']['full_name'])
                }
            except:
                yield {
                    'error' : response.url,
                    'source' : source
                }

        time.sleep(0.1)

        InstaSpider.now_followee += len(sources['edges'])

        InstaSpider.end_cursor = sources['page_info']['end_cursor'] #Next Page 확인
        if int(InstaSpider.now_followee/6000) != InstaSpider.tmp:
            time.sleep(600)
            InstaSpider.tmp = int(InstaSpider.now_followee/6000)
            if InstaSpider.end_cursor != None:
                yield scrapy.Request('http://instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables={"id":"' + InstaSpider.id_list[InstaSpider.id_number] + '","first":12'+',"after":"'+InstaSpider.end_cursor+'"}', callback=self.parse)
            else:
                InstaSpider.id_number += 1
                yield scrapy.Request('http://instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables={"id":"' + InstaSpider.id_list[InstaSpider.id_number] + '","first":12}', callback=self.parse)

            