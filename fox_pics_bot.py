import httpx
import time


API_URL = 'https://api.telegram.org/bot'
API_FOX_URL = 'https://randomfox.ca/floof/'
BOT_TOKEN = '7274875670:AAHD2swgWpB308UVqg3xEht_-yFBgnYgBy4'
TEXT = 'Here be potatoes and dragons!'
FOX_TEXT = 'Why, catch some fox!'
ERROR_TEXT = 'Не пришла картинка с лисом :('
MAX_COUNTER = 100

offset = -2
counter = 0
cat_response: httpx.Response
cat_link: str


while counter < MAX_COUNTER:

    print('attempt =', counter)
    updates = httpx.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            fox_response = httpx.get(API_FOX_URL)
            if fox_response.status_code == 200:
                fox_link = fox_response.json()['link']
                httpx.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={FOX_TEXT}')
                httpx.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={fox_link}')
            else:
                httpx.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')

    time.sleep(1)
    counter += 1
