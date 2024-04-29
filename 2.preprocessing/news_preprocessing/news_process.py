import pandas as pd
import datetime
from mariadb import MariaDB
import os

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_DATABASE'),
    'charset' : 'utf8mb4'
}
db = MariaDB(db_config)
now = datetime.datetime.now()
df = pd.read_csv(f'kosdaq_data_{now.strftime('%Y-%m-%d')}.csv', on_bad_lines='skip')
data = []

for _, row in df.iterrows():
    sentences = row['content'].split('&&')
    for sentence in sentences:
        if len(sentence) > 40:
            data.append((row['company'], row['date'], row['url'], sentence))
df = pd.DataFrame(data, columns=['Company','Date','URL', 'Sentence'])
df = df.drop_duplicates(subset='Sentence')
df.dropna(inplace=True)
db_data = list(zip(df['Company'],df['Date'],df['URL'],df['Sentence']))

db.insert_many('tb_news','기업명,날짜,URL,문장',db_data)