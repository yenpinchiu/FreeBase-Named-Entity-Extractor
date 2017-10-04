import os
from erd2014_module import *

#methods
def remove_stop_word(seg,stops): #把很可能是stop word的砍掉
    seg2 = {}
    for entity in seg:
        if entity not in stops:
            seg2.update({entity:seg[entity]})
        else:
            seg2.update({entity:{'-1':0}})
    return seg2

def by_wiki_title(seg): # 如果entity的wiki title裡有lengh > 3的 context word或其它entity，每有一個給一分
    seg2 = seg.copy()
    for entity in seg2:
        for candidate in seg2[entity]:
            if candidate != '0' and candidate != '-1':
                title = search_form_db2(candidate)
                title = title.replace('\'','')#title裡的'也砍掉不補空格
                title = title.replace('_',' ')#雖然wiki頁面的title沒底線，但是若直接用連接會很多底限當空白
                title_split = re.findall(r"[\w']+",title.lower())
                for entity2 in seg2:
                    if entity != entity2:
                        flag = True
                        for entity2_seg in re.findall(r"[\w']+",entity2):
                            if entity2_seg not in title_split:
                                flag = False
                        if flag == True and len(entity2) >= 4:
                            seg2[entity][candidate] += 1
    return seg2                            

def by_wiki_link(seg): # 如果有link在二個entity的wiki page之間，給他們各一分
    seg2 = seg.copy()    
    link_pool = []
    for entity in seg2:
        for candidate in seg2[entity]:
            flag = 0
            try:
                link_file = open('./page/l_'+candidate[3:],'r',encoding='utf-8')
                flag = 1
            except:
                do = 'nothing'
            if flag == 1:
                for line in link_file:
                    link_pool.append(candidate)
                    link_pool.append(line[:-1])
                    
    for entity in seg2:
        for candidate in seg2[entity]:
            if seg2[entity][candidate] == seg[entity][candidate] and candidate in link_pool:
                seg2[entity][candidate] += 1
    if link_pool != []:
        print("fuck")
    return seg2

def tagme_delete(seg):  #砍掉沒分數(沒有啥證據它是) 且tagme也沒找到的
    tag_result = open('tagme_result.txt','r',encoding='utf-8')
    tag_dic = []
    for line in tag_result:
        tag_dic.append(line[:-1].lower())#取小寫來比，tagme_resul.txt裡不見德是小寫

    seg2 = {}  
    for entity in seg:
        for candidate in seg[entity]:
            flag = 0
            try:
                wiki_page = open('./page/'+candidate[3:],'r',encoding='utf-8')
                flag = 1
            except:
                do = 'nothing'
            title = ''
            if flag == 1:
                for line in wiki_page:
                    if '<title>' in line:
                        title = line.split('<title>')[1].split('</title>')[0].split(' - Wikipedia')[0].lower()
                        break
            if title in tag_dic or seg[entity][candidate] > 0:
                if entity not in seg2:
                    seg2.update({entity:{}})
                seg2[entity].update({candidate:seg[entity][candidate]})
    return seg2

#run
stops = stop_list()
for subdir, dirs, files in os.walk('./data/'):
    for file in files:
        #print(file) 
        f = open('./data/'+file,'r',encoding='utf-8')
        for line in f:
            #print(file + ' ' + line)
            seg = segment(line)
            seg = chang_seg_result_to_dic(seg)
            seg = remove_stop_word(seg,stops)
            '''
            for entity in seg:
                try:
                    test = int(entity)
                    print(file + ' ' + line)
                    print(entity)
                except:
                    do = 'nothing'
            '''
            #download_from_wiki(seg)
            #inter_search_for_each_other_wiki_link_in_wiki_page(seg)
            #seg = by_wiki_link(seg)
            seg = by_wiki_title(seg)
            seg = tagme_delete(seg)
            print(seg)
            #print(seg)
            #write_ans(seg,file)
        f.close()
