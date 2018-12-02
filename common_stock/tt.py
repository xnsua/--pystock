
def capture_choice_code():
    import pyscreenshot
    im=pyscreenshot.grab(bbox=(194,124,258,654)) # X1,Y1,X2,Y2
    # im.show()
    # return

    try:
        import Image
    except ImportError:
        from PIL import Image
    import pytesseract

    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
    tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata" '\
                          'C:\\Program Files (x86)\\Tesseract-OCR\\tessdata\\configs\\digits'

    val = pytesseract.image_to_string(im, lang='eng', config=tessdata_dir_config)
    return val

def main():
    val = capture_choice_code()
    print(val)


if __name__ == '__main__':
    main()
