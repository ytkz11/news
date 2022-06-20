# test.py
# coding: utf-8
import feedparser
import requests
from extractcontent3 import ExtractContent
from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.simple_tokenizer import SimpleTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor
import time, threading
import re, datetime, os
from translate import translate

extractor = ExtractContent()
opt = {"threshold": 50}
extractor.set_option(opt)

def getSummary(text):
    # Object of automatic summarization.
    auto_abstractor = AutoAbstractor()
    # Set tokenizer.
    auto_abstractor.tokenizable_doc = SimpleTokenizer()
    # Set delimiter for making a list of sentence.
    auto_abstractor.delimiter_list = [". ", ".\n", "\n"]
    # Object of abstracting and filtering document.
    abstractable_doc = TopNRankAbstractor()
    # Summarize document.
    result_dict = auto_abstractor.summarize(text, abstractable_doc)

    # Output result.
    out_text = ''

    dic_len = len(result_dict["summarize_result"])
    if dic_len > 10:
        dic_len = 10
    for i in range(dic_len):
        out_text += result_dict["summarize_result"][i]
    return out_text


def getBody(link, txtname):
    try:
        proxies = {'http': 'socks5h://127.0.0.1:7890',
                   'https': 'socks5h://127.0.0.1:7890'
                   }

        res = requests.get(link, timeout=30, proxies=proxies)
        extractor.analyse(res.text)
        text, title = extractor.as_text()
        title = re.sub('[-|:|\||\[|\(|\{].*', '', title)
        text = re.sub('&.*?;', '', text)
        text = getSummary(text)
        title_translate = translate(title)
        text_translate = translate(text)
        print('===================================================')
        print('title:' + title_translate)
        print('===================================================')
        print('body :' + text_translate.replace('. ', '.\n'))
        # print('===================================================')
        text_translate = text_translate.replace('.', '')
        if len(title_translate) > 7 and len(text_translate) > 100:
            with open(txtname,'a+') as f:
                f.write('===================================================')
                f.write('\n')
                f.write(title_translate)
                f.write('---------------------------------------------------')
                f.write('\n')
                f.write(text_translate)
                # f.write('____________________________________________________')
                f.write('\n')
                f.write('\n')
    except Exception as e:
        print(e)


def getTECHNOLOGYRss():
    # BUSINESS TECHNOLOGY
    rssUrl = 'https://news.google.com/news/rss/headlines/section/topic/TECHNOLOGY'
    rssLang = '?hl=en-US&gl=US&ceid=US:en'
    feed = feedparser.parse(rssUrl + rssLang)
    outpath = r'D:\dengkaiyuan\txt'
    txtname = os.path.join(outpath, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + 'Technology.md')
    for entry in feed.entries:
        link = entry.get('link')
        getBody(link, txtname)
def getBUSINESSRss():
    # BUSINESS TECHNOLOGY
    rssUrl = 'https://news.google.com/news/rss/headlines/section/topic/BUSINESS'
    rssLang = '?hl=en-US&gl=US&ceid=US:en'
    feed = feedparser.parse(rssUrl + rssLang)
    outpath = r'D:\dengkaiyuan\txt'
    txtname = os.path.join(outpath, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + 'Business.md')
    for entry in feed.entries:
        link = entry.get('link')
        getBody(link, txtname)

def main():
    t1 = threading.Thread(target=getTECHNOLOGYRss)
    t2 = threading.Thread(target=getBUSINESSRss)
    t1.start()
    t2.start()
if __name__ == '__main__':
    main()
