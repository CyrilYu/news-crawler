# -*- coding: utf-8 -*-

import os
from flask import Flask,jsonify,request
from flask_cors import *
import yaml
import json
from urllib.parse import urlencode, quote_plus
import urllib
import csv
import time
import urllib.parse

import requests
from bs4 import BeautifulSoup
import random

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

#get /searching
@app.route('/searching', methods=['GET', 'POST'])
def searching():
  print(request.is_json)
  data = request.get_json()
  keywords = data['keywords']
  google_url = 'https://www.google.com/search'
  with open(os.path.join(APP_ROOT, 'config.yml'), 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
  print(cfg['reducenews'])
  with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', lineterminator='\n')
    writer.writerow(['id', 'media', 'title', 'url'])
    counter = 1
    saver = 1
    for key, value in cfg['reducenews'].items():
      q_str = 'site:' + value['url'] + ', ' + keywords
      print(q_str)
      print(saver)
      print(saver%3)
      if saver%3 == 0:
        time.sleep(60)
      # 查詢參數
      # q_str = 'site:today.line.me, ' + data['keywords']
      my_params = {'q': q_str}

      headerlist = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 OPR/42.0.2393.94",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36 OPR/47.0.2631.39",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"]
      user_agent = random.choice(headerlist)
      headers = {'User-Agent': user_agent}
      print(headers)

      # 下載 Google 搜尋結果
      r = requests.get(google_url, params=urlencode(my_params), headers=headers)
      r.encoding = 'utf-8'
      print(r.encoding)

      # 確認是否下載成功
      print(r.status_code)
      if r.status_code == requests.codes.ok:
        # 以 BeautifulSoup 解析 HTML 原始碼
        soup = BeautifulSoup(r.text, 'html.parser')

        # 觀察 HTML 原始碼
        # print(soup.prettify())

        # 以 CSS 的選擇器來抓取 Google 的搜尋結果
        items = soup.select('div.g > h3.r > a[href^="/url"]')
        for i in items:
          url = urllib.parse.unquote(urllib.parse.unquote(i.get('href').replace("/url?q=", "")))
          title = i.text
          if url.index('&sa=U') > 0:
            url = url.split('&sa=U', 1)[0]
          writer.writerow([counter, value['title'], title, url])
          counter += 1
          # result.append({'title': i.text, 'url': i.get('href')})
          # 標題
          print("標題：" + i.text)
          # # 網址
          # print("網址：" + i.get('href'))
      saver += 1
      time.sleep(2)
  return json.dumps({'message': 'test'})

app.run(port=5000)