import random
import textwrap
from io import BytesIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 


class ThermoImage(object):

    def __init__(self, image, width=384):
        self.image = Image.open(BytesIO(image))
        if self.image.width > self.image.height:
            self.image = self.image.transpose(Image.ROTATE_90)
        new_height = int(width * self.image.height / self.image.width)
        self.image = self.image.resize((width, new_height), Image.LANCZOS)

    def instagram(self, name='ThermoImage', comment=''):
        font_bold = ImageFont.truetype('fonts/opensans-bold.ttf', 16)
        font_light = ImageFont.truetype('fonts/opensans-light.ttf', 16)
        instagram_line = Image.open('images/instagram_line.jpg')
        comment_lines = textwrap.wrap(comment, width=40)
        line_height = font_light.getsize(name)[1]
        
        height = [self.image.height, instagram_line.height]
        height.append(line_height * 3)
        height.append(line_height * len(comment_lines))
        
        _image = Image.new('RGB', (self.image.width, sum(height)), (255, 255, 255))
        _image.paste(self.image, (0, 0))
        _image.paste(instagram_line, (0, self.image.height))
        
        pos_y = self.image.height +  instagram_line.height + 5
        draw = ImageDraw.Draw(_image)
        draw.text((15, pos_y), f'{random.randint(100, 1000)} отметок "Нравится"', 0, font=font_bold)
        
        pos_y += line_height
        draw.text((15, pos_y), name, 0, font=font_bold)
        
        pos_y += line_height
        for line in comment_lines:
            draw.text((15, pos_y), line, 0, font=font_light)
            pos_y += line_height
        
        self.image = _image
        return self.image
    
    @property
    def binary(self):
        _image = list(self.image.convert('1').getdata())
        result = bytearray()
        for i in range(0, len(_image), 8):
            result.append(int(''.join(['1' if i==0 else '0' for i in _image[i: i+8]]), 2))
        return bytes(result)