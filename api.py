import time
import json
import socket


class TelegramBot(object):

    def __init__(self, token, bot_url='api.telegram.org', img_url=''):
        self.token = token
        self.kbd = {'keyboard': [], 'resize_keyboard': True, 'one_time_keyboard': True}
        self.upd = {'offset': 0, 'limit': 1, 'timeout': 30, 'allowed_updates': ['message']}

        self.addr = [(socket.getaddrinfo(bot_url, 443)[0][-1], bot_url)]
        if img_url:
            self.addr.append((socket.getaddrinfo(img_url, 443)[0][-1], img_url))

    def request(self, path, data='{}', url=0):
        r = None
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            import ssl
            s.connect(self.addr[url][0])
            s = ssl.wrap_socket(s)

            s.write('POST /bot{}/{} HTTP/1.0\r\n'.format(self.token, path).encode())
            s.write('Host: {}\r\n'.format(self.addr[url][1]).encode())
            s.write(b'Content-Type: application/json\r\n')
            s.write('Content-Length: {}\r\n'.format(len(data)).encode())
            s.write(b'\r\n')
            s.write(data)

            while s.readline() != b'\r\n':
                continue

            if url == 0:
                r = s.read()
            else:
                d = s.read(1024)
                if d:
                    with open('data.bin', 'wb') as fd:
                        while d:
                            fd.write(d)
                            d = s.read(1024)

        except Exception as e:
            print(e)
        finally:
            s.close()

        return r

    def update(self):
        result = []
        try:
            r = self.request('getUpdates', json.dumps(self.upd).encode())
            jo = json.loads(r.decode())
        except Exception as e:
            print(e)
            return None

        if 'result' in jo and len(jo['result']) > 0:
            for item in jo['result']:
                if 'text' in item['message'] or 'photo' in item['message']:
                    sender = item['message']['from'].get('username', 'unknown')
                    title = item['message']['chat'].get('title')
                    if title:
                        sender = '{} | {}'.format(title, sender)

                    message = [item['message']['chat']['id'],
                               sender,
                               item['message'].get('text', ' '),
                               item['message']['date']]

                    if 'photo' in item['message'] and len(self.addr) > 1:
                        message[2] = item['message'].get('caption', '')
                        self.request(item['message']['photo'][-1]['file_id'],
                                     json.dumps(message).encode(), 1)

                    result.append(message)

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
