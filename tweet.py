import tweepy

Consumer_key = 'gV9rrGZhUbU1QCujMPhYxCGVD'
Consumer_secret = 'rPNQCr0pwWRyUKRSuZSQZ2PVd1SkfRIoNlZbmqY5RVw7wyKfjn'
Access_token = '154103818-fe4tV19Khef68fKO3KRfypbFtHQSBQW1rHOWumbG'
Access_secret = 'fUoAAVVGgxHU2ENZC5ZbG9AgA2s57qjYKbPAoD6mbV2IN'

# OAuth認証
auth = tweepy.OAuthHandler(Consumer_key, Consumer_secret)
auth.set_access_token(Access_token, Access_secret)
api = tweepy.API(auth)

#ツイート取得
data = []

#最大200*pages件のツイートを取得するためのページ
pages = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

for page in pages:
    results = api.user_timeline(screen_name="Kurihiroooooo", count=200, page=page)#twitterのuserid指定
    for r in results:
    #r.textで、投稿の本文のみ取得する
        data.append(r.text)

line = ''.join(data)
with open("text.txt", 'wt') as f:
    f.write(line)

#テスト
results = api.user_timeline(screen_name="Kurihiroooooo", count=200, page=1)
for r in results:
    #r.textで、投稿の本文のみ取得する
    print(r)
    print("-------------------------------------")
    print(r.text)
    print("-------------------------------------")

    #必要モジュール
import requests
import json
import copy

#取得した文字列データを辞書型に変換する
import ast


#テキスト分析用情報

text_analytics_base_url = "https://kuri-text-analytics.cognitiveservices.azure.com/"
sentiment_api_url = text_analytics_base_url + "text/analytics/v3.0/languages"
subscription_key = "44fa217b94d2474e8b8cce68d7e1f1c1"

azure_json = ""
results = api.user_timeline(screen_name="Kurihiroooooo", count=200, page=1)
for num, result in enumerate(results):
    azure_json_single = str({'id': num,\
                             'language':'ja',\
                             'text':result.text\
                            })
    azure_json += azure_json_single + ','
    
#最後だけカンマ抜く
azure_json=azure_json[:-1]
azure_json = "{'documents' : ["+ azure_json+"]}"                      

#辞書型に変換し、typeの確認
azure_json = ast.literal_eval(azure_json)
type(azure_json)

#HTTPリクエスト処理で、分析結果を取得
headers = {"Ocp-Apim-Subscription-Key": subscription_key}
response = requests.post(sentiment_api_url, headers=headers, json=azure_json)
sentiments = response.json()
print(sentiments)

#取得結果をソートする
posi_sort = copy.copy(sentiments['documents'])
posi_sort.sort(key=lambda x: x['detectedLanguage']['confidenceScore'], reverse=True)

print(posi_sort[0]['detectedLanguage']['confidenceScore'])
print("------------------")
print(posi_sort[-1]['detectedLanguage']['confidenceScore'])