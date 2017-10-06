from ghost import Ghost

ghost = Ghost()
# url = 'http://www.baidu.com'
url = 'http://www.sse.com.cn/market/sseindex/indexlist/constlist/index.shtml?COMPANY_CODE=000001&INDEX_Code=000001'
with ghost.start() as session:
    page, extra_resources = session.open(url)
    session.show()
    try:
        session.wait_for(lambda: False, '', 3)
    except:
        pass
    assert page.http_status == 200
    session.open('http://www.baidu.com')
    print(session.content)
