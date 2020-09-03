import scrapy
from datetime import datetime
import json
import time
from SNS import FileMaker
from SNS import FileSearch
import pandas as pd
import re
# Insta Cralwer

class InstaSpider(scrapy.Spider):
    
    js = FileSearch.JsonSearch()
    fl = js.search('Insta_Data')
    id_list = list(pd.read_json(fl[0])['insta_id'])
    fn = FileMaker.JsonMaker()
    

    name = "insta_post"
    for s_i in range(65,80):
        try:
            path = 'Insta_Data/A'+chr(s_i)
            fl = js.search(path)
            if len(fl) != 100:
                f_num = max(list(map(lambda i : int(re.search('[0-9]+', i).group()), fl)))
                id_number = id_list.index(list(pd.read_json(path + '/' + str(f_num) + '.json')['insta_id'])[-1])
                fn.f_si = s_i
                fn.fn += len(fl)
                break
        except:
            id_number = 0
            break

    count = 0
    short_url = 'https://www.instagram.com/p/'
    tmp = 0


    def start_requests(self) :
        InstaSpider.fn.create_folder()
        InstaSpider.fn.write_file()
        url =  'https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables={"id":"' + str(InstaSpider.id_list[InstaSpider.id_number]) + '","first":36}'
        yield scrapy.Request(url = url, callback= self.parse)
    
    def close(self, reason):
        InstaSpider.fn.close_file()
    
    end_cursor = True
    
    def parse(self, response):
        InstaSpider.count += 1 
        if int(InstaSpider.count/180) != InstaSpider.tmp:
            time.sleep(650)
            InstaSpider.tmp = int(InstaSpider.count/180)

        try:
            sources = json.loads(response.text)['data']['user']['edge_owner_to_timeline_media'] #필요한 데이터
        except:
            InstaSpider.id_number += 1
            yield scrapy.Request('https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables={"id":"' + str(InstaSpider.id_list[InstaSpider.id_number]) + '","first":36}', callback=self.parse)
            return


        for source in sources['edges']:
            try:
                yield InstaSpider.fn.add_data({
                    'post_date' : datetime.fromtimestamp(source['node']['taken_at_timestamp']).strftime('%Y-%m-%d %H:%M:%S'),
                    'crawling_time' : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'insta_id' : str(source['node']['owner']['id']),
                    'content' : source['node']['edge_media_to_caption']['edges'][0]['node']['text'], #게시글
                    'image_url' : str(source['node']['display_url']),
                    'like_count' : int(source['node']['edge_media_preview_like']['count']),
                    'url' : InstaSpider.short_url + str(source['node']['shortcode']),
                    'post_id' : str(source['node']['shortcode']),
                    })
            except:
                yield InstaSpider.fn.add_data({
                    'error' : response.url,
                    'source' : source
                })

        InstaSpider.end_cursor = sources['page_info']['end_cursor'] #Next Page 확인
       
        if InstaSpider.end_cursor != None:
            #id 리스트로 받기
            yield scrapy.Request('https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables={"id":"' + str(InstaSpider.id_list[InstaSpider.id_number]) + '","first":36,"after":"'+InstaSpider.end_cursor+'"}', callback=self.parse)
        else :
             InstaSpider.id_number += 1
             yield scrapy.Request('https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables={"id":"' + str(InstaSpider.id_list[InstaSpider.id_number]) + '","first":36}', callback=self.parse)
