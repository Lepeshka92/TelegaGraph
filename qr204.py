import time


class QR204(object):

    _uart = None

    def __init__(self, uart):
        self._uart = uart
        self._uart.write(b"\xff\xff\xff")
        self._uart.write(b"\x1b\x76\x00")
        self._uart.write(b"\x1b\x40")
        self._uart.write(b"\x1b\x37")
        self._uart.write(b"\x07\x50\x02") # heating dots/heat time/heat interval
        self._uart.write(b"\x12\x23\xff")

    def newline(self, n=3):
        self._uart.write(b"\x0a" * n)

    def inverse_enbl(self):
        self._uart.write(b"\x1d\x42\x01")

    def inverse_dsbl(self):
        self._uart.write(b"\x1d\x42\x00")

    def bold_enbl(self):
        self._uart.write(b"\x1b\x45\x01")

    def bold_dsbl(self):
        self._uart.write(b"\x1b\x45\x00")

    def font_b(self):
        self._uart.write(b"\x1b\x21\x01")

    def font_a(self):
        self._uart.write(b"\x1b\x21\x00")

    def uline_enbl(self):
        self._uart.write(b"\x1b\x2d\x01")

    def uline_dsbl(self):
        self._uart.write(b"\x1b\x2d\x00")

    def align(self, arg="<"):
        if "<" in arg:
            self._uart.write(b"\x1b\x61\x00")
        elif ">" in arg:
            self._uart.write(b"\x1b\x61\x02")
        else:
            self._uart.write(b"\x1b\x61\x01")

    def sleep(self):
        self._uart.write(b"\x1b\x38\x01")

    def awake(self):
        self._uart.write(b"\xff\x1b\x76\x00")

    def write(self, text):
        self._uart.write(text.encode())

    def writeln(self, text):
        self.write(text)
        self.write("\n")

    def paper(self):
        self._uart.write(b"\x1b\x76\x00")
        res = 1
        for i in range(10):
            if self._uart.any() > 0:
                res = ord(self._uart.read(1)) & 4
                break
            time.sleep(0.1)
        return res == 0
    
    def print_image(self):
        self.newline(1)
        
        with open('data.bin', 'rb') as fd:
            line = fd.read(48)
            while line:
                self._uart.write(b'\x12\x2a\x01\x30')
                self._uart.write(line)
                line = fd.read(48)
        
        self.newline()
