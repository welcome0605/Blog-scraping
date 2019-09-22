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

output_file = 'china.csv'

def setUpChrome():
    global driver
    # Using Chrome
    chrome_options = webdriver.ChromeOptions()
    #prefs = {"profile.managed_default_content_settings.images": 2}
    #chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    #chrome_options.add_argument('headless')

    scriptpath = os.path.realpath(__file__)
    foldername = os.path.basename(scriptpath)
    scriptpath = scriptpath[:scriptpath.find(foldername)]

    scriptpath += 'chromedriver'

    driver = webdriver.Chrome(scriptpath, chrome_options=chrome_options)
    return driver

def add_csv_head():
    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['city', 'name', 'po1', 'po2', 'po3', 'po4', 'po5', 'po6', 'po7', 'po8', 'po9', 'po10', 'dd1', 'dd2', 'dd3', 'dd4', 'dd5', 'dd6', 'dd7', 'dd8', 'dd9', 'dd10', 'hd1', 'hd2', 'hd3', 'hd4', 'hd5', 'hd6', 'hd7', 'hd8', 'hd9', 'hd10'])

def add_csv_row(city, titles, po, dd, hd):
    with open(output_file, 'a', newline='', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        # writer.writerow(['city', 'name', 'po1', 'po2', 'po3', 'po4', 'po5', 'po6', 'po7', 'po8', 'po9', 'po10', 'dd1', 'dd2', 'dd3', 'dd4', 'dd5', 'dd6', 'dd7', 'dd8', 'dd9', 'dd10', 'hd1', 'hd2', 'hd3', 'hd4', 'hd5', 'hd6', 'hd7', 'hd8', 'hd9', 'hd10'])
        # for i in range(0, len(po)):       
        # writer.writerows([city, title, po[0], po[1], po[2], po[3], po[4], po[5], po[6], po[7], po[8], po[9], dd[0], dd[1], dd[2], dd[3], dd[4], dd[5], dd[6], dd[7], dd[8], dd[9], hd[0], hd[1], hd[2], hd[3], hd[4], hd[5], hd[6], hd[7], hd[8], hd[9]])
        # titles = content.find_elements_by_class_name('building-card__address')
        # for content in contents:
            # names.append(content)
        # print(len(po), len(dd), len(hd))
        # for i in range(0, len(po)):  
        #     print(po[i])     
        # print(po)
        # print('\n')
        # print(dd)
        # print('\n')
        # print(hd)
        # for title in titles:
        #     print(title.text)
        # print('\n')
        title = ['189 Yunxia Lu Oceanwide Fortune Center, 7/F., JIANGHAN Wuhan 430072', 'No.465 Guan Shan Da Dao, Hongshan Qu Wuhan Shi, Hubei Sheng Wuhan 430073']
        i = 0
        temp = []
        temp.append(city)
        temp.append(title[0])

        j = 0
        while j < 4:
            temp.append(po[j])
            j += 1
        j = 5
        while j <= 15:
            temp.append(po[j])
            j += 2

        j = 0
        while j < 4:
            temp.append(dd[j])
            j += 1
        j = 5
        while j <= 15:
            temp.append(dd[j])
            j += 2

        j = 0
        while j < 4:
            temp.append(hd[j])
            j += 1
        j = 5
        while j <= 15:
            temp.append(hd[j])
            j += 2

        writer.writerow(temp)

        temp = []
        temp.append(city)
        temp.append(title[1])
        j = 0
        while j < 3:
            temp.append('n/a')
            j += 1
        j = 4
        while j <= 16:
            temp.append(po[j])
            j += 2

        j = 0
        while j < 3:
            temp.append('n/a')
            j += 1
        j = 4
        while j <= 16:
            temp.append(dd[j])
            j += 2

        j = 0
        while j < 3:
            temp.append('n/a')
            j += 1
        j = 4
        while j <= 16:
            temp.append(hd[j])
            j += 2

        writer.writerow(temp)


            # j = 0
            # while j < 10:
            #     if j < 4:
            #         temp.append()
            #     temp.append(po[i + j * 2])
            #     j += 1
            # j = 0
            # while j < 10:
            #     temp.append(dd[i + j * 2])
            #     j += 1
            # j = 0
            # while j < 10:
            #     temp.append(hd[i + j * 2])
            #     j += 1

            # i += 1
            

def pull_data(base_url, city):
    po = []
    dd = []
    hd = []
    for i in range(1,11):
        names = []
        link = base_url + city + '?capacity=' + str(i)
        driver.get(link)
        contents = driver.find_elements_by_class_name('ray-card__content')

        for content in contents:

            # content.find_elements_by_class_name('building-card__text-pricing')
            prices = content.find_elements_by_class_name('building-card__text-pricing')
            for price in prices:
                # names.append(title)
                targets = price.find_elements_by_tag_name('div')
                # print(len())
                if len(targets) == 4:
                    j = 0
                    for target in targets:
                        j += 1
                        if j == 1:
                            continue
                        if j == 2:
                            for real in target.find_elements_by_class_name('office-pricing'):
                                po.append(real.text.replace('\n', ' ').replace(" ", ""))
                                # print(real.text.replace('\n', ' ').replace(" ", ""))
                        if j == 3:
                            for real in target.find_elements_by_class_name('dedicated-desk-pricing'):
                                dd.append(real.text.replace('\n', ' ').replace(" ", ""))
                                # print(real.text.replace('\n', ' ').replace(" ", ""))
                        if j == 4:
                            for real in target.find_elements_by_class_name('hot-desk-pricing'):
                                hd.append(real.text.replace('\n', ' ').replace(" ", ""))
                                # print(real.text.replace('\n', ' ').replace(" ", ""))

                else:
                    po.append('n/a')
                    dd.append('n/a')
                    hd.append('n/a')
    add_csv_row(city, driver.find_elements_by_class_name('building-card__address'), po, dd, hd)

driver = setUpChrome()
add_csv_head()


urls = ['wuhan']

i = 0
while i < 1:
    base_url = 'https://www.wework.com/l/'
    pull_data(base_url, urls[i])
    # time.sleep(10)
    i += 1

print("done")
# , 'shenzhen', 'suzhou', 'hong-kong', 'shanghai--31'