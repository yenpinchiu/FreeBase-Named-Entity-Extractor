import urllib.request
import urllib.parse
import os
import ast
import urllib.request,socket,ast,urllib.parse

def search_form_db(key):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 12345))
    sock.send(key.encode(encoding='UTF-8'))
    if key[:5] == "wikww" or "kblgp":
        try:
            result = sock.recv(1048576).decode('utf-8')
        except:
            result = ''
    else:
        try:
            result = ast.literal_eval(sock.recv(1048576).decode('utf-8'))
        except:
            result = []
    sock.close()
    return result

url = r'http://spotlight.dbpedia.org/rest/annotate/'


data = {
    'text':"youtube destinys child soldier",
    'confidence': 0
}


s = urllib.request.urlopen(url, bytes(urllib.parse.urlencode(data),'UTF-8'))

for line in s:
    line = str(line)
    if "<Resource URI=" in line:
        print(line)
        line = line.replace('%','\\u00')
        dbp_url = line.split("\" support=")[0].split("<Resource URI=\"http://dbpedia.org/resource/")[1].encode(encoding='UTF-8').decode('unicode_escape').lower()
        print(search_form_db("kblgp"+str(dbp_url)))
    
#print(s.read().decode(encoding='UTF-8'))
