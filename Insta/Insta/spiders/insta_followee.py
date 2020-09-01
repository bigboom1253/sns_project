# import scrapy
# from datetime import datetime
# import json
# import time
# import pandas as pd
# from SNS import FileMaker

# # Insta Cralwer
# class InstaSpider(scrapy.Spider):
    
#     name = "insta_followee"

#     id_list = pd.read_json('Insta_Data/insta_id.json')['insta_id']
#     id_number = 0
#     now_followee = 0
#     tmp = 0
#     count = 0

#     cookies = {
#         'ig_did':'72BDF73A-FB8F-4B27-883B-AEA3CF55D654', 
#         'mid':'XzzUVQALAAE6BTDfbBXndfduewfo',
#         'csrftoken':'UuAZg4Kvd17km4lmdLzWVlEbNKU316CZ', 
#         'ds_user_id':'2159978789',
#         'sessionid':'2159978789%3AsnqWqG04ZZBvGl%3A16', 
#         'shbid':'8668', 
#         'shbts':'1598258553.0701873', 
#         'rur':'ASH', 
#         'urlgen':'"{\"222.107.238.25\": 4766}:1kA83q:KGSwmHTPsTWw9AjJPF2ui3DGWRI"'
#     }
    
#     def close(self, reason):
#         InstaSpider.fm.close_file()

#     def start_requests(self):
#         url = 'http://instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables={"id":"' + str(InstaSpider.id_list[InstaSpider.id_number]) + '","first":36}'
#         InstaSpider.fm = FileMaker.JsonMaker()
#         InstaSpider.fm.create_folder()
#         InstaSpider.fm.write_file()
#         yield scrapy.Request(url, callback=self.parse, cookies=InstaSpider.cookies)

#     end_cursor = True
#     def parse(self, response):
#         InstaSpider.count += 1
#         if int(InstaSpider.count/180) != InstaSpider.tmp:
#             time.sleep(600)
#             InstaSpider.tmp = int(InstaSpider.count/180)
        
#         try:
#             sources = json.loads(response.text)['data']['user']['edge_follow'] #필요한 데이터
#         except:
#             InstaSpider.id_number += 1
#             if InstaSpider.id_number < len(InstaSpider.id_list):
#                 yield scrapy.Request('http://instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables={"id":"' + str(InstaSpider.id_list[InstaSpider.id_number]) + '","first":36}', callback=self.parse, cookies=InstaSpider.cookies)
#                 return

#         if len(sources['edges']) > 500:
#             InstaSpider.id_number += 1
#             if InstaSpider.id_number < len(InstaSpider.id_list):
#                 yield scrapy.Request('http://instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables={"id":"' + str(InstaSpider.id_list[InstaSpider.id_number]) + '","first":36}', callback=self.parse, cookies=InstaSpider.cookies)
#                 return

#         for source in sources['edges']:
#             try:
#                 yield InstaSpider.fm.add_data({
#                     'user_id' : str(InstaSpider.id_list[InstaSpider.id_number]),
#                     'followee_id' : str(source['node']['id']),
#                     'followee_name' : str(source['node']['username']),
#                     'followee_fullname' : str(source['node']['full_name'])
#                 })
#             except:
#                 yield InstaSpider.fm.add_data({
#                     'error' : response.url,
#                     'user_id' : str(InstaSpider.id_list[InstaSpider.id_number]),
#                     'source' : source
#                 })

#         time.sleep(0.1)
#         InstaSpider.end_cursor = sources['page_info']['end_cursor'] #Next Page 확인
        
#         if InstaSpider.end_cursor != None:
#             yield scrapy.Request('http://instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables={"id":"' + str(InstaSpider.id_list[InstaSpider.id_number]) + '","first":36'+',"after":"'+InstaSpider.end_cursor+'"}', callback=self.parse, cookies=InstaSpider.cookies)
#         else:
#             InstaSpider.id_number += 1
#             yield scrapy.Request('http://instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables={"id":"' + str(InstaSpider.id_list[InstaSpider.id_number]) + '","first":36}', callback=self.parse, cookies=InstaSpider.cookies)


