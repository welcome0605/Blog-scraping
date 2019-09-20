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

output_file = 'singapore.csv'

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
        i = 0
        for title in titles:
            temp = []
            temp.append(city)
            # titles = content.find_elements_by_class_name('building-card__address')
            temp.append(title)
            j = 0
            while j < 10:
                temp.append(po[i + j * len(titles)])
                j += 1
            j = 0
            while j < 10:
                temp.append(dd[i + j * len(titles)])
                j += 1
            j = 0
            while j < 10:
                temp.append(hd[i + j * len(titles)])
                j += 1

            i += 1
            writer.writerow(temp)

def pull_data(base_url, city):
    po = []
    dd = []
    hd = []
    sample = []
# ray-text--body building-card__address
    link = base_url + city + '?capacity=' + str('1')
    driver.get(link)
    contents = driver.find_elements_by_class_name('ray-card__content')
    send_contents = contents
    for content in contents:
        titles = content.find_elements_by_class_name('building-card__address')
        for title in titles:     
            sample.append(title.text)

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

    # print(sample)

    for i in range(2, 11):
        t_po = []
        t_dd = []
        t_hd = []
        names = []
        link = base_url + city + '?capacity=' + str(i)
        driver.get(link)
        contents = driver.find_elements_by_class_name('ray-card__content')
        for content in contents:
            titles = content.find_elements_by_class_name('building-card__address')
            for title in titles:
                names.append(title.text)

            prices = content.find_elements_by_class_name('building-card__text-pricing')
            for price in prices:
                # names.append(title)
                targets = price.find_elements_by_tag_name('div')
                # print(len(targets))
                if len(targets) == 4:
                    j = 0
                    for target in targets:
                        j += 1
                        if j == 1:
                            continue
                        if j == 2:
                            for real in target.find_elements_by_class_name('office-pricing'):
                                t_po.append(real.text.replace('\n', ' ').replace(" ", ""))
                                # print(real.text.replace('\n', ' ').replace(" ", ""))
                        if j == 3:
                            for real in target.find_elements_by_class_name('dedicated-desk-pricing'):
                                t_dd.append(real.text.replace('\n', ' ').replace(" ", ""))
                                # print(real.text.replace('\n', ' ').replace(" ", ""))
                        if j == 4:
                            for real in target.find_elements_by_class_name('hot-desk-pricing'):
                                t_hd.append(real.text.replace('\n', ' ').replace(" ", ""))
                                # print(real.text.replace('\n', ' ').replace(" ", ""))

                else:
                    t_po.append('n/a')
                    t_dd.append('n/a')
                    t_hd.append('n/a')
        # print('\n')
        # print(names)

        k = 0
        for j in range(0, len(sample)):
            if sample[j] in names:
                # print("yes")
                po.append(t_po[k])
                dd.append(t_dd[k])
                hd.append(t_hd[k])
                k += 1
            else:
                # print("no")
                po.append('n/a')
                dd.append('n/a')
                hd.append('n/a')
        # print(po)
        # print(dd)
        # print(hd)

    add_csv_row(city, sample, po, dd, hd)

driver = setUpChrome()
add_csv_head()


base_url = 'https://www.wework.com/l/'
pull_data(base_url, 'singapore')

# ray-grid__cell--span-4 ray-grid__cell--span-6-desktop
# ray-grid__cell--span-4 ray-grid__cell--span-6-desktop
# 'shenzhen', 'suzhou', 'hong-kong', 'shanghai--31'

print("done")
