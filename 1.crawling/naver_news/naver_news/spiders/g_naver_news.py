import scrapy
from bs4 import BeautifulSoup
import json
import os
import re

class g_naver_news(scrapy.Spider):
    name = "g_naver_news"

    def start_requests(self):
        os.chdir('./naver_news/keywords')
        with open('./G_key_words.txt', encoding='utf-8') as f:
            g_list = [lines.rstrip() for lines in f.readlines()]
        with open('./top200_name_list.csv', encoding='utf-8') as f:
            companys = [lines.rstrip() for lines in f.readlines()]

        for cp in companys :
            for g in g_list :
                keyword = (f'{cp} {g}')
                for url_num in range(1,11,10):  # 10의 배수로 갯수 지정
                    url_num = str(url_num)
                    jq_url = f'https://s.search.naver.com/p/newssearch/search.naver?cluster_rank={url_num}&de=&ds=&eid=&field=0&force_original=&is_dts=0&is_sug_officeid=0&mynews=0&news_office_checked=&\
                        nlu_query=&nqx_theme=%7B%22theme%22%3A%7B%22main%22%3A%7B%22name%22%3A%22site%22%2C%22score%22%3A%220.831540%22%7D%7D%7D&nso=%26nso%3Dso%3Ar%2Cp%3Aall%2Ca%3Aall&nx_and_query=\
                        &nx_search_hlquery=&nx_search_query=&nx_sub_query=&office_category=0&office_section_code=0&office_type=0&pd=0&photo=0&query={keyword}&query_original=&service_area=0&sort=1&spq=0&start={url_num}&where=news_tab_api&nso=so:r,p:all,a:all'
                    yield scrapy.Request(url=jq_url, callback=self.url_parse, meta={'company': cp, 'keyword': g})

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
                    yield scrapy.Request(url=href, callback=self.parse, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}, meta={'company': response.meta['company'], 'keyword': response.meta['keyword']})

    def parse(self, response):
        company = response.meta['company']
        keyword = response.meta['keyword']

        # 제목
        title = response.css('#title_area span::text').get()

        # 날짜
        date = response.css('.media_end_head_info_datestamp_bunch span::text')
        date_str = date[0].get() if date else None  # date가 None이 아닐 때만 date_str에 값을 할당
        if date_str:
            if '. ' in date_str:
                date = date_str.split('. ')[0]
            else:
                date = date_str.split(' ')[0]
        else:
            date = None

        # 본문
        selectors = response.css('article::text')
        contents = [selector.get().strip() for selector in selectors if selector.get().strip()]
        with open('./E_key_words.txt', encoding='utf-8') as file:
            e_kw_list = [lines.rstrip() for lines in file.readlines()]

        # 문장 분리
        content_list = []
        for sentence in contents:
            sentences = re.split(r'(?<=\w)\.', sentence)
            for s in sentences:
                if s != '':
                    content_list.append(s.strip())

        # 키워드 문장만 가져옴
        sentence_list = []
        for content in content_list:
            for e_kw in e_kw_list:
                if e_kw in content:
                    sentence_list.append(content)
                    break

        # 특정 패턴 제거
        patten_1 = '[0-9]{3}-[0-9]{3,4}-[0-9]{4}'
        patten_2 = '\w{4,}\@[a-zA-Z0-9\-]{2,}\.[a-z]{2,}(\.[a-z]{2})?'
        patten_3 = '\[.*?기자]'
        patten_4 = '\[.*?특파원]'
        patten_5 = '\[이데일리.*?]'
        patten_6 = '\(서울=뉴스1\)'
        patten_7 = '\[.*?뉴스]'
        patten_8 = '[\d]'
        patten_9 = '.*(검사부|실장|부장|부사장|상무|팀장|책임연구원|본부장|선임연구원|총무부|부서장|지원센터장|총괄|총무|검사|비서실|재난관리|단장|사업|디렉터|승무원|총무부|수석|부총재|인사부|인사|상무|총무본부|전무|사장|수석연구원|총무|상무|연구원장|부서|사원|감사관|차장|처장|감사관).*'
        patten_last = '[^\w\s]'
        
        for i, sentence in enumerate(sentence_list):
            sentence = re.sub(patten_1, '', sentence)
            sentence = re.sub(patten_2, '', sentence)
            sentence = re.sub(patten_3, '', sentence)
            sentence = re.sub(patten_4, '', sentence)
            sentence = re.sub(patten_5, '', sentence)
            sentence = re.sub(patten_6, '', sentence)
            sentence = re.sub(patten_7, '', sentence)
            sentence = re.sub(patten_8, '', sentence)
            sentence = re.sub(patten_9, '', sentence)
            sentence = re.sub(patten_last, '', sentence)
            sentence_list[i] = sentence
        clean_sent = [sentence for sentence in sentence_list if sentence != '']
        if clean_sent == []:
            pass
        else:
            print(company, keyword, clean_sent , sep='\n')
