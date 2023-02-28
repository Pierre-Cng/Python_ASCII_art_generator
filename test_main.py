import pytest
import asciiart
import numpy as np
from pathlib import Path

@pytest.mark.parametrize('args', [('test_path', 'test_ratio', 'test_output_name', 'test_precise', 'test_separator')])
def test_parser(args, monkeypatch):
    monkeypatch.setattr('sys.argv', ['py -m asciiart.py', args[0], args[1], args[2], args[3], args[4]])
    assert asciiart.parser().image_path==args[0]
    assert asciiart.parser().ratio== args[1]
    assert asciiart.parser().output_name == args[2]
    assert asciiart.parser().precise == args[3]
    assert asciiart.parser().separator == args[4]

@pytest.fixture(scope='function', autouse=True)
def setup_teardown():
    print('**********Setup**********')
    yield
    print('**********Teardown**********')

@pytest.mark.parametrize('precise, expected', [(False, r' .:-=+*#%@'),
                        (True,r'`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$')])
def test_greyscale_precision(precise, expected):
    obj = asciiart.Asciiart()
    obj.precise = precise
    assert obj.greyscale_precision == expected

@pytest.mark.parametrize('precise, expected', [(False, 25.5), (True, 3.8059701492537314)])
def test_brightness_weight(precise, expected):
    obj = asciiart.Asciiart()
    obj.precise = precise
    assert obj.brightness_weight == expected

@pytest.mark.parametrize('path', ['image.png'])
def test_get_image(path):
    obj = asciiart.Asciiart()
    obj.get_image(path)
    obj.image.verify()

@pytest.mark.parametrize('ratio', [0.1])
def test_rescale(ratio):
    obj = asciiart.Asciiart()
    obj.get_image('image.png')
    obj.rescale(ratio)
    assert obj.resized_image.size == tuple(int(ratio * elem) for elem in obj.image.size)

@pytest.mark.parametrize('', [''])
def test_image_to_array():
    obj = asciiart.Asciiart()
    obj.get_image('image.png')
    obj.rescale()
    obj.image_to_array()
    assert obj.image_array.dtype.type is np.str_
    assert obj.image_array.shape == (obj.image.size[1], obj.image.size[0])

# @pytest.mark.parametrize('', [''])
def test_save_as_txt():
    obj = asciiart.Asciiart()
    obj.get_image('image.png')
    obj.rescale()
    obj.image_to_array()
    obj.save_as_txt()
    #check if text data correspond to array?
    assert Path('out_file.txt').is_file()

# ************* function to finish: *************

# @pytest.mark.parametrize('', [''])
# def test_create_new_image():

# @pytest.mark.parametrize('', [''])
# def test_data_from_text():

# @pytest.mark.parametrize('', [''])
# def test_resize():

# @pytest.mark.parametrize('', [''])
# def test_save_as_png():

# @pytest.mark.parametrize('', [''])
# def test_save():

# @pytest.mark.parametrize('', [''])
# def test_convert_to_ascii():

# @pytest.mark.parametrize('', [''])
# def test_main():
