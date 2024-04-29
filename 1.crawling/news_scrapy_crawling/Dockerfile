FROM python:3.9-slim
WORKDIR /app

# 파일 복사
COPY . /app

# cron 설치
RUN apt-get update && apt-get -y install cron

# Cron 작업 설정
COPY crontab /etc/cron.d/scrapy-cron
RUN chmod 0644 /etc/cron.d/scrapy-cron
RUN crontab /etc/cron.d/scrapy-cron

# 환경 설정 로그 파일 생성(디버깅 용)
RUN touch /var/log/cron.log

# cron 실행 및 로그 출력
CMD cron && tail -f /var/log/cron.log