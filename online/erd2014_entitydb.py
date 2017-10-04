import socket

f = open('join_2nd_2_hasno\'.tsv','r',encoding='utf-8')
f2 = open('wiki_id_fb_mid','r',encoding='utf-8')
f3 = open('entity_unicode_wiki_link.tsv','r',encoding='utf-8')

db = {}

for line in f:
        line_split = line[:-1].split("  ")
        try:
                db_key = line_split[1]
                if db_key not in db:
                        db.update({db_key:[]})
                db[db_key].append(line_split[0])
        except:
                do = 'nothing'

for line2 in f2:
        line2_split = line2[:-1].split('	')
        db.update({"wikww"+line2_split[0]:line2_split[1]})

for line3 in f3:
        line3_split = line3[:-1].split('	')
        db.update({"tbtbt"+line3_split[0]:line3_split[1]})

print('db start')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 12345))
sock.listen(5)

while True:
        (csock, adr) = sock.accept()
        msg = csock.recv(1024)
        if not msg:
                pass
        else:
                try:
                        csock.send(str(db[msg.decode('utf-8')]).encode(encoding='UTF-8'))
                except:
                        do = "nothing"
        csock.close()

