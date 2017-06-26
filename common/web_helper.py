import datetime

import requests
import requests_cache

session_nocache = requests.session()
# toch
session_nocache = session_cache_one_day = requests_cache.CachedSession(
    'session_cache_one_day', expire_after=datetime.timedelta(days=1))

def firefox_get_url(session, url, headers=None, timeout=5):
    if headers is None:
        headers = {}
    agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }
    headers = {**agent, **headers}
    response = session.get(url, timeout=timeout, headers=headers)
    return response


def firefox_quick_get_url(url, headers=None, timeout=5):
    if headers is None:
        headers = {}
    return firefox_get_url(session_nocache, url, headers, timeout=timeout)


def firefox_quick_download_file(url, file_path, headers=None):
    if headers is None:
        headers = {}
    return firefox_download_file(session_nocache, url, file_path, headers)


def firefox_download_file(session, url, file_path, headers_=None):
    if headers_ is None:
        headers_ = {}
    r = session.get(url, headers=headers_, stream=True)
    if r.status_code == 200:
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)


def main():
    pass


if __name__ == '__main__':
    main()
