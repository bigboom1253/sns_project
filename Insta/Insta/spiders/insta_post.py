import scrapy
from datetime import datetime
import json
import time
from SNS import FileMaker
import pandas as pd
# Insta Cralwer

class InstaSpider(scrapy.Spider):
    
    cookies = {
        'ig_did':'4475FF53-AA12-491C-A1A6-9BEA170155BC', 
        'mid':'W21bMAALAAFp96Mh4deV9H0g9FN6',
        'csrftoken':'SNkEseuLyR6MAdufsbNyvSjM3qteRIEg', 
        'ds_user_id':'40382277127',
        'sessionid':'40382277127%3AjbkwRX5hRZjK8C%3A14', 
        'shbid':'8677', 
        'shbts':'1598245161.28281', 
        'rur':'ATN', 
        'urlgen':'"{\"222.107.238.125\": 4766}:1kA79M:od8HEpiAong0o0zizyocvF-NsB4"'
    }

    name = "insta_post"

    id_number = 0
    id_list = list(map(lambda i : int(i), pd.read_json('Insta_Data/insta_users.json')['insta_id'].unique()))
    # POST_MAX = 1500 # 한 해시태그당 약 1500개 포스트 수집 (해시태그 10개 기준, 목표 : 1만명, 여유 1.5배)
    count = 0
    short_url = 'https://www.instagram.com/p/'
    tmp = 0


    def start_requests(self) :
        url =  'https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables={"id":"' + str(InstaSpider.id_list[InstaSpider.id_number]) + '","first":36}'
        InstaSpider.fn = FileMaker.JsonMaker()
        InstaSpider.fn.create_folder()
        InstaSpider.fn.write_file({})
        yield scrapy.Request(url = url, callback= self.parse, cookies= InstaSpider.cookies)
    
    def close(self, reason):
        InstaSpider.fn.close_file()
    
    end_cursor = True
    
    def parse(self, response):
        sources = json.loads(response.text)['data']['user']['edge_owner_to_timeline_media'] #필요한 데이터

        for source in sources['edges']:
            try:
            # try :
            #     temp = source['node']['edge_media_to_tagged_user']['edges']['node']['user']['full_name']    
            # except :    
            #     temp = ''
                
                yield InstaSpider.fn.add_data({
                    'post_date' : datetime.fromtimestamp(source['node']['taken_at_timestamp']).strftime('%Y-%m-%d %H:%M:%S'),
                    'crawling_time' : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'insta_id' : str(source['node']['owner']['id']),
                    'content' : source['node']['edge_media_to_caption']['edges'][0]['node']['text'], #게시글
                    'image_url' : str(source['node']['display_url']),
                    'like_count' : int(source['node']['edge_media_preview_like']['count']),
                    'url' : InstaSpider.short_url + str(source['node']['shortcode']),
                    'post_id' : str(source['node']['shortcode']),
                    # 'tagged' : temp,
                    # hashtag -없음
                    # region_tag -없음
                    # view_count #비디오에만 있음
                    })
            except:
                yield InstaSpider.fn.add_data({
                    'error' : response.url,
                    'source' : source
                })

        # InstaSpider.now_post += len(sources['edges'])

        InstaSpider.end_cursor = sources['page_info']['end_cursor'] #Next Page 확인

        InstaSpider.count += 1 
        # 180 번 정도 부르면 60초 쉬게
        if int(InstaSpider.count/180) != InstaSpider.tmp:
            time.sleep(600)
            InstaSpider.tmp = int(InstaSpider.count/180)
        # if InstaSpider.now_post < InstaSpider.POST_MAX:
       
        if InstaSpider.end_cursor != None:
            #id 리스트로 받기
            yield scrapy.Request('https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables={"id":"' + str(InstaSpider.id_list[InstaSpider.id_number]) + '","first":36,"after":"'+InstaSpider.end_cursor+'"}', callback=self.parse)
            
        else :    
             InstaSpider.id_number += 1
             yield scrapy.Request('https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables={"id":"' + str(InstaSpider.id_list[InstaSpider.id_number]) + '","first":36}', callback=self.parse)

        