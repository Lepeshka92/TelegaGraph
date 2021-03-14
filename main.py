import gc
import os
import time
import machine
import api
import qr204


gc.enable()

# Для того, чтобы печатались фото нужно указать адрес сайта в img_url
# lepeshka.pythonanywhere.com указан для примера и проверки работы
# 
#tg = api.TelegramBot('API-KEY',
#                     img_url='lepeshka.pythonanywhere.com')

tg = api.TelegramBot('API-KEY')
printer = qr204.QR204(machine.UART(2, 9600, tx=17, rx=16))

def convert_time(s):
    date = time.gmtime(s - 946674000)
    fmt = '{:04}/{:02}/{:02} {:02}:{:02}'
    return fmt.format(*date[:5])

def message_handler(messages):
    for message in messages:
        if message[2] == '/start':
            tg.send(message[0], 'This bot prints messages to thermal printer')
        elif message[2] == '/info':
            tg.send(message[0], 'My IP: ' + sta_if.ifconfig()[0])
        else:
            printer.awake()
            if not printer.paper():
                tg.send(message[0], 'No paper')
            else:
                printer.font_b()
                printer.write('Sender: ')
                printer.write(message[1])
                printer.newline(1)
                printer.write('Date: ')
                printer.write(convert_time(message[3]))
                printer.newline(1)
                
                printer.font_a()
                printer.bold_enbl()
                printer.write('_ ' * 16)
                printer.bold_dsbl()
                printer.newline(1)
                if 'data.bin' in os.listdir():
                    printer.print_image()
                    os.remove('data.bin')
                else:
                    printer.write(message[2])
                    printer.newline(1)
                    printer.bold_enbl()
                    printer.write('_ ' * 16)
                    printer.bold_dsbl()
                    printer.newline()
            printer.sleep()

printer.sleep()
tg.listen(message_handler)
