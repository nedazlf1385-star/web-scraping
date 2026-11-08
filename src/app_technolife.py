from bs4 import BeautifulSoup
import requests
import sqlite3

DB_NAME = 'LaptopData.db'
conn = sqlite3.connect(DB_NAME)
print('DB CREATED')

query = '''CREATE TABLE IF NOT EXISTS laptop_techno
(id INTEGER primary key AUTOINCREMENT,
description TEXT,
price REAL,
image_url TEXT,
link TEXT)
'''
cursor = conn.cursor()
cursor.execute(query)
conn.commit()
print('TABLE CREATED')

url = 'https://www.technolife.com/category/laptop-equipment/laptop'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
# print(soup)

cards = soup.select('section.relative.w-full.rounded-\\[10px\\].bg-white')
# print(len(cards))

for card in cards:

    description = card.select_one('h2').get_text().strip()
    
    if description == None:
        continue
    # print(description)
    # print('-'*30)

    price = card.select_one('p.text-\\[22px\\].font-semiBold.leading-5').get_text().strip()
    if price ==  None:
        continue
    # print(price)
    # print('-'*30)

    img_url = 'https://www.technolife.com' + card.select_one('img').get('src')
    # print(img_url)
    # print('-'*30)

    link = 'https://www.technolife.com' + card.select_one('a').get('href')
    # print(link)
    # print('-'*30)

    query = '''
            INSERT INTO laptop_techno(description, price, image_url, link)
            VALUES(?, ?, ?, ?)'''
    
    cursor = conn.cursor()
    cursor.execute(query, (description, price, img_url, link))
    conn.commit()
    
conn.close()
print('DATA SCRAP')    


# Mobile Scraping - Technolife

import re
import time
import sqlite3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

conn = sqlite3.connect('LaptopData.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS mobile_techno (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    brand TEXT,
    storage TEXT,
    ram TEXT,
    color TEXT,
    rating TEXT,
    link TEXT UNIQUE
)
""")
conn.commit()

url = 'https://www.technolife.com/category/mobile/mobile-phone'
headers = {'User-Agent': 'Mozilla/5.0'}

response = requests.get(url, headers=headers, timeout=30)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')

links = list(dict.fromkeys(
    urljoin(url, a['href'])
    for a in soup.select('a[href]')
    if '/product/' in a['href'].lower()
    and 'technolife.com' in urljoin(url, a['href'])
))[:10]

print('Tedade mahsoolat:', len(links))

for link in links:
    try:
        page = requests.get(link, headers=headers, timeout=30)
        page.raise_for_status()
        s = BeautifulSoup(page.text, 'html.parser')

        title = s.title.get_text(strip=True) if s.title else ''

        meta = s.select_one('meta[name="description"]')
        description = meta.get('content', '') if meta else ''

        text = s.get_text(' ', strip=True)

        def find(pattern):
            m = re.search(pattern, text, re.I)
            return m.group(1).strip() if m else ''

        brand = next((b for b in [
            'Samsung', 'Apple', 'Xiaomi', 'Redmi',
            'POCO', 'Honor', 'Huawei', 'Nokia', 'Realme'
        ] if b.lower() in title.lower()), '')

        storage = find(
            r'(?:حافظه داخلی|حافظه)\s*[:：]?\s*(\d+\s*(?:GB|TB|گیگابایت|ترابایت))'
        )

        ram = find(
            r'(?:حافظه RAM|رم)\s*[:：]?\s*(\d+\s*(?:GB|گیگابایت))'
        )

        color = find(r'رنگ\s*[:：]?\s*([^,،|]{2,30})')

        rating = find(
            r'(?:امتیاز کاربران|میانگین امتیاز|امتیاز)\s*[:：]?\s*(\d+(?:\.\d+)?)'
        )

        data = (
            title, description, brand, storage,
            ram, color, rating, link
        )

        cursor.execute("""
            INSERT INTO mobile_techno
            (title, description, brand, storage, ram, color, rating, link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(link) DO UPDATE SET
                title=excluded.title,
                description=excluded.description,
                brand=excluded.brand,
                storage=excluded.storage,
                ram=excluded.ram,
                color=excluded.color,
                rating=excluded.rating
        """, data)

        conn.commit()

        print('\nName:', title)
        print('Tozih:', description)
        print('Brand:', brand or 'Peyda nashod')
        print('Hafeze:', storage or 'Peyda nashod')
        print('RAM:', ram or 'Peyda nashod')
        print('Rang:', color or 'Peyda nashod')
        print('Emtiaz:', rating or 'Peyda nashod')
        print('Link:', link)

        time.sleep(1)

    except requests.RequestException as e:
        print('Khata:', link, e)

conn.close()
print('MOBILE SCRAPING FINISHED')
