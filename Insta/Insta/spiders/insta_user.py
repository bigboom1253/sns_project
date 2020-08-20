import scrapy
from datetime import datetime
import json
import pandas as pd

# Insta Cralwer
class InstaSpider(scrapy.Spider):
    
    name = "insta_user"

    id_list = pd.read_json('insta.json')['insta_id'].unique()
    id_number = 0
    
    short_url = 'https://www.instagram.com/p/'

    start_urls = [
        'https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables={"id":"{}","first":12}'.format(int(id_list[id_number]))
    ]

    end_cursor = True
    def parse(self, response):
        sources = json.loads(response.text)['data']['user']['edge_owner_to_timeline_media'] #필요한 데이터

        for source in sources['edges']:
            try:
                yield {
                    'hashtag' : InstaSpider.tag_list[InstaSpider.tag_number],
                    'post_date' : datetime.fromtimestamp(source['node']['taken_at_timestamp']),
                    'crawling_time' : datetime.now(),
                    'insta_id' : str(source['node']['owner']['id']),
                    'content' : source['node']['edge_media_to_caption']['edges'][0]['node']['text'],
                    'image_url' : str(source['node']['display_url']),
                    'like_count' : int(source['node']['edge_liked_by']['count']),
                    'url' : InstaSpider.short_url + str(source['node']['shortcode'])
                }
            except:
                yield {
                    'error' : response.url,
                    'source' : source
                }

        InstaSpider.end_cursor = sources['page_info']['end_cursor'] #Next Page 확인
        if InstaSpider.end_cursor != None:
            yield scrapy.Request('https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables={"id":"' + InstaSpider.id_list[InstaSpider.id_number] + '","first":12'+',"after":"'+InstaSpider.end_cursor+'"}', callback=self.parse)
        else:
            return
            InstaSpider.id_number += 1
            if InstaSpider.id_number < len(InstaSpider.id_list):
                InstaSpider.id_number = 0
                yield scrapy.Request('https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables={"id":"{}","first":12}'.format(int(InstaSpider.id_list[InstaSpider.id_number])))
