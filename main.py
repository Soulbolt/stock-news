import os
from dotenv import load_dotenv
import requests
from twilio.rest import Client

load_dotenv()

STOCKS_API_KEY = os.getenv('STOCKS_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCKS_END_POINT = "https://www.alphavantage.co/query?"
sep_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCKS_API_KEY,
}
NEWS_END_POINT = "https://newsapi.org/v2/everything?"
ned_parameters = {
    "language": "en",
    "qinTitle": COMPANY_NAME,
    "apikey": NEWS_API_KEY,
}
## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stocks_response = requests.get(url=STOCKS_END_POINT, params= sep_parameters)
stocks_response.raise_for_status()
data_stocks = stocks_response.json()["Time Series (Daily)"]
# Get two different dates closing data
data_list = [value for (key, value) in data_stocks.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = yesterday_data["4. close"]

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔼"
else:
    up_down = "🔽"

# Get percentage difference
percentage = round((difference/float(yesterday_closing_price)) * 100)


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
# check if stock difference is up or down by 5%
if percentage <= 5 and percentage >= -5:
    news_response = requests.get(url=NEWS_END_POINT, params=ned_parameters)
    news_response.raise_for_status()
    articles = news_response.json()["articles"]
    first_three_articles = articles[:3]

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 
formatted_articles = [f"{STOCK_NAME}: {up_down}{percentage}%\nHeadline: {aritcle['title']}. \nBrief: {aritcle['description']}" for aritcle in first_three_articles]

account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

client = Client(account_sid, auth_token)

for article in formatted_articles:
    message = client.messages.create(from_=os.environ.get('TWILIO_PHONE_NUMBER'),
                        to=os.environ.get('CELL_PHONE_NUMBER'),
                        body=article)
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
