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
from translate import translate_main
from bs4 import BeautifulSoup
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
        html = res.content.decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')
        images = soup.findAll('img')

        extractor.analyse(res.text)
        texts, title = extractor.as_text()
        title = re.sub('[-|:|\||\[|\(|\{].*', '', title)
        texts = re.sub('&.*?;', '', texts)
        texts = getSummary(texts)
        textpiecewise =texts.split('\n')  # 分割
        title_translate = translate_main(title)
        text_translate = ''
        try:
            for text in textpiecewise:
                if text!='':
                    text_translate = text_translate + translate_main(text)
        except:
            print('error')

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
                f.write('## ')
                f.write(title_translate)

                f.write('\n')
                f.write(text_translate)
                # f.write('____________________________________________________')
                f.write('\n')
                f.write('\n')
    except Exception as e:
        print(e)

def getRss(topic):
    # BUSINESS TECHNOLOGY
    rssUrl = 'https://news.google.com/news/rss/headlines/section/topic/'+topic
    rssLang = '?hl=en-US&gl=US&ceid=US:en'
    feed = feedparser.parse(rssUrl + rssLang)
    outpath = os.path.split(os.path.realpath(__file__))[0] + r'//archives'
    if os.path.exists(outpath)==0:
        os.makedirs(outpath)
    txtname = os.path.join(outpath, datetime.datetime.now().strftime("%Y-%m-%d") + topic+'.md')
    for entry in feed.entries:
        link = entry.get('link')
        getBody(link, txtname)
def main():
    t1 = threading.Thread(target=getRss('SCIENCE'))
    t2 = threading.Thread(target=getRss('WORLD'))
    t3 = threading.Thread(target=getRss('BUSINESS'))
    t4 = threading.Thread(target=getRss('TECHNOLOGY'))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
if __name__ == '__main__':
    main()
