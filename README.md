# TelegaGraph

## Добавлена возможность печати фотографий / Added the ability to print photos 

[![Видео](https://img.youtube.com/vi/DN97YGAF-z0/maxresdefault.jpg)](https://youtu.be/DN97YGAF-z0)

Бот для телеграм, который распечатывает сообщения на термопринтере.
Использовался ESP32 с Micropython 1.14. Термопринтер подключен к UART2 (tx=17, rx=16).

### Подключение
Пины rx, tx, gnd от принтера соединяем с пинами 17, 16, gnd на esp32 соответственно. 

### Настройка
В модуль esp32 необходимо прошить прошивку micropython 1.14 (на ней тестировалось). Прошивка и как прошивать - здесь https://micropython.org/download/esp32/
Регистрируете своего бота в телеграм у бота @BotFather. Получаете токен. Вставляете токен в файле main.py вместо API-KEY. В файле boot.py вводите данные своего wi-fi. Там три значения в словаре, но можете оставить одно со своим (просто я переношу свой девайс в разные места, где разные точки доступа)
Загружаете все файлы (boot.py, api.py, qr204.py, main.py) в esp32, перезагружаете и всё должно заработать.

Bot for Telegram, which prints messages on the thermal printer.
I used ESP32 with Micropython 1.14. The thermal printer is connected to UART2 (tx=17, rx=16).

### Connection
Pins rx, tx, gnd from the printer are connected to pins 17, 16, gnd on esp32, respectively. 

### Settings
The esp32 module must be flashed with micropython 1.14 firmware (tested on it). Firmware and how to flash you can here https://micropython.org/download/esp32/
Register your bot in telegram with @BotFather bot. Get bot token. Insert the token in the main.py file instead of the API-KEY. In the boot.py file, enter your wi-fi details. There are three meanings in the dictionary, but you can leave obly one with yours (I just move my device to different places where there are different access points)
Upoad all files (boot.py, api.py, qr204.py, main.py) into esp32, reboot and everything should work. 
