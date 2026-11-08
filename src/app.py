import requests
from bs4 import BeautifulSoup

url = 'https://www.python.org/'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
# print(soup)

# latest_news = soup.find('div' , attrs={'class': 'medium-widget blog-widget'})
# # print(latest_news)
# titles = latest_news.find_all('a')
# # print(titles)
# for item in titles:
#     print(item.get_text())
#     print('-'*30)
# ##########################################

# times = latest_news.find_all('time')
# for item in times:
#     print(item.get_text())
#     print('-'*30)

events_title = soup.select('div.medium-widget.event-widget.last a')
events_time = soup.select('div.medium-widget.event-widget.last time')

for item in events_title:
    print(item.get_text())
    print('-'*30)

for item in events_time:
    print(item.get_text())
    print('-'*30)
    
    