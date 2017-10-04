import re

f = open('entity.tsv','r',encoding='utf-8')
f2 = open('entity_unicode_wiki_link.tsv','w',encoding='utf-8')
for line in f:
    line = line.split('	')
    line[2] = line[2].split('/')[3][:-2]
    line[2] = line[2].replace('$','\\u')
    try:
        f2.write(line[0]+'	'+line[2].encode(encoding='UTF-8').decode('unicode_escape')+'\n')
    except:
        print(line)
f2.close()
f.close()

f = open('join_2nd.tsv','r',encoding='utf-8')
f2 = open('join_2nd_2_hasno\'.tsv','w',encoding='utf-8')

for line in f:
    line_split = line.split('	')
    line_split2 = re.findall(r"[\w']+",line_split[1].lower())
    db_key = ""
    for term in line_split2[:-1]:
        db_key = db_key + ' ' + term
    f2.write(line_split[0].replace('\'','') + ' ' + db_key +'\n')
    
f2.close()
f.close()
