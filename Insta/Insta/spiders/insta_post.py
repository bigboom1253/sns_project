import scrapy
from datetime import datetime
import json
import time
# Insta Cralwer

class InstaSpider(scrapy.Spider):
    
    name = "insta_post"

    user_list = ''.split()
    user_number = 0
    POST_MAX = 1500 # 한 해시태그당 약 1500개 포스트 수집 (해시태그 10개 기준, 목표 : 1만명, 여유 1.5배)
    now_post = 0
    
    short_url = 'https://www.instagram.com/p/'

    start_urls = [
      'https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables={"id":"1009824958","first":12}'
    ]

    end_cursor = True
    def parse(self, response):
        sources = json.loads(response.text)['data']['user']['edge_owner_to_timeline_media'] #필요한 데이터

        for source in sources['edges']:
            try:
                yield {
                    'post_date' : datetime.fromtimestamp(source['node']['taken_at_timestamp']),
                    'crawling_time' : datetime.now(),
                    'insta_id' : str(source['node']['owner']['id']),
                    'content' : source['node']['edge_media_to_caption']['edges'][0]['node']['text'], #게시글
                    'image_url' : str(source['node']['display_url']),
                    'like_count' : int(source['node']['edge_media_preview_like']['count']),
                    'url' : InstaSpider.short_url + str(source['node']['shortcode']),
                    'post_id' : str(source['node']['shortcode'])
                   
                    #hashtag -없음
                    #region_tag -없음
                    #tagged -tagged_user는 없음
                    #view_count #비디오에만 있음
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
                #id 리스트로 받기
                yield scrapy.Request('https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables={"id":"1009824958","first":12,"after":"'+InstaSpider.end_cursor+'"}', callback=self.parse)
                return
    

        # InstaSpider.user_number += 1

        # time.sleep(600)
        # if InstaSpider.user_number < len(InstaSpider.user_list):
        #     InstaSpider.now_post = 0
        #     yield scrapy.Request('https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables={"id":"' + InstaSpider.user_list[InstaSpider.user_number] + '","first":12}', callback=self.parse)