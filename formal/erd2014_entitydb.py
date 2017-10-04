import socket

f = open('join_2nd_2_hasno\'.tsv','r',encoding='utf-8')#join_xnd_2_hasno'.tsv 是名稱去除標點符號(若有標點符號則用空格隔開)的字典('則是直接砍掉，不補空格)(而_則有可能存在 但目測沒有)(freebase_id 對 名稱)
f2 = open('entity_unicode_wiki_link.tsv','r',encoding='utf-8')#把entity裡的wiki連結改成標準unicode後的字典(freebase_id 對 wiki連結) 
entities_db = {}
for line in f:
        line_split = line[:-1].split("  ")
        try:
                db_key = line_split[1]
        except:
                do = 'nothing'
        if db_key in entities_db:
                if line_split[0] not in entities_db[db_key]:
                        entities_db[db_key].append(line_split[0])
        else:
                entities_db.update({db_key:[]})
                entities_db[db_key].append(line_split[0])

for line2 in f2:
        line2_split = line2[:-1].split('	')
        entities_db.update({line2_split[0]:line2_split[1]})

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
                        csock.send(str(entities_db[msg.decode('utf-8')]).encode(encoding='UTF-8'))
                except:
                        do = "nothing"
        csock.close()

