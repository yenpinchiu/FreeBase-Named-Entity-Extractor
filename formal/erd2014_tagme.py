import urllib.request
import urllib.parse
import os
import ast

url = r'http://tagme.di.unipi.it/tag'
f2 = open('tagme_result.txt','w',encoding='utf-8')
for subdir, dirs, files in os.walk('./data/'):
    for file in files:
        print(file) 
        f = open('./data/'+file,'r',encoding='utf-8')
        for line in f:
            data = {
                'text':line
                ,'key':'Yen-PIN-ChIU.2014.tw'
            }
            s = urllib.request.urlopen(url, bytes(urllib.parse.urlencode(data),'UTF-8'))
            for annotation in ast.literal_eval(s.read().decode(encoding='UTF-8'))['annotations']:
                try:
                    wiki_page = urllib.request.urlopen("http://en.wikipedia.org/w/api.php?action=query&prop=info&pageids=" + str(annotation['id']) + "&inprop=url").read().decode('utf-8')
                    link = wiki_page.split('fullurl=&quot;<a href=\"')[1].split('\">')[0]
                    link = link.replace('%','\\u00')
                    link = link.encode(encoding='UTF-8').decode('unicode_escape')
                    print(link)
                    wiki_title = urllib.request.urlopen(link).read().decode('utf-8')
                    wiki_title = wiki_title.split('<title>')[1].split(' - Wikipedia, the free encyclopedia</title>')[0]
                    print(wiki_title)
                    f2.write(wiki_title+'\n')
                except:
                    do = 'nothing'
        f.close()
f2.close()