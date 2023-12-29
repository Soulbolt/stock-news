import os
from dotenv import load_dotenv
import requests

load_dotenv()

STOCKS_API_KEY = os.getenv('STOCKS_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCKS_END_POINT = "https://www.alphavantage.co/query?"
sep_parameters = {
    "function": "TIME_SERIES_INTRADAY",
    "symbol": "TSLA",
    "interval": "60min",
    "month": "2023-11",
    "outputsize": "compact",
    "apikey": STOCKS_API_KEY,
}
NEWS_END_POINT = "https://newsapi.org/v2/top-headlines?"
ned_parameters = {
    "q": "tesla",
    "from": "2023-11-30",
    "sortBy": "publishedAt",
    "apikey": NEWS_API_KEY,
}
## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
response1 = requests.get(url=STOCKS_END_POINT, params= sep_parameters)
response1.raise_for_status()
data_stocks = response1.json()
# Get two different dates closing data
day1_stock_close = data_stocks["Time Series (60min)"]["2023-11-30 19:00:00"]["4. close"]
day2_stock_close = data_stocks["Time Series (60min)"]["2023-11-29 19:00:00"]["4. close"]
# Get percentage difference
percentage_to_compare = (float(day1_stock_close)/float(day2_stock_close))* 100

response2 = requests.get(url=NEWS_END_POINT, params=ned_parameters)
response2.raise_for_status()
data_news = response2.json()
# print(data_news)

# check if stock difference is up or down by 5%
if percentage_to_compare <= 105 and percentage_to_compare >=95:
    print(data_news["articles"]) 

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
