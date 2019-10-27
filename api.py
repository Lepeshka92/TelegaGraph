import time
import gc
import ujson
import urequests


class TelegramBot:
    
    def __init__(self, token):
        self.url = 'https://api.telegram.org/bot' + token

        self.kbd = {
            'keyboard': [],
            'resize_keyboard': True,
            'one_time_keyboard': True}

        self.upd = {
            'offset': 0,
            'limit': 1,
            'timeout': 30,
            'allowed_updates': ['message']}

    def send(self, chat_id, text, keyboard=None):
        data = {'chat_id': chat_id, 'text': text}
        if keyboard:
            self.kbd['keyboard'] = keyboard
            data['reply_markup'] = json.dumps(self.kbd)
        try:
            urequests.post(self.url + '/sendMessage', json=data)
        except:
            pass
        finally:
            gc.collect()

    def update(self):
        result = []
        try:
            jo = urequests.post(self.url + '/getUpdates', json=self.upd).json() 
        except:
            return None
        finally:
            gc.collect()
        if 'result' in jo:
            for item in jo['result']:
                if 'text' in item['message']:
                    if 'username' not in item['message']['chat']:
                        item['message']['chat']['username'] = 'notset'
                    result.append((item['message']['chat']['id'],
                                   item['message']['chat']['username'],
                                   item['message']['text']))
        if len(result) > 0:
            self.upd['offset'] = jo['result'][-1]['update_id'] + 1
            
        return result

    def listen(self, handler):
        while True:
            messages = self.update()
            if messages:
                handler(messages)
            time.sleep(3)
            gc.collect()
