# Picture capture

#-- include('examples/showgrabbox.py')--#
import sys
sys.path.append('D:\\GitRepo\\PyStock')
from common_stock.stock_helper import CodeTools


def capture_choice_code():
    import pyscreenshot
    im=pyscreenshot.grab(bbox=(1430,90,1538,120)) # X1,Y1,X2,Y2
    # im.show()

    try:
        import Image
    except ImportError:
        from PIL import Image
    import pytesseract

    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
    tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'

    val = pytesseract.image_to_string(im, lang='eng', config=tessdata_dir_config)
    return val

def open_xue_qiu(code):
    assert len(code) == 6
    print(code)
    code = CodeTools.to_sina_code(code)
    # https://xueqiu.com/S/SZ000710
    url = f'https://xueqiu.com/S/{code}'
    import webbrowser
    webbrowser.open(url)  # Go to example.com
    pass

def main():
    code = capture_choice_code()
    open_xue_qiu(code)


if __name__ == '__main__':
    main()


