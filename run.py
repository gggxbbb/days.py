#!/usr/bin/python3
# -*- coding: utf-8 -*-
import datetime
import json
import requests
import random
import os

ua = [
    'Mozilla/5.0 (Android 9; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0',
]

ss = []

for v in ua:
    ## 实例化 session
    s = requests.session()
    ## 设置不同的 UA
    s.headers.update({'User-Agent': v})
    ## 添加到 List
    ss.append(s)

http_count = 0

# 获取 Response
def getReq(url) -> requests.Response:
    ## 随机获取 session
    s = ss[random.randint(0, len(ua)-1)]
    ## 获取 Response
    req = s.get(url)
    ## 判断是否获取成功
    if not req.status_code == 200:
        ### 失败抛出输出错误
        print(req.url,req.status_code,req.text)
        ### 并退出
        sys.exit(1)
    global http_count
    http_count += 1
    ## 返回获取的 Response
    return req

# 获取 JSON 数据
def getJson(url):
    ## 获取 Response
    req = getReq(url)
    ## 设置编码
    req.encoding='utf-8'
    ## 序列化并返回
    return json.loads(req.text)

def sortDict(dict,reverse=False,key=lambda e:e[0]):
    n_keys = []
    n_dict = {}
    s_list = sorted(dict.items(),key=key,reverse=reverse)
    for v in s_list:
        n_keys.append(v[0])
        n_dict[v[0]] = v[1]
    return (n_keys,n_dict)

if not os.path.isdir('build'):
    os.mkdir('build')

days = {}

def getDay(day:int):
    data = getJson(f'https://api.comm.miui.com/calendar/festival/v2/detail?id={day}')
    #print(data)
    date = datetime.datetime.fromtimestamp(data['data']['second'])
    date_str = date.strftime('%Y-%m-%d')
    name = data['data']['name']
    info = data['data']['description']
    out = {
        'date': date_str,
        'name': name,
        'info': info
        }
    days[date_str]=out
    return out

for i in range(0,500):
    print(f'-->id={i}')
    try:
        print(getDay(i))
    except:
        print('Null')

_,output = sortDict(days)

with open('build/days.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(output))
    f.close()


#getDay(200)

print(f'http_count->{http_count}')
