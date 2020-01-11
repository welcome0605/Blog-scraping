import csv
import sys
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

import requests
from bs4 import BeautifulSoup

import time

output_file = 'contact.csv'


def add_csv_head():
    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['site link', 'email', 'instagram link'])

def add_csv_row(site_link, email, i_link):
    with open(output_file, 'a', newline='', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([site_link, email, i_link])

add_csv_head()

# base_url = 'https://www.shopistores.com/shopify/'

# i = 1
# while i < 168:
#     url = base_url + 'i'

page1 = requests.get("https://myip.ms/browse/sites/1/ownerID/376714/ownerID_A/1")
soup1 = BeautifulSoup(page1.content, 'html.parser')
# site_link = soup.findAll(attrs={"data-title" : "Store Address"})[0].find('a', attrs={"rel" : "nofollow"}, href = True)
for a in soup1.findAll(attrs={"class" : "row_name"}):
    # site_link = a.find('a', attrs={"rel" : "nofollow"}, href = True)['href']
    # print(a.text)
    str = 'https://www.'
    site_link = a.text
    site_link = site_link[:-1]
    str += site_link
    site_link = str
    i_link = "N/A"
    email = "N/A"
    f_link = "N/A"
    # print(site_link['href'])
    page2 = requests.get(site_link)
    soup2 = BeautifulSoup(page2.content, 'html.parser')
    for b in soup2.find_all('a', href = True):
        # print(b['href'].find('instagram'))
        if b['href'].find('facebook') != -1:
            f_link = b['href']
        if b['href'].find('instagram') != -1:
            i_link = b['href']
    if f_link == "N/A":
        add_csv_row(site_link, "N/A", "N/A")
        # print("N/A")
    else:
        add_csv_row(site_link, f_link, i_link)

        page3 = requests.get(f_link)
        soup3 = BeautifulSoup(page3.content, 'html.parser')
        # add_csv_row(site_link, f_link, i_link)
        # soup3.find_all()
        # print(soup3.findAll('a', attrs={'data-ft' : '{"tn":"-U"}'}, href = True))
        # for c in soup3.findAll('a', attrs={'data-ft' : '{"tn":"-U"}'}, href = True):
        #     print(c['href'])
        #     print('\n')
    # break


# soup.find_all('p', class_='outer-text')
# def add_csv_row(city, titles, po, dd, hd):


print("done")
