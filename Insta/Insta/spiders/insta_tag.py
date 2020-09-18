import scrapy
from datetime import datetime
from SNS import FileMaker
import json
from ..middlewares import TooManyRequestsRetryMiddleware

# Insta Cralwer
class InstaSpider(scrapy.Spider):
    
    name = "insta_tag"

    def __init__(self, HASHTAG = ''):
        self.HASHTAG = HASHTAG

    def start_requests(self) :
        InstaSpider.fm = FileMaker.JsonMaker()
        InstaSpider.fm.create_folder()
        InstaSpider.fm.write_file()
        yield scrapy.Request('https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables={"id":"{}","first":36}'.format(self.HASHTAG), callback= self.parse)


    def parse(self, response):
        sources = json.loads(response.text)['data']['hashtag']['edge_hashtag_to_media'] #필요한 데이터

        for source in sources['edges']:
            try:
                yield InstaSpider.fm.add_data({
                    'hashtag' : InstaSpider.tag_list[InstaSpider.tag_number],
                    'post_date' : datetime.fromtimestamp(source['node']['taken_at_timestamp']),
                    'insta_id' : str(source['node']['owner']['id']),
                    'content' : source['node']['edge_media_to_caption']['edges'][0]['node']['text'], #게시글
                    'image_url' : str(source['node']['display_url']),
                    'like_count' : int(source['node']['edge_media_preview_like']['count']),
                    'url' : InstaSpider.short_url + str(source['node']['shortcode']),
                    'post_id' : str(source['node']['shortcode']),
                })
            except:
                pass

        end_cursor = sources['page_info']['end_cursor'] #Next Page 확인
        if end_cursor != None:
            yield scrapy.Request('http://instagram.com/graphql/query/?query_hash=7dabc71d3e758b1ec19ffb85639e427b&variables={"tag_name":"{}","first":36,"after":"{}"}'.format(self.HASHTAG, end_cursor), callback=self.parse)
            return

    def close(self, reason):
        InstaSpider.fm.close_file()
