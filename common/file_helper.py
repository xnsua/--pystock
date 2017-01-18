from pathlib import Path


def save_bin_to_file(filename: str, b: bytes):
    with open(filename, 'wb') as file:
        file.write(b)
    return


def save_string_to_file(filecontent: str, filename: str):
    Path(filename).write_text(filecontent, 'utf-8')


def read_string_from_file(filename: str):
    return Path(filename).read_text(encoding='utf-8')


if __name__ == '__main__':
    content = '我们'
    file_name = 'testfile.text'
    save_string_to_file(file_name, content)
    contentread = read_string_from_file(file_name)
    assert contentread == content
