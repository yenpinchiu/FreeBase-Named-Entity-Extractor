f = open('stop_word2.txt','r',encoding='utf-8')
f2 = open('stop_word22.txt','w',encoding='utf-8')

for line in f:
    f2.write(line.replace('’',''))

f2.close()
f.close()

#要去'的  除了字典  還有stopword
