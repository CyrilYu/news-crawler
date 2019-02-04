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
import mimetypes
from flask_mail import Mail
from flask_mail import Message
from flask import send_from_directory

import requests
from bs4 import BeautifulSoup
import random

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/download', methods=['GET', 'POST'])
def download():
  filepath = os.path.join(app.root_path, '..')
  return send_from_directory(filepath, 'output.csv', mimetype='application/octet-stream', as_attachment=True)

#get /searching
@app.route('/searching', methods=['GET', 'POST'])
def searching():
  print(request.is_json)
  data = request.get_json()
  keywords = data['keywords']
  weeks = data['weeks']
  google_url = 'https://www.google.com/search'
  user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', \
      'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
      (KHTML, like Gecko) Element Browser 5.0', \
      'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)', \
      'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
      'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14', \
      'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
        Version/6.0 Mobile/10A5355d Safari/8536.25', \
      'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/28.0.1468.0 Safari/537.36', \
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']
  with open(os.path.join(APP_ROOT, 'config.yml'), 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
  print(cfg['reducenews'])
  with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', lineterminator='\n')
    writer.writerow(['id', 'date', 'media', 'title', 'url'])
    counter = 1
    saver = 1
    for key, value in cfg['reducenews'].items():
      q_str = 'site:' + value['url'] + ', ' + keywords
      print(q_str)
      
      print(saver)
      print(saver%10)
      sleep_time = random.randint(60, 180)
      if saver%10 == 0:
        time.sleep(sleep_time)
      if saver%29 == 0:
        time.sleep(random.randint(300, 480))
      if saver%51 == 0:
        time.sleep(1200)
      # 查詢參數
      # q_str = 'site:today.line.me, ' + data['keywords']
      my_params = {'q': q_str, 'as_qdr': 'w' + weeks}
      index = random.randint(0, 9)
      user_agent = user_agents[index]

      headers = {'user-agent': user_agent}
      print(headers)

      # 下載 Google 搜尋結果
      r = requests.get(google_url, params=urlencode(my_params))
      r.encoding = 'utf-8'
      print(r.encoding)

      # 確認是否下載成功
      print(r.status_code)
      print(r.url)
      if r.status_code == requests.codes.ok:
        # 以 BeautifulSoup 解析 HTML 原始碼
        soup = BeautifulSoup(r.text, 'html.parser')

        # 觀察 HTML 原始碼
        # print(soup.prettify())
        # https://www.google.com/search?q=site:travel.ettoday.net+Hoi&tbs=cdr:1,cd_min:07/22/2018,cd_max:12/31/2018
        # 以 CSS 的選擇器來抓取 Google 的搜尋結果
        items = soup.select('div.g > h3.r > a[href^="/url"]')
        dates = soup.select('div.g > div.s > span.st')
        date_counter = 1
        for i in items:
          time.sleep(random.randint(1, 3))
          url = urllib.parse.unquote(urllib.parse.unquote(i.get('href').replace("/url?q=", "")))
          title = i.text
          if url.index('&sa=U') > 0:
            url = url.split('&sa=U', 1)[0]
          if (len(dates[date_counter-1].text.split(' ... ')[0])) == 10:
            date = dates[date_counter-1].text.split(' ... ')[0].replace('年', '/').replace('月', '/').replace('日', '')
            writer.writerow([counter, date, value['title'], title, url])
          else:
            writer.writerow([counter, '', value['title'], title, url])
          counter += 1
          date_counter += 1
          # result.append({'title': i.text, 'url': i.get('href')})
          # 標題
          print("標題：" + i.text)
          # # 網址
          # print("網址：" + i.get('href'))
        r.close()
        time.sleep(2)
      saver += 1
  return json.dumps({'message': 'test'})

app.run(port=5000)
