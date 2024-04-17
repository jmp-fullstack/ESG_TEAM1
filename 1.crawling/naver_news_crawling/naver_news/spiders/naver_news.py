import scrapy
from bs4 import BeautifulSoup
import json
import re
from naver_news.items import NaverNewsItem


with open('./keywords/top200_name_list.csv', encoding='utf-8') as company_f:
    companys = [lines.rstrip() for lines in company_f.readlines()]

class naver_news(scrapy.Spider):
    name = "naver_news"

    def start_requests(self):
        # sort=0 최신순, sort=1 관련도순
        s_year, s_month, s_day = '2024', '01', '01' # 시작 날짜지정
        e_year, e_month, e_day = '2024', '04', '16' # 끝 날짜지정
        for company in companys:
                url = (
                    'https://s.search.naver.com/p/newssearch/search.naver?'
                    f'cluster_rank=1&'
                    f'de={e_year}.{e_month}.{e_day}&'
                    f'ds={s_year}.{s_month}.{s_day}&'
                    'is_dts=0&'
                    'nqx_theme=%7B%22theme%22%3A%7B%22main%22%3A%7B%22name%22%3A%22stock%22%7D%7D%7D&'
                    f'nso=so:r,p:from{s_year}{s_month}{s_day}to{e_year}{e_month}{e_day},a:all&'
                    f'nx_and_query={company}&'
                    f'nx_search_query={company}&'
                    f'query=+{company}&'
                    'sort=0&'
                    f'start=1&'
                    'where=news_tab_api&'
                    'nso=so:r,p:all,a:all'
                )
                yield scrapy.Request(url=url, callback=self.parse_url, meta={'company': company})

    def parse_url(self, response):
        # JSONP 응답에서 JSON 형식 데이터 추출
        jsonp_data = response.text
        json_data_start = jsonp_data.find('{')
        json_data_end = jsonp_data.rfind('}')
        json_data = jsonp_data[json_data_start:json_data_end+1]
        parsed_data = json.loads(json_data)

        # 링크 추출 및 요청
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
                            'company': response.meta.get('company'),})

        # 다음 URL 처리
        next_url = parsed_data.get('nextUrl')
        if next_url:
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
                },
                meta={
                    'company': response.meta.get('company'),
                    'keyword': response.meta.get('keyword')
                }
            )

    def parse_news(self, response):
        item = NaverNewsItem()

        # 기업명 
        company = response.meta['company']
        item['company'] = company

        # 제목
        item['title'] = response.css('title::text').get()

        # 날짜
        date = response.css('.media_end_head_info_datestamp_bunch span::text')
        date_str = date[0].get() if date else None
        if date_str:
            if '. ' in date_str:
                date = date_str.split('. ')[0]
            else:
                date = date_str.split(' ')[0]
        else:
            date = None
        item['date'] = date


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
        patten_1 = '[0-9]{3}-[0-9]{3,4}-[0-9]{4}'
        patten_2 = '\w{4,}\@[a-zA-Z0-9\-]{2,}\.[a-z]{2,}(\.[a-z]{2})?'
        patten_3 = '\[.*?기자]'
        patten_4 = '\[.*?특파원]'
        patten_5 = '\[이데일리.*?]'
        patten_6 = '\(서울=뉴스1\)'
        patten_7 = '\[.*?뉴스]'
        patten_8 = '.*(검사부|실장|부장|부사장|상무|팀장|책임연구원|본부장|선임연구원|총무부|부서장|지원센터장|총괄|총무|검사|비서실|재난관리|단장|사업|디렉터|승무원|총무부|수석|부총재|인사부|인사|상무|총무본부|전무|사장|수석연구원|총무|상무|연구원장|부서|사원|감사관|차장|처장|감사관).*'
        patten_9 = '[^\w\s^.]'
        
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
            item['url'] = response.url
            #크롤링 확인용
            print(date, company, len(clean_sent), response.url)
            item['content'] = '&&'.join(clean_sent)
            yield item