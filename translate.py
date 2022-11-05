import requests,time
from fastlid import fastlid
text=''
# while text!="quit":
#     text=input("请输入你要翻译的内容：")
#     lang=fastlid(text)
#     if lang=="zh":
#         from_lang,to_lang="zh","en"
#     elif lang=="en":
#         from_lang,to_lang="en","zh"
#     else:
#         from_lang=lang[0]
#         to_lang="zh"
#     data = [text,from_lang,to_lang]
#     json_data = {"data": data }
#     start=time.time()
#     url = "https://hf.space/embed/mikeee/gradio-deepl/+/api/predict"
#     resp = requests.post(url,json=json_data)
#     trans=resp.json()
#     end=time.time()
#     total= end-start
#     print(f"译文：{trans['data'][0]}\n用时:{total}")
def translate(text,from_lang="en",to_lang="zh"):
    data = [text,from_lang,to_lang]
    json_data = {"data": data }
    start=time.time()
    url = "https://hf.space/embed/mikeee/gradio-deepl/+/api/predict"
    resp = requests.post(url,json=json_data)
    trans=resp.json()
    end=time.time()
    total= end-start
    print(f"译文：{trans['data'][0]}\n用时:{total}")