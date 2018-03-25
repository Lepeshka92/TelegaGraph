class QR204(object):


    _printer = None

    def __init__(self, uart):
        self._printer = uart
        self._printer.write(b'\x1b\x40')
        self._printer.write(b'\x1b\x37')
        self._printer.write(b'\x14\x96\x50')
        self._printer.write(b'\x12\x23\xff')
    
    def newline(self, n=3):
        self._printer.write(b'\x0a' * n)

    def inverse_enbl(self):
        self._printer.write(b'\x1d\x42\x01')
        
    def inverse_dsbl(self):
        self._printer.write(b'\x1d\x42\x00')

    def bold_enbl(self):
        self._printer.write(b'\x1b\x45\x01')
        
    def bold_dsbl(self):
        self._printer.write(b'\x1b\x45\x00')

    def font_b(self):
        self._printer.write(b'\x1b\x21\x01')
        
    def font_a(self):
        self._printer.write(b'\x1b\x21\x00')

    def uline_enbl(self):
        self._printer.write(b'\x1b\x2d\x01')
        
    def uline_dsbl(self):
        self._printer.write(b'\x1b\x2d\x00')

    def align(self, arg='<'):
        if '<' in arg:
            self._printer.write(b'\x1b\x61\x00')
        elif '>' in arg:
            self._printer.write(b'\x1b\x61\x02')
        else:
            self._printer.write(b'\x1b\x61\x01')

    def write(self, text):
        self._printer.write(text.encode())
        

'''Example

printer = QR204(port)

printer.uline_enbl()
printer.write('Underline')
printer.uline_dsbl()

printer.newline(1)

printer.bold_enbl()
printer.write('Bold')
printer.bold_dsbl()

printer.newline(1)

printer.inverse_enbl()
printer.write('Inverse')
printer.inverse_dsbl()

printer.newline(1)

printer.font_b()
printer.write('Font B')
printer.font_a()

printer.newline(3)
'''
