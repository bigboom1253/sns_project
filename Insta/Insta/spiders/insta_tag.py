import scrapy
from datetime import datetime
import json

# Insta Cralwer
class InstaSpider(scrapy.Spider):
    
    name = "insta_tag"

    tag_list = '테니스 서핑'.split()
    tag_number = 0
    POST_MAX = 1500 # 한 해시태그당 약 1500개 포스트 수집 (해시태그 10개 기준, 목표 : 1만명, 여유 1.5배)
    now_post = 0
    
    short_url = 'https://www.instagram.com/p/'

    start_urls = [
        'http://instagram.com/graphql/query/?query_hash=7dabc71d3e758b1ec19ffb85639e427b&variables={"tag_name":"' + tag_list[tag_number] + '","first":12}'
    ]

    end_cursor = True
    def parse(self, response):
        sources = json.loads(response.text)['data']['hashtag']['edge_hashtag_to_media'] #필요한 데이터

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

        InstaSpider.now_post += len(sources['edges'])

        InstaSpider.end_cursor = sources['page_info']['end_cursor'] #Next Page 확인
        if InstaSpider.now_post < InstaSpider.POST_MAX:
            if InstaSpider.end_cursor != None:
                yield scrapy.Request('http://instagram.com/graphql/query/?query_hash=7dabc71d3e758b1ec19ffb85639e427b&variables={"tag_name":"' + InstaSpider.tag_list[InstaSpider.tag_number] + '","first":12'+',"after":"'+InstaSpider.end_cursor+'"}', callback=self.parse)
                return
        
        InstaSpider.tag_number += 1
        if InstaSpider.tag_number < len(InstaSpider.tag_list):
            InstaSpider.now_post = 0
            yield scrapy.Request('http://instagram.com/graphql/query/?query_hash=7dabc71d3e758b1ec19ffb85639e427b&variables={"tag_name":"' + InstaSpider.tag_list[InstaSpider.tag_number] + '","first":12}', callback=self.parse)
