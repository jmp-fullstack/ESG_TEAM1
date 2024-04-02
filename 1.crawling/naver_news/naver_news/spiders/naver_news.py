from naver_news.items import NaverNewsItem
import scrapy
from bs4 import BeautifulSoup
import json
# from evn_keyword_list import evn_keyword

class NaverNewsSpider(scrapy.Spider):
    name = "naver_news"
    
    def start_requests(self):
        # companys = company_list
        # keywords = evn_keyword + social_keyword + gvn_keyword
        # for compny in companys :
        keywords = ['삼성']
        for keyword in keywords:
            for url_num in range(1,11,10):  # 10의 배수로 갯수 지정
                # keyword = f'{compny} {keyword}'
                url_num = str(url_num)
                jq_url = f'https://s.search.naver.com/p/newssearch/search.naver?cluster_rank={url_num}&de=&ds=&eid=&field=0&force_original=&is_dts=0&is_sug_officeid=0&mynews=0&news_office_checked=&\
                    nlu_query=&nqx_theme=%7B%22theme%22%3A%7B%22main%22%3A%7B%22name%22%3A%22site%22%2C%22score%22%3A%220.831540%22%7D%7D%7D&nso=%26nso%3Dso%3Ar%2Cp%3Aall%2Ca%3Aall&nx_and_query=\
                    &nx_search_hlquery=&nx_search_query=&nx_sub_query=&office_category=0&office_section_code=0&office_type=0&pd=0&photo=0&query={keyword}&query_original=&service_area=0&sort=0&spq=0&start={url_num}&where=news_tab_api&nso=so:r,p:all,a:all'
                yield scrapy.Request(url=jq_url, callback=self.url_parse)

    def url_parse(self, response):
        # 자바쿼리형식에서 제이슨 형태로 처리
        jsonp_data = response.text
        json_data_start = jsonp_data.find('{')
        json_data_end = jsonp_data.rfind('}')
        json_data = jsonp_data[json_data_start:json_data_end+1]
        parsed_data = json.loads(json_data)        

        # 각 항목에 대해 링크 추출
        for content in parsed_data['contents']:
            soup = BeautifulSoup(content, 'html.parser')
            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href']
                if 'https://n.news.naver.com' in href:
                    yield scrapy.Request(url=href, callback=self.parse, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'})

    def parse(self, response):
        date = response.css('.media_end_head_info_datestamp_bunch span::text')
        date = date[0].get().split(' ')[0]

        # br태크이므로 article태그안의 내용을 다가져옴
        selectors = response.css('article::text')
        contents = [selector.get().strip() for selector in selectors if selector.get().strip()]

        print(date, contents)