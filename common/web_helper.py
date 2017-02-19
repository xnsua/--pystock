import datetime

import requests
import requests_cache
from pyquery import PyQuery

requests_cache.install_cache('demo_cache', expire_after=datetime.timedelta(days=1))


def url_to_pyquery(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }
    rep = requests.get(url, timeout=5, headers=headers)

    py = PyQuery(rep.content)
    return py


def firefox_get_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }
    response = requests.get(url, timeout=5, headers=headers)
    return response


def firefox_download_file(url, filepath):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)


def main():
    # firefox_download_file('http://quotes.money.163.com/service/chddata.html?code=1000001&start=19910102&end=20170214&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP', 'jqtt.down')
    pass


if __name__ == '__main__':
    main()
