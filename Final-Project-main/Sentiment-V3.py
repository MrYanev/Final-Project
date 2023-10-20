#Reference https://www.kaggle.com/code/mmmarchetti/sentiment-analysis-on-financial-news
# @MARCOS MARTINS MARCHETTI 2020

import os 
import requests
import warnings
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

finviz_url = 'https://finviz.com/quote.ashx?t='
finviz_end = '&p=d'
tickers = ['AMZN', 'GOOG', 'VOO', 'TSLA']

warnings.filterwarnings('ignore', category=FutureWarning)

html_tables = {}


"""
//This section is when working with a file

for table_name in os.listdir('../input'):
    #File's path
    table_path = f'../input/{table_name}'

    #Open python file in ready-only mode
    table_file = open(table_path, 'r')

    #Read the contents of the file into 'html'
    html = BeautifulSoup(open(table_path, 'r'))

    #Takes the contet of news-table and loads it to variable
    html_table = html.find(id='news-table')

    #Add table to tables dictionary
    html_tables[table_name] = html_table
print('Done!')
"""

#Version for directly scraping the website

#Create URL for all desired tickers
for ticker in tickers:
    #Concatenate the parts to create the URL
    url = finviz_url + ticker + finviz_end

    #Makes a GET request to the URL 
    req = Request(url=url, headers={'user-agent': 'ScraperV2'})
    response = urlopen(req)

    #Parse the HTML content 
    html = BeautifulSoup(response, features='html.parser')

    #Find the element with id news-table
    html_table = html.find(id='news-table')

    #Add the table to the dictionary
    html_tables[ticker] = html_table

#print('Done!')
#print(html_tables['TSLA'])
tsla = html_tables['TSLA']
amzn = html_tables['AMZN']
voo = html_tables['VOO']
goog = html_tables['GOOG']

#Get all table rows
tesla_tr = tsla.findAll('tr')

#For each row
for i, table_row in enumerate(tesla_tr):
    #Read elements in <a>
    link_text = table_row.a.get_text()
    #Read the text of 'td' into data_text
    data_text = table_row.td.get_text()
    #Print count
    print(f'{i}:')
    #Print contents
    print(link_text)
    print(data_text)

#List for parsed news
parsed_news = []
#Iterate through the news
for ticker_name, news_table in html_tables.items():
    #Iterate through all tr tags in the table
    for x in news_table.findAll('tr'):

        #Read the text from the tag
        text = x.get_text()

        #Split the text in the td tag
        date_scrape = x.td.text.split()
        headline = x.a.text

        #If len is 1 load 'time'
        #If not load 'date' as 1st element
        if len(date_scrape) == 1:
            time = date_scrape[0]

        else:
            date = date_scrape[0]
            time = date_scrape[1]

        parsed_news.append([ticker, date, time, headline])

print(parsed_news[:10])

from nltk.sentiment.vader import SentimentIntensityAnalyzer

#New words and values
new_words= {
    'crushes': 10,
    'beats': 5,
    'misses': -5,
    'trouble': -10,
    'falls': -100,
}

#Iniciate the sentiment analyser
vader = SentimentIntensityAnalyzer()
#Update the lexicon
vader.lexicon.update(new_words)

columns = ['ticker', 'date', 'time', 'headline']
#Convert list of lists to DF
scored_news = pd.DataFrame(parsed_news, columns=columns)
#Iterate through headlines and get polarity socres
scores = scored_news['headline'].apply(vader.polarity_scores)
#Convert the list of dict into dataframe
scores_df = pd.DataFrame.from_records(scores)
#Join the DataFrames
scored_news = scored_news.join(scores_df)
#Convert date from string to date-time
scored_news['date'] = pd.to_datetime(scored_news.date).dt.date

import matplotlib.pyplot as plt
import seaborn as sns

mean_c = scored_news.groupby(['date', 'ticker']).mean()

#Unstack the column ticker
mean_c = mean_c.unstack('ticker')

mean_c = mean_c.xs('compound', axis='columns')

mean_c.plot(kind='bar', figsize=(10,5), width=1)


#Cound the number of headlines
num_news_before = scored_news['headline'].count()

#Drop duplicates
scored_news_clean = scored_news.drop_duplicates(subset=['ticker', 'headline'])

#Cound number of dups after dropping duplicates
num_news_after = scored_news_clean['headline'].count()

#Sentiment on asingle day

#set the index to ticker and date
single_day = scored_news_clean.set_index(['ticker', 'date'])

single_day = single_day.xs('TSLA')

single_day = single_day['2023-04-10']

single_day['time'] = pd.to_datetime(single_day['time']).dt.time

single_day = single_day.set_index('time')

single_day = single_day.sort_index()
print(single_day.info())

TITLE = "Positive, negative and neutral sentiment for TSLA on 2023-04-10"
COLORS = ["red", "orange", "green"]

# Drop the columns that aren't useful for the plot
plot_day = single_day.drop(['headline', 'compound'], axis=1)

# Change the column names to 'negative', 'positive', and 'neutral'
plot_day.columns = ['negative', 'positive', 'neutral']

# Plot a stacked bar chart
plot_day.plot(kind='bar', color=COLORS, figsize=(10,5), width=1)