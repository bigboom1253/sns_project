import scrapy
from datetime import datetime
import json
import time
import pandas as pd
from SNS import FileMaker, FileSearch

# Insta Cralwer
class InstaSpider(scrapy.Spider):
    
    name = "insta_follower"

    js = FileSearch.JsonSearch()
    fl = js.search('Insta_Data')
    id_list = list(pd.read_json(fl[0])['insta_id'])
    fn = FileMaker.JsonMaker()
    
    id_number = 0
    count = 0
    for s_i in range(65,80):
        try:
            path = 'Insta_Data/A'+chr(s_i)
            fl = js.search(path)
            f_num = max(list(map(lambda i : int(re.search('[0-9]+', i).group()), fl)))
            if f_num != 100:
                id_number = id_list.index(list(pd.read_json(path + '/' + str(f_num) + '.json')['insta_id'])[-1])
                fn.f_si = s_i
                fn.fn += f_num
                break
        except:
            id_number = 0
            break
    
    cookies = {
        'ig_did':'FB9150AA-A5D9-453B-8333-EDC9B2D6011F', 
        'mid':'XtmvJwALAAHl9lyoJfP-qGCRTCQb',
        'csrftoken':'smONbCv8IJ6N5F5tPy1EibH4UxCwnlgt', 
        'ds_user_id':'7779828642',
        'sessionid':'7779828642%3AcVuB3nhkO9AkXT%3A9', 
        'shbid':'12875', 
        'shbts':'1598311471.9713743', 
        'rur':'ASH', 
        'urlgen':'"{\"222.107.238.25\": 4766}:1kALpQ:sHl_0N-nCZb2KzEvOs3D4XpjLRs"'
    }
    
    def start_requests(self):
        url = 'http://instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":"' + str(InstaSpider.id_list[InstaSpider.id_number]) + '","first":36}'
        InstaSpider.fm = FileMaker.JsonMaker()
        InstaSpider.fm.create_folder()
        InstaSpider.fm.write_file()
        yield scrapy.Request(url, callback=self.parse, cookies=InstaSpider.cookies)
        
    def close(self, reason):
        InstaSpider.fm.close_file()

    end_cursor = True
    def parse(self, response):

        try:
            sources = json.loads(response.text)['data']['user']['edge_followed_by'] #필요한 데이터
        except:
            InstaSpider.id_number += 1
            if InstaSpider.id_number < len(InstaSpider.id_list):
                yield scrapy.Request('http://instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":"' + str(InstaSpider.id_list[InstaSpider.id_number]) + '","first":36}', callback=self.parse, cookies=InstaSpider.cookies)
                return

        if len(sources['edges']) > 500:
            InstaSpider.id_number += 1
            if InstaSpider.id_number < int(len(InstaSpider.id_list)/2):
                yield scrapy.Request('http://instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":"' + str(InstaSpider.id_list[InstaSpider.id_number]) + '","first":36}', callback=self.parse, cookies=InstaSpider.cookies)
                return

        for source in sources['edges']:
            try:
                yield InstaSpider.fm.add_data({
                    'user_id' : str(InstaSpider.id_list[InstaSpider.id_number]),
                    'follower_id' : str(source['node']['id']),
                    'follower_username' : str(source['node']['username']),
                    'follower_full_name' : str(source['node']['full_name'])
                })
            except:
                yield InstaSpider.fm.add_data({
                    'error' : response.url,
                    'user_id' : str(InstaSpider.id_list[InstaSpider.id_number]),
                    'source' : source
                })

        InstaSpider.end_cursor = sources['page_info']['end_cursor'] #Next Page 확인
        
        if InstaSpider.end_cursor != None:
            yield scrapy.Request('http://instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":"' + str(InstaSpider.id_list[InstaSpider.id_number]) + '","first":36'+',"after":"'+InstaSpider.end_cursor+'"}', callback=self.parse, cookies=InstaSpider.cookies)
            return
        
        InstaSpider.id_number += 1
        if InstaSpider.id_number < int(len(InstaSpider.id_list)/2):
            yield scrapy.Request('http://instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":"' + str(InstaSpider.id_list[InstaSpider.id_number]) + '","first":36}', callback=self.parse, cookies=InstaSpider.cookies)
