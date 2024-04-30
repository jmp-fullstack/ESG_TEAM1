<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=200&section=header&text=KOSDAQ+ESG+평가+대시보드&fontSize=35&animation=fadeIn" />
<div align=center>
<img src="/image.png/메인페이지.JPG" width="800" height="580">
</div>
<div>
<h2><h2>
</div>
<div align=center>
<h3>📚 Teck Stacks<h3>
</div>
<br>
<div align="center">
	<img src="https://img.shields.io/badge/sklearn-003366?style=flat&logo=sklearnB&logoColor=white" />
  <img src="https://img.shields.io/badge/Pytorch-EE4C2C?style=flat&logo=Pytorch&logoColor=white" />
</div>
<div align="center">
	<img src="https://img.shields.io/badge/MariaDB-003545?style=flat&logo=MariaDB&logoColor=white" />
  <img src="https://img.shields.io/badge/AWS-232F3E?style=flat&logo=AmazonAWS&logoColor=white" />
  <img src="https://img.shields.io/badge/Google Colab-F9AB00?style=flat&logo=Google Colab&logoColor=white" />
</div>
<br>
<div align="center">
  <img src="https://img.shields.io/badge/Tableau-E97627?style=flat&logo=Tableau&logoColor=white" />
</div>
<div align="center">
  <img src="https://img.shields.io/badge/git-F05032?style=flat&logo=git&logoColor=white" />
  <img src="https://img.shields.io/badge/Slack-4A154B?style=flat&logo=Slack&logoColor=white" />
  <img src="https://img.shields.io/badge/Notion-000000?style=flat&logo=Notion&logoColor=white" />
</div>

<div align=center>
<h2><h2>
</div>


`1. 크롤링`

**Kosdaq_jobplanet_crawler.ipynb**    

