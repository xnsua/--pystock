from datetime import datetime

print(datetime.now())


class tt:
    @classmethod
    def test(cls, content):
        return content


if __name__ == '__main__':
    a = [tt(), tt()]
    for i in a:
        i = 'a'
    print(a)
