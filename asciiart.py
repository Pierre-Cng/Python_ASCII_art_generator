import argparse
from PIL import Image, ImageDraw
import numpy as np

def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('image_path', help='Path of the image you want to convert', nargs="?", default=None)
    parser.add_argument('ratio', help='Ratio to rescale the image and the result', nargs="?", default=1.0)
    parser.add_argument('output_name', help='Output name', nargs="?", default='out_file')
    parser.add_argument('precise', help='Boolean to choose between a precise grey scale and a less but shorter one', nargs="?", default=True)
    parser.add_argument('separator', help='Separator that can be added between each ascii character', nargs="?", default=' ')
    return parser.parse_args()

class Asciiart:
    def __init__(self, precise=True, separator=' '):
        self.precise = precise
        self.separator = separator
        self.image_path = 'image.png'
        self.image = None
        self.resized_image = None
        self.image_array = None

    @property
    def greyscale_precision(self):
        low_precision = r' .:-=+*#%@'
        high_precision = r"`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
        if self.precise:
            return high_precision
        else:
            return low_precision

    @property
    def brightness_weight(self):
        return 255 / len(self.greyscale_precision)

    def get_image(self, path=None):
        if path is None:
            path = self.image_path
        self.image = Image.open(path)

    def rescale(self, ratio=1.0):
        width, height = self.image.size
        width = int(width * ratio)
        height = int(height * ratio)
        self.resized_image = self.image.resize((width, height))

    def image_to_array(self):
        array = np.array(self.resized_image.convert('L')) // self.brightness_weight
        array = array.astype(int)
        array = array.astype(str)
        for value in range(len(self.greyscale_precision)):
            array[array == str(value)] = self.greyscale_precision[value]
        self.image_array = array

    def save_as_txt(self, output_name='out_file'):
        file = open(output_name + '.txt', 'w', encoding='utf-8')
        for row in self.image_array:
            for element in row:
                file.write(element + self.separator)
            file.write('\n')
        file.close()

    def create_new_image(self, color=(255, 255, 255)):
        width = (self.image_array.shape[1] * 2 * 6) + 10
        height = (self.image_array.shape[0] * 15) + 10
        return Image.new(mode='RGB', size=(width, height), color=color)

    def data_from_text(self, output_name):
        txt_file = open(output_name + '.txt', 'r')
        data = txt_file.read()
        txt_file.close()
        return data

    def resize(self, image, keep_ratio=True, width=None, height=None):
        w, h = image.size
        if keep_ratio:
            if width is None and height is None:
                width, height = w, h
            elif width is None:
                width = (height * w) // h
            elif height is None:
                height = (width * h) // w
        if not keep_ratio:
            if width is None:
                width = w
            if height is None:
                height = h
        return image.resize((width, height))

    def save_as_png(self, output_name='out_file', ratio=True, dimension=(None, None)):
        image = self.create_new_image()
        drawing = ImageDraw.Draw(image)
        data = self.data_from_text(output_name)
        font_color = (0, 0, 0)
        drawing.text((10, 10), data, fill=font_color)
        image = self.resize(image, ratio, dimension[0], dimension[1])
        image.save(output_name + '.png')

    def save(self, output_name='out_file'):
        self.save_as_txt(output_name)
        self.save_as_png(output_name)

    def convert_to_ascii(self, path=None, ratio=1.0, output_name='out_file'):
        self.get_image(path)
        self.rescale(ratio)
        self.image_to_array()
        self.save(output_name)

def main():
    args = parser()
    generator = Asciiart(args.precise, args.separator)
    generator.convert_to_ascii(path=args.image_path, ratio=args.ratio, output_name=args.output_name)
    print(generator.image_array.shape)

if __name__ == '__main__':
    main()
