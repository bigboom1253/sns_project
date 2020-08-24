import scrapy
from datetime import datetime
import json
import time
import pandas as pd
from SNS import FileMaker

# Insta Cralwer
class InstaSpider(scrapy.Spider):
    
    name = "insta_follower"

    id_list = list(map(lambda i : int(i), pd.read_json('Insta_Data/insta_users.json')['insta_id'].unique()))
    
    id_number = 0
    count = 0
    follower_max = 180
    
    cookies = {
        'ig_did':'06548C02-0DCB-4692-8EA3-ADCD9804555D', 
        'mid':'X0NITwALAAGpos1dYjjZi7DxOhQF',
        'csrftoken':'X1W6anVSNI3A57oMTOm6Ln45h8FIWRkL', 
        'ds_user_id':'27175886134',
        'sessionid':'27175886134%3Adggd9B7zspeWhY%3A23', 
        'shbid':'2488', 
        'shbts':'1598244963.155258', 
        'rur':'ASH', 
        'urlgen':'"{\"222.107.238.25\": 4766}:1kA4XS:_QfDw8Ax5-ycHtUvNIxu89VZ4qU"'
    }
    
    def start_requests(self):
        url = 'http://instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":"' + str(InstaSpider.id_list[InstaSpider.id_number]) + '","first":36}'
        InstaSpider.fm = FileMaker.JsonMaker()
        InstaSpider.fm.create_folder()
        InstaSpider.fm.write_file({})
        yield scrapy.Request(url, callback=self.parse, cookies=InstaSpider.cookies)
        
    def close(self, reason):
        InstaSpider.fm.close_file()

    end_cursor = True
    def parse(self, response):
        sources = json.loads(response.text)['data']['user']['edge_followed_by'] #필요한 데이터

        for source in sources['edges']:
            try:
                yield InstaSpider.fm.add_data({

                    'follower_id' : str(source['node']['id']),
                    'follower_username' : str(source['node']['username']),
                    'follower_full_name' : str(source['node']['full_name'])
                    
                })
            except:
                yield InstaSpider.fm.add_data({
                    'error' : response.url,
                    'source' : source
                })


        time.sleep(0.1)
        
        # InstaSpider.now_follower += len(sources['edges'])

        InstaSpider.end_cursor = sources['page_info']['end_cursor'] #Next Page 확인
        
        InstaSpider.count += 1
        if InstaSpider.count >= InstaSpider.follower_max:    
            time.sleep(600)
            InstaSpider.count = 0

        if InstaSpider.end_cursor != None:
            yield scrapy.Request('http://instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":"' + str(InstaSpider.id_list[InstaSpider.id_number]) + '","first":36'+',"after":"'+InstaSpider.end_cursor+'"}', callback=self.parse, cookies=InstaSpider.cookies)
            return
        
        InstaSpider.id_number += 1
        if InstaSpider.id_number < len(InstaSpider.id_list):
            yield scrapy.Request('http://instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":"' + str(InstaSpider.id_list[InstaSpider.id_number]) + '","first":36}', callback=self.parse, cookies=InstaSpider.cookies)
