import sys
import socket

from HTMLParser import HTMLParser
from urlparse import urlparse, urljoin

#

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global srcs
        
        if tag not in ('img', 'script'): return
        for attr in attrs:
            if attr[0] == 'src':
                srcs.append(attr[1])

#

def loadContentsAndSave(sock, result):  # web page 내의 object를 하나씩 불러온 다음 저장하는 함수
    sendmsg = template.format(host=result.netloc, path=result.path, connection='close')

    sock.send(sendmsg)
            
    getmsg = ''  # getmsg: http 요청 후의 응답 메시지

    while True:
        received = sock.recv(1024)
        getmsg = getmsg + received

        print 'loading...', len(received), 'got.'
            
        if len(received) < 1024:  # '1024 미만' 이라는 것은 더 이상 받을 데이터가 없다는 뜻이므로 loop를 빠져 나옴
            break

    headers, obj = getmsg.split('\r\n\r\n')  # headers, obj: http response 내의 header 및 object(body)

    i = len(result.path)-1
    file_name = ''
    
    while i >= 0:  # file name을 알아낸 다음 그대로 저장함
        if result.path[i:i+1] == '/':
            file_name = result.path[i+1:]
            break
        
        i = i-1

    with open(file_name, "wb") as code:
        code.write(obj)

    return obj

#

print 'Welcome to 2017 CN Assignment #3 !!'

base_url = raw_input('Enter URL: ')

if base_url == '.':
    print 'See you next time~'
    sys.exit(1)

template = '''GET {path} HTTP/1.1\r
Host: {host}\r
Connection: {connection}\r
\r
'''

parseResult = urlparse(base_url)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((parseResult.netloc, 80))

HTMLCode = loadContentsAndSave(sock, parseResult)  # HTMLCode: 웹 페이지 내의 소스 코드

print "A web page loaded."
sock.close()

srcs = []

parser = MyHTMLParser()
parser.feed(HTMLCode)

for i in range(0,len(srcs)):
    url = urljoin(base_url, srcs[i])
    result = urlparse(url)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((result.netloc, 80))

    loadContentsAndSave(sock, result)

    print "An object loaded."
    sock.close()

print 'See you next time~'
