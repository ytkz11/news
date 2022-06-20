import re
import html
from urllib import parse
import requests

GOOGLE_TRANSLATE_URL = 'http://translate.google.cn/m?q=%s&tl=%s&sl=%s'

def translate(text, to_language="zh-CN", text_language="en"):

    text = parse.quote(text)
    url = GOOGLE_TRANSLATE_URL % (text,to_language,text_language)
    proxies = {'http': 'socks5h://127.0.0.1:7890',
               'https': 'socks5h://127.0.0.1:7890'
               }
    response = requests.get(url, proxies=proxies)
    data = response.text
    expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
    result = re.findall(expr, data)
    if (len(result) == 0):
        return ""

    return html.unescape(result[0])

if __name__ == '__main__':
    print(translate("你吃饭了么?", "en","zh-CN")) #汉语转英语
    print(translate("你吃饭了么？", "ja","zh-CN")) #汉语转日语
    print(translate("about your situation", "zh-CN","en")) #英语转汉语