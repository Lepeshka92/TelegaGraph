import urequests as requests
import ujson as json


class TelegramBot:
    
    def __init__(self, token):
        self.token = token
        self.offset = 0
        self._url = 'https://api.telegram.org/bot' + token

    def send(self, chat_id, text):
        data = 'chat_id={}&text={}'.format(chat_id, text)
        url = self._url + '/sendMessage?' + data.replace(' ', '%20')
        
        try:
            requests.get(url)
            return True
        except:
            return False

    def update(self):
        data = 'timeout=30&limit=1&offset=' + str(self.offset)
        url = self._url + '/getUpdates?' + data
        
        try:
            r = requests.get(url)
            jo = json.loads(r.text)
        except:
            return None
            
        if len(jo['result']) > 0:
            self.offset = jo['result'][0]['update_id'] + 1
            if 'text' in jo['result'][0]['message']:
                return (jo['result'][0]['message']['chat']['id'],
                        str(jo['result'][0]['message']['from']['first_name']),
                        str(jo['result'][0]['message']['text']))
        
        return None

    def listen(self, handler):
        while True:
            message = self.update()
            if message:
                handler(message)


