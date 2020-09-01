# import scrapy
# from datetime import datetime
# import json
# import time
# import pandas as pd
# from SNS import FileMaker

# # Insta Cralwer
# class InstaSpider(scrapy.Spider):
    
#     name = "insta_follower"

#     id_list = pd.read_json('Insta_Data/insta_id.json')['insta_id']
    
#     id_number = 0
#     count = 0
#     follower_max = 180
    
#     cookies = {
#         'ig_did':'FB9150AA-A5D9-453B-8333-EDC9B2D6011F', 
#         'mid':'XtmvJwALAAHl9lyoJfP-qGCRTCQb',
#         'csrftoken':'smONbCv8IJ6N5F5tPy1EibH4UxCwnlgt', 
#         'ds_user_id':'7779828642',
#         'sessionid':'7779828642%3AcVuB3nhkO9AkXT%3A9', 
#         'shbid':'12875', 
#         'shbts':'1598311471.9713743', 
#         'rur':'ASH', 
#         'urlgen':'"{\"222.107.238.25\": 4766}:1kALpQ:sHl_0N-nCZb2KzEvOs3D4XpjLRs"'
#     }
    
#     def start_requests(self):
#         url = 'http://instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":"' + str(InstaSpider.id_list[InstaSpider.id_number]) + '","first":36}'
#         InstaSpider.fm = FileMaker.JsonMaker()
#         InstaSpider.fm.create_folder()
#         InstaSpider.fm.write_file()
#         yield scrapy.Request(url, callback=self.parse, cookies=InstaSpider.cookies)
        
#     def close(self, reason):
#         InstaSpider.fm.close_file()

#     end_cursor = True
#     def parse(self, response):
#         InstaSpider.count += 1
#         if InstaSpider.count >= InstaSpider.follower_max:
#             time.sleep(600)
#             InstaSpider.count = 0

#         try:
#             sources = json.loads(response.text)['data']['user']['edge_followed_by'] #필요한 데이터
#         except:
#             InstaSpider.id_number += 1
#             if InstaSpider.id_number < len(InstaSpider.id_list):
#                 yield scrapy.Request('http://instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":"' + str(InstaSpider.id_list[InstaSpider.id_number]) + '","first":36}', callback=self.parse, cookies=InstaSpider.cookies)
#                 return

#         if len(sources['edges']) > 500:
#             InstaSpider.id_number += 1
#             if InstaSpider.id_number < int(len(InstaSpider.id_list)/2):
#                 yield scrapy.Request('http://instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":"' + str(InstaSpider.id_list[InstaSpider.id_number]) + '","first":36}', callback=self.parse, cookies=InstaSpider.cookies)
#                 return

#         for source in sources['edges']:
#             try:
#                 yield InstaSpider.fm.add_data({
#                     'user_id' : str(InstaSpider.id_list[InstaSpider.id_number]),
#                     'follower_id' : str(source['node']['id']),
#                     'follower_username' : str(source['node']['username']),
#                     'follower_full_name' : str(source['node']['full_name'])
#                 })
#             except:
#                 yield InstaSpider.fm.add_data({
#                     'error' : response.url,
#                     'user_id' : str(InstaSpider.id_list[InstaSpider.id_number]),
#                     'source' : source
#                 })


#         time.sleep(0.1)
        
#         # InstaSpider.now_follower += len(sources['edges'])

#         InstaSpider.end_cursor = sources['page_info']['end_cursor'] #Next Page 확인
        
#         if InstaSpider.end_cursor != None:
#             yield scrapy.Request('http://instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":"' + str(InstaSpider.id_list[InstaSpider.id_number]) + '","first":36'+',"after":"'+InstaSpider.end_cursor+'"}', callback=self.parse, cookies=InstaSpider.cookies)
#             return
        
#         InstaSpider.id_number += 1
#         if InstaSpider.id_number < int(len(InstaSpider.id_list)/2):
#             yield scrapy.Request('http://instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":"' + str(InstaSpider.id_list[InstaSpider.id_number]) + '","first":36}', callback=self.parse, cookies=InstaSpider.cookies)