👉🏻 [잡플래닛](https://www.jobplanet.co.kr/job)    

S,G에 특화된 잡플래닛 리뷰텍스트와 수치 데이터 크롤링   

수치 데이터(11개 항목)    

| 복지평점 |복지개수 |리뷰평점 |복지 및 급여|워라밸|사내문화|승진기회 및 가능성|경영진 점수|기업추천율|ceo지지율|성장가능성|   
|---|---|---|---|---|---|---|---|---|---|---|
| 5점 만점 |5점 만점 |5점 만점 |5점 만점|5점 만점|5점 만점|5점 만점|5점 만점|100% 기준|100% 기준|100% 기준|   

텍스트 데이터(2개 항목)   

| 장점 리뷰| 단점 리뷰 |   
|-----------|-----------|  


**Naver_news_crawling.ipynb**    

👉🏻 [네이버 뉴스](https://news.naver.com)   

| kobert train data |kobert test data |  
|-----------|-----------|   
| KOSPI 200 기업명 + 키워드 년도 별 기사 모음 (100,987 개) | 1718개 KOSDAQ 기업별 + 키워드 + 19\~24년 + 1\~12 월 기사모음 (594,200 개) |    


**Patent_report_crawling.ipynb** 

👉🏻 [KIPRIS](https://www.kipris.or.kr)

KIPRIS 특허사이트에 특허정보 검색   

| 1718개의 코스닥 기업의 특허 내용, 출원일자, 등록일자, 크롤링 (16414개) |    
|-----------|



**Green_company_crawl.ipynb**  

👉🏻 [ECO SQUARE](https://ecosq.or.kr)          

- 환경기술산업 원스톱 서비스(ECO SQUARE)의 녹색제품 인증기업 수집     
- 녹색 제품 종류 3가지를 모두 통합 후 기업 별, 연도 별 가산점 책정   

| 환경표지 | GR(재활용) | 저탄소인증 |   
|-----------|-----------|------------|    


- 크롤링 대상 : 4512개의 녹색제품 -> 코스닥에 속한 56개의 회사를 선별 -> 해당 코스닥 기업에 E 가산점 부여      

| 회사명 | 인증연도 | 제품명 |   
|-----------|-----------|------------|    


**Recall_company_crawl.ipynb**  

👉🏻 [국가기술 표준원(KATS)](https://www.kats.go.kr/main.do)          

- 국가기술 표준원(KATS)의 유해기업 수집   

- 자발적리콜, 명령에 따른 리콜, 권고에 따른 리콜로 분류되어 있어 리콜 종류에 따른 가산점 점수 책정   

- 현재 3668개의 리콜 항목의 회사명, 연도, 리콜종류, 제품명 크롤링   

- 이중 코스닥에 속한 18개의 회사를 선별   

- 리콜 여부에 따라 전체 코스닥 기업의 S 가산점 부여   

---  
---

`2. 전처리`

**sustainable_management_report_crawling.ipynb**

《K-ESG 가이드라인 v1.0》의 진단항목명을 통해 추출한 키워드 → SEED  WORD  로 사용  

| E keyword | S keyword | G keyword |
|-----------|-----------|------------|
|    36개   |    50개   |    56개    |

**esg_keyword_extraction.ipynb**   

👉🏻 [지속가능 경영 보고서](https://esg.krx.co.kr)  

SEED WORD 기반으로 《지속가능경영보고서》에서 키워드 추출 → 뉴스 텍스트를 E, S, G 항목으로 분류할 때 사용  
코스피200에 속한 회사 중 110개의 회사의 지속가능경영보고서(pdf 366개)에서 추출된 213,973개의 문장에서 키워드 추출  

| E keyword | S keyword | G keyword |
|-----------|-----------|------------|
|    261개   |    213개   |    240개    |

**bert_train_preprocessing.ipynb**
	
 -  100,987개의 뉴스 기사 문장화 954,452개의 문장, train을 위한 전처리 및 seedword기반 라벨링 후 489,528개의 문장 학습데이터로 이용  

**bert_test_preprocessing.ipynb**
	
 - 594,200개의 데이터 전처리 및 문장화 4,571,733개의 데이터 기업별,년도별 bert_test_input을 위해 자료구조 변환  

**Patent_report_preprocessing.ipynb**  

- 분할 기준 : - (바)    
- 제거항목
1. 기업 별 특허 출원번호 제거
2. 괄호([], (), {}, <>) 및 괄호 안 문자 제거
3. -'...외', '...총' 제거


---  
---

`3. 데이터베이스 구축`   

👉🏻 [ERD CLOUD](https://www.erdcloud.com/d/53ceCuGvDutkGREKx)       
👉🏻 [PIGMA]( https://www.figma.com/file/DhxOgXePlMSGTrwthDzg8D/ESG-Tableau-Dashboard?type=design&node-id=0%3A1&mode=design&t=YZp0d8WbFG6lifL6-1)  

<img src="/image.png/ERD.PNG" width="800" height="500">

**Tableau Architecture기반으로 ERD설계 및 데이터베이스 구축**  

---  
---

`4. Kobert 모델링`

**Fine-Tuning**

- ESG fine-tuning 
- 긍정 부정 fine-tuning   

**훈련용( KOSPI 200 ) 텍스트 데이터 & 훈련**

- ESG : 총 104만개 텍스트 데이터 사용
- 학습 시 라벨(ex : (e,s,g) -> (1,0,1)) 비율 일정하게 학습
- 학습 결과  :  valid_data 기준 90%대
- 모델 구조 : kobert + nn.Linear(hidden, 3) -> output -> sigmoid(output)

| 네이버 뉴스 | 잡플래닛 장점/단점 리뷰 | 
|-----------|-----------|
|  100만 개   |   3만 개   | 


- 긍정, 부정 : 총 22만개 텍스트 데이터 사용   
- 텍스트 비율 =  긍정(5) : 부정(5)
- 학습 결과 : valid_data 기준 90%대
- 모델 구조 : kobert + nn.Linear(hidden, 2) -> out

| 네이버 영화 리뷰 긍부정 데이터 | 잡플래닛 장점/단점 리뷰 |     
|-----------|-----------|  
|  15만 개   |   7만 개   | 

  





**테스트( KOSDAQ 1700 ) 데이터 & Test-output**   

- 총 460만 개 문장 (네이버 뉴스 + 잡플래닛 리뷰)  
   
- 테스트 output

A. 기업 별 > 년도 별  e, s, g, p, n 점수   
기업의 e,s,g 추세 확인 용도
ex)

|기업|년도|E_score|S_score|G_score|P_score|N_score|  
|---|---|---|---|---|---|---|
|XX전자|2023|0.4|0.6|0.5|0.3|-0.4|

B. 문장 별 > e, s, g, p, n 점수 : 

E,S,G 영역 별 긍부정 단어 counting 용도
ex)

|문장|E_score|S_score|G_score|P_score|N_score|
|---|---|---|---|---|---|
|문장1|0.4|0.6|0.5|0.3|-0.4|

---  
---

`5. SCORE 계산`




**특허점수.ipynb**

- 특허 개수에 따른 점수  

|0개|1~2개|3~4개|5~6개|7개 이상|
|---|---|---|---|---|
|0점|1점|2점|3점|3.5점|


**product_point.ipynb**

- 녹색제품 점수

|0개|1~2개|3~4개|5개 이상|
|---|---|---|---|
|0점|2점|3점|3.5점|

- 리콜 점수

|0개|1개|2개|3개|4개|5개 이상|
|---|---|---|---|---|---|
|5점|4점|3점|2점|1점|0점|

**잡플래닛 데이터 점수 측정 방식**

- S(사회) 점수 책정

| 잡플래닛 S 점수 도출 공식 |
|-----------|
|  (((복지평점 + 복지개수 + 복지 및 급여 + 워라밸) / 4) * ((성장가능성 + 기업추천율) / 2 * 0.01)) * 2 |  


| 잡플래닛 S 점수 범위 |
|-----------|
| min(10) ~ max(25)  |  


- G(지배구조) 점수 책정

| G 점수 도출 공식 |
|-----------|
|((사내문화 + 승진기회 및 가능성 + 경영진) / 3) * (ceo지지율 * 0.01)) * 2 |  

| 잡플래닛 G 점수 범위 |
|-----------|
|min(20) ~ max(50)|  
		
**ESG_count.ipynb**

- Tableau wordcloud구축을 위해 년도 ESG별 seed_words를 이용하여 카운팅

**sentiment_count.ipynb**

- 기업별 년도별 문장들 긍/부정 키워드 기반 카운팅 or KoBERT 내에서 처리한다면 삭제할 수도 있음

**총점수.ipynb**

- 점수 데이터 모두 가져와서 E, S, G 그룹별로 가중치 주어 최종 E, S, G, 총점수 계산
E : (bert_e + 녹색점수 + 특허점수)/15\*100

| bert_e | 녹색점수 | 특허점수 |
|-----------|-----------|------------|
| 기본 15점 ~ 최대 54점 | 기본 10점 ~ 최대 23점 | 기본 13점 ~ 최대 23점 |

S : (bert_s + job_s + 리콜점수)/40\*100

| bert_s | job_s | 리콜점수 |
|-----------|-----------|------------|
| 기본 30점 ~ 최대 50점 | 기본 15점 ~ 최대 25점 |기본 10점 ~ 최대 25점 |

G : (bert_g + job_g + 다트점수)/45\*100

| bert_s | job_s | 
|-----------|-----------|
| 기본 30점 ~ 최대 50점 | 기본 20점 ~ 최대 50점 |

총 점수

| 총 점수 도출 공식| 
|-----------|
| (E + S + G)/3 | 

**점수 결과 형태**

<img src="/image.png/total_score.png" width="900" height="200">


---   
---

`6. Tableau 시각화`

👉🏻 [Tableau]( https://public.tableau.com/shared/M67ZK26GZ?:display_count=n&:origin=viz_share_link)  

Tableau_ESG_Dashboard_public용.twb
전문적인 시각화 차트 Tableau를 사용하여 기업별 ESG 지표 대시보드 생성
중소기업에 대한 투자와 정보 탐색을 원하는 사용자 입장에서 보기 쉽게 구성
불필요한 숫자형 수치들은 줄이고, 워드클라우드, 종합 데이터 위주로 색 대비 명확하게 지정

**1. 화면명세서 제작**

- 디자인 공동 작업 가능한 피그마 프로그램을 사용하여 화면명세서 제작
- ERD를 연계하여 각 페이지별 세부 디자인 계획

**2. 데이터 연결**

- Tableau의 서버를 통해 MariaDB 데이터베이스 연결
- 데이터베이스에 적재된 테이블을 각 요소에 맞게 서로 연결하여 그래프화할 데이터 준비

**3. 페이지 구성**

| 종합 페이지| 
|-----------|
| A. 기업명 검색창 | 
| B. 종합 ESG점수 top3 기업, 급등 ESG점수 top3 기업, 급락 ESG점수 top3 기업 | 
| C. E, S, G별 점수 기업 리스트와 대표 키워드를 나타내는 워드클라우드| 
| D. 급등/급락 ESG 비교 그래프, 업종별 ESG점수 변동 추이, ESG등급 비율 추이| 
<img src="/image.png/메인페이지.JPG" width="800" height="580">

| 랭킹 카테고리| 
|-----------|
| A. 전체 기업들의 ESG등수와 등급 및 전년대비 점수를 한눈에 알아볼 수 있도록 구성 | 
| B. Total, Environment, Social, Governance 별 랭킹 리스트 | 
<img src="/image.png/랭킹카테고리.JPG" width="800" height="580">

| 기업 상세 페이지| 
|-----------|
| A. 해당 기업의 전체 ESG 등급을 상단에 배치창 | 
| B. 해당 기업의 대표 워드클라우드 및 긍/부정 비율 | 
| C. E,S,G 점수에 따라 나타나는 다각형 그래프| 
| D. E,S,G 막대그래프로 연도별 ESG 변동 추이 표현| 
| E. 키워드를 통해 나타난 긍/부정 비율로 기업 인식 제고| 
<img src="/image.png/상세기업페이지.JPG" width="800" height="580">


**4. 대시보드 연동**

- 대시보드 액션으로 3페이지의 대시보드를 연결하고 각 페이지를 편리하게 오갈 수 있게 구성
- 기업명을 클릭하여 랭킹 카테고리 및 기업 상세 페이지로 이동
- 개별 아이콘을 사용하여 각 페이지로 되돌아 갈 수 있게 구현

**5. Tableau public 게시**

- 완성된 대시보드를 Tableau public에 공유하여 ESG 평가 및 모니터링 서비스 제안


