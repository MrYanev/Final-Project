#References: https://www.youtube.com/watch?v=o-zM8onpQZY&t=1368s
#References: https://github.com/TheCodex-Me/Projects/blob/master/Sentiment-Analysis-Stock-News-Final/main.py

import os
import openai
import pandas as pd
import matplotlib.pyplot as plt
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

openai.api_key = os.getenv("API_KEY")

finviz_url = 'https://finviz.com/quote.ashx?t='
finviz_end = '&p=d'
tickers = ['AMZN', 'GOOG', 'VOO', 'TSLA']

news_tables = {}
for ticker in tickers:
    url = finviz_url + ticker + finviz_end

    req = Request(url=url, headers={'user-agent': 'Sentiment-scraper'})
    response = urlopen(req)

    html = BeautifulSoup(response, features='html.parser')
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table

parsed_data = []

for ticker, news_table in news_tables.items():

    for row in news_table.findAll('tr'):

        title = row.a.text
        date_data = row.td.text.split(' ')

        if len(date_data) == 1:
            time = date_data[0]
        else:
            date = date_data[0]
            time = date_data[1]

        parsed_data.append([ticker, date, time, title])

df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title'])

response = openai.Completion.create(
    model = 'text-davinci-003',
    prompt= f'Classify the sentiment in these headlines: {df}',
    temperature=0,
    max_tokens=60,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
)
#Reference OpenAI
# @https://platform.openai.com/docs/guides/fine-tuning

plt.figure(figsize=(10,8))
mean_df = df.groupby(['ticker', 'date']).mean().unstack()
mean_df = mean_df.xs('compound', axis="columns")
mean_df.plot(kind='bar')
plt.show()

#References: https://www.youtube.com/watch?v=o-zM8onpQZY&t=1368s
#References: https://github.com/TheCodex-Me/Projects/blob/master/Sentiment-Analysis-Stock-News-Final/main.py
