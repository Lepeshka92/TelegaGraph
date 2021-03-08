import time
import json
import socket


class TelegramBot(object):
    
    def __init__(self, token):
        self.addr = None
        self.token = token
        self.kbd = {'keyboard': [], 'resize_keyboard': True, 'one_time_keyboard': True}
        self.upd = {'offset': 0, 'limit': 1, 'timeout': 30, 'allowed_updates': ['message']}

    def request(self, path, data):
        if not self.addr:
            self.addr = socket.getaddrinfo('api.telegram.org', 443)[0][-1]
        
        r = None
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            import ssl
            s.connect(self.addr)
            s = ssl.wrap_socket(s)
            
            s.write('POST /bot{}/{} HTTP/1.0\r\n'.format(self.token, path).encode())
            s.write(b'Host: api.telegram.org\r\n')
            s.write(b'Content-Type: application/json\r\n')
            s.write('Content-Length: {}\r\n'.format(len(data)).encode())
            s.write(b'\r\n')
            s.write(data)
            
            while s.readline() != b'\r\n':
                continue
            r = s.read().decode()
        except Exception as e:
            print(e)
        finally:
            s.close()
        
        return r
    
    def update(self):
        result = []
        try:
            r = self.request('getUpdates', json.dumps(self.upd).encode())
            jo = json.loads(r)
        except Exception as e:
            print(e)
            return None
        if 'result' in jo:
            for item in jo['result']:
                if 'text' in item['message']:
                    if 'username' not in item['message']['chat']:
                        item['message']['chat']['username'] = 'notset'
                    result.append((item['message']['chat']['id'],
                                   item['message']['chat']['username'],
                                   item['message']['text'],
                                   item['message']['date']))
        if len(result) > 0:
            self.upd['offset'] = jo['result'][-1]['update_id'] + 1
        
        return result
    
    def send(self, chat_id, text, keyboard=None):
        data = {'chat_id': chat_id, 'text': text}
        if keyboard:
            self.kbd['keyboard'] = keyboard
            data['reply_markup'] = json.dumps(self.kbd)
        try:
            self.request('sendMessage', json.dumps(data).encode())
        except Exception as e:
            print(e)
            
    def listen(self, handler):
        while True:
            messages = self.update()
            if messages:
                handler(messages)
            time.sleep(3)
