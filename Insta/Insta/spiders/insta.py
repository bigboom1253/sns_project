import scrapy
from datetime import datetime
import json

# Insta Cralwer
class InstaSpider(scrapy.Spider):
    
    name = "insta"

    search_word = '홈쇼핑'

    start_urls = [
        'http://instagram.com/graphql/query/?query_hash=7dabc71d3e758b1ec19ffb85639e427b&variables={"tag_name":"' + search_word + '","first":12}'
    ]

    end_cursor=True
    def parse(self, response):
        text = response.css('::text').get()
        yield { 'text' : text }
        return
        sources = json.loads(text)['data']['hashtag']['edge_hashtag_to_media'] #필요한 데이터

        for source in sources['edges']:
            try:
                yield {
                    'date' : datetime.fromtimestamp(source['node']['taken_at_timestamp']),
                    'content' : source['node']['edge_media_to_caption']['edges'][0]['node']['text']
                }
            except:
                pass

        InstaSpider.end_cursor = sources['page_info']['end_cursor'] #Next Page 확인
        if InstaSpider.end_cursor != None:
            URL = 'http://instagram.com/graphql/query/?query_hash=7dabc71d3e758b1ec19ffb85639e427b&variables={"tag_name":"' + self.search_word + '","first":12'+',"after":"'+self.end_cursor+'"}'
            yield scrapy.Request(URL, callback=self.parse)
        else :
            return
