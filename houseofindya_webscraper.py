import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd

from time import sleep
from random import randint


product = []
new_price = []
old_price = []
disccount = []
description = []

urls = []


url = "https://www.houseofindya.com/zyra/hair-jewelry/cat?depth=3&label=Jewelry-Shop%20By%20Category-Hair%20Jewelry"
results = requests.get(url)
soup = BeautifulSoup(results.text,"html.parser")

iteam_div = soup.find_all('li', attrs={'data-cat':'Indya Clothing'})


for data in iteam_div:
    link = data['data-url']
    urls.append(link)
    name = data.a['title']
    product.append(name)



for url in urls:
    sleep(randint(2,5))

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    right_div = soup.find_all('div', class_="prodRight")

    for info in right_div:

        #old price
        o_price = info.find('span', style="text-decoration:line-through;font-size:20px;color:#000").text
        old_price.append(o_price)

        #new price
        n_price = info.find('span', style="font-size:20px;color:#ed1c24").text
        new_price.append(n_price)

        #disscount
        disc = info.find('span', style="font-size:12px;color:#000;float:right;margin:5px 0 0 10px").text
        disc = disc.replace('(','')
        disc = disc.replace(')','')
        disccount.append(disc)

        #description
        descri = info.find('div', class_="prodecbox current").text
        description.append(descri)

hair_jewelry = pd.DataFrame({
    'products': product,
    'new price': new_price,
    'old price' : old_price,
    'disccount' : disccount,
    'description': description
})


hair_jewelry['new price'] = hair_jewelry['new price'].astype(int)
hair_jewelry['old price'] = hair_jewelry['old price'].astype(int)


hair_jewelry.to_csv('hair_jewlry.csv')

