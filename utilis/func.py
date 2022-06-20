#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# @Time : 2022/6/14 19:44 
# @Author : DKY
# @File : func.py

import requests
import json
import re
import time


def googleTranslate(text):
    """
        用谷歌翻译内容，返回翻译结果
        params: text 翻译的内容
        return: str s 翻译结果
    """

    url = 'https://translate.google.cn/_/TranslateWebserverUi/data/batchexecute?rpcids=MkEWBc&f.sid=-2984828793698248690&bl=boq_translate-webserver_20201221.17_p0&hl=zh-CN&soc-app=1&soc-platform=1&soc-device=1&_reqid=5445720&rt=c'
    headers = {
        'origin': 'https://translate.google.cn',
        'referer': 'https://translate.google.cn/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'x-client-data': 'CIW2yQEIpbbJAQjEtskBCKmdygEIrMfKAQj2x8oBCPfHygEItMvKAQihz8oBCNzVygEIi5nLAQjBnMsB',
        'Decoded': 'message ClientVariations {repeated int32 variation_id = [3300101, 3300133, 3300164, 3313321, 3318700, 3318774, 3318775, 3319220, 3319713, 3320540, 3329163, 3329601];}',
        'x-same-domain': '1'
    }  # 以防万一，我全加上了，可能有些不写也可以
    data = {
        'f.req': f'[[["MkEWBc","[[\\"{text}\\",\\"auto\\",\\"zh-CN\\",true],[null]]",null,"generic"]]]'
    }  # text则是你要翻译的内容
    proxies = {'http': 'socks5h://127.0.0.1:7890',
               'https': 'socks5h://127.0.0.1:7890'
               }
    res = requests.post(url, headers=headers, data=data, proxies=proxies).text  # 获取返回的结果
    pattern = '\)\]\}\'\s*\d{3,4}\s*\[(.*)\s*'  # 提取需要的部分
    part1 = re.findall(pattern, res)
    part1_list = json.loads(part1[0])  # 字符串转列表
    if part1_list[2] is None:  # 如果返回的结果中没有需要的数据，则返回输入的内容
        print(text)
        return text
    content1 = part1_list[2].replace('\n', '')
    part2_list = json.loads(content1)[1][0][0][5:][0]  # 过滤结果中重复的部分
    s = ''
    for i in part2_list:  # 遍历结果中的每一句话，并进行拼接
        s += i[0]
    print(s)
    return s


text = 'friend. Let us look back on 2020 and look forward to 2021.'
print(text)
googleTranslate(text)