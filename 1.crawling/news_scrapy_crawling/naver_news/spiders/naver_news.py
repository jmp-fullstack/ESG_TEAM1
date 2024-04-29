import scrapy
from bs4 import BeautifulSoup
import json
import re
from naver_news.items import NaverNewsItem
import datetime
with open('./keywords/kosdaq기업목록.csv', encoding='utf-8') as company_f:
    companys = [lines.rstrip() for lines in company_f.readlines()]
current_datetime = datetime.datetime.now()


class naver_news(scrapy.Spider):
    name = "naver_news"

    def start_requests(self):
        # for year in range(2019,2021):
            # for month in range(1,12):
                # if month in [4, 6, 9, 11]:
                #     e_day = '30'
                # elif month == 2:
                #     e_day = '29' if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else '28'
                # else:
                #     e_day = '31'

        for company in companys:
            url = (
                'https://s.search.naver.com/p/newssearch/search.naver?'
                f'cluster_rank=1&'
                f'de={current_datetime.year}.{current_datetime.month}.{current_datetime.day}&'
                f'ds={current_datetime.year}.{current_datetime.month}.01&'
                'is_dts=0&'
                'nqx_theme=%7B%22theme%22%3A%7B%22main%22%3A%7B%22name%22%3A%22stock%22%7D%7D%7D&'
                f'nso=so:r,p:from{current_datetime.year}{current_datetime.month:02d}01to{current_datetime.year}{current_datetime.month:02d}{current_datetime.day},a:all&'
                f'nx_and_query={company}&'
                f'nx_search_query={company}&'
                f'query=+{company}&'
                'sort=0&'
                f'start=1&'
                'where=news_tab_api&'
                'nso=so:r,p:all,a:all'
            )
            yield scrapy.Request(url=url, callback=self.parse_url, meta={'company': company, 'page_count': 1})

    def parse_url(self, response):
        if response.meta['page_count'] > 2:
            return  # 페이지 카운터가 2를 초과하면 추가 요청을 중단

        jsonp_data = response.text
        json_data_start = jsonp_data.find('{')
        json_data_end = jsonp_data.rfind('}')
        json_data = jsonp_data[json_data_start:json_data_end+1]
        parsed_data = json.loads(json_data)

        for content in parsed_data['contents']:
            soup = BeautifulSoup(content, 'html.parser')
            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href']
                if 'https://n.news.naver.com' in href:
                    yield scrapy.Request(
                        url=href,
                        callback=self.parse_news,
                        headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
                        },
                        meta={
                            'company': response.meta.get('company')
                        })

        next_url = parsed_data.get('nextUrl')
        if next_url and response.meta['page_count'] < 2:
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
                },
                meta={
                    'company': response.meta['company'],
                    'page_count': response.meta['page_count'] + 1  # 페이지 카운터 증가
                })
    def parse_news(self, response):
        item = NaverNewsItem()

        # 기업명 
        company = response.meta['company']

        # 날짜
        date = response.css('.media_end_head_info_datestamp_bunch span::text')
        date_str = date[0].get() if date else None
        if date_str:
            if '. ' in date_str:
                date = date_str.split('. ')[0]
                date = date.split('.')[0]
            else:
                date = date_str.split(' ')[0]
                date = date.split('.')[0]
        else:
            date = None

        # 본문 로직
        selectors = response.css('article::text')
        contents = [selector.get().strip() for selector in selectors if selector.get().strip()]

        # 문장 분리
        content_list = []
        for sentence in contents:
            sentences = re.split(r'(?<=\w)\.', sentence)
            for s in sentences:
                if s != '':
                    content_list.append(s.strip())

        # 특정 패턴 제거
        patten_1 = r'[0-9]{3}-[0-9]{3,4}-[0-9]{4}'
        patten_2 = r'\w{4,}\@[a-zA-Z0-9\-]{2,}\.[a-z]{2,}(\.[a-z]{2})?'
        patten_3 = r'\[.*?기자]'
        patten_4 = r'\[.*?특파원]'
        patten_5 = r'\[이데일리.*?]'
        patten_6 = r'\(서울=뉴스1\)'
        patten_7 = r'\[.*?뉴스]'
        patten_8 = r'.*(검사부|실장|부장|부사장|상무|팀장|책임연구원|본부장|선임연구원|총무부|부서장|지원센터장|총괄|총무|검사|비서실|재난관리|단장|사업|디렉터|승무원|총무부|수석|부총재|인사부|인사|상무|총무본부|전무|사장|수석연구원|총무|상무|연구원장|부서|사원|감사관|차장|처장|감사관).*'
        patten_9 = r'[^\w\s^.]'
        
        for i, sentence in enumerate(content_list):
            sentence = re.sub(patten_1, '', sentence)
            sentence = re.sub(patten_2, '', sentence)
            sentence = re.sub(patten_3, '', sentence)
            sentence = re.sub(patten_4, '', sentence)
            sentence = re.sub(patten_5, '', sentence)
            sentence = re.sub(patten_6, '', sentence)
            sentence = re.sub(patten_7, '', sentence)
            sentence = re.sub(patten_8, '', sentence)
            sentence = re.sub(patten_9, '', sentence)
            content_list[i] = sentence
        clean_sent = [sentence for sentence in content_list if sentence != '']

        if clean_sent == []:
            pass
        else:
            #크롤링 확인용
            print(date, company, len(clean_sent), response.url)

            item['company'] = company
            item['date'] = date
            item['title'] = response.css('title::text').get()
            item['content'] = '&&'.join(clean_sent)
            item['url'] = response.url
            yield item