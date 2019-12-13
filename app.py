from flask import Flask, escape, request,render_template
from decouple import config
import requests
import random
from bs4 import BeautifulSoup
app = Flask(__name__)

api_url='https://api.telegram.org/bot'
token= config('TELEGRAM_BOT_TOKEN')
google_key=config('GOOGLE_TRANSLATE_TOKEN')

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/write')
def write():
    return render_template('write.html')

@app.route('/send')
def send():
    
    user_input=request.args.get('user_input')
    get_user_api = f"{api_url}{token}/getUpdates"
    res=requests.get(get_user_api).json()
    user_id=res['result'][0]['message']['from']['id']

    send_url=f'https://api.telegram.org/bot{token}/sendMessage?text={user_input}&chat_id={user_id}'
    requests.get(send_url)
    return render_template('send.html')

@app.route('/telegram',methods=['POST'])
def telegram():
    req=request.get_json()

    user_id =req['message']['from']['id']
    user_input =req['message']['text'] 

    if user_input=='로또':
        numbers=list(range(1,46))
        lucky=random.sample(numbers,6)
        sorted_lucky=sorted(lucky)
        return_data=sorted_lucky 


    elif user_input[0:3]=='번역 ':
        google_api_url="https://translation.googleapis.com/language/translate/v2"
        before_text=user_input[3:]

        data={
            'q': before_text,
            'source':'ko',
            'target': 'en',
        }
        request_url = f'{google_api_url}?key={google_key}'

        res=requests.post(request_url,data).json()
        # print(res)
        return_data=res['data']['translations'][0]['translatedText']

    # elif user_input=='노래순위':
    #     url_music='https://www.melon.com/chart/index.htm'
    #     music_html=requests.get(url_music).text
    #     soup=BeautifulSoup(music_html,'html.parser')
    #     lst50=soup.find_all('tr',{'class':'lst50'})
    #     music_rank=[]
    #     # for i in range(0,5):
    #     music_title=lst50[1].find('div',{'class':'ellipsis rank01'})
    #     music_singer=lst50[1].find('div',{'class':'ellipsis rank02'})
    #     music_rank.append(music_title+' - '+music_singer)
    #     return_data=music_rank





    else:
        return_data = "지금 사용 가능한 명령어는 로또입니다."
    send_url=f'https://api.telegram.org/bot{token}/sendMessage?text={return_data}&chat_id={user_id}'
    requests.get(send_url)
    # print(request.get_json())
    return 'ok', 200

if __name__ == '__main__':
    app.run(debug=True)