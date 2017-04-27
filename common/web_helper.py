import datetime

import requests
import requests_cache

session_cache_one_day = requests_cache.CachedSession(
    'session_cache_one_day', expire_after=datetime.timedelta(days=1))

session_nocache = requests.session()


def firefox_get_url(session, url, headers={}):
    agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }
    headers = {**agent, **headers}
    response = session.get(url, timeout=5, headers=headers)
    return response


def firefox_quick_get_url(url, headers={}):
    return firefox_get_url(session_nocache, url, headers)


def firefox_quick_download_file(url, filepath, headers={}):
    return firefox_download_file(session_nocache, url, filepath, headers)


def firefox_download_file(session, url, filepath, headers_={}):
    r = session.get(url, headers=headers_, stream=True)
    if r.status_code == 200:
        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)


def main():
    firefox_download_file(requests.Session(),
                          'http://quotes.money.163.com/service/chddata.html?code=1000001&start=19910102&end=20170214&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP',
                          'jqtt.down')
    pass


if __name__ == '__main__':
    main()
