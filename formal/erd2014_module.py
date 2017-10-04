import urllib.request,socket,ast,re,urllib.parse,random

def search_form_db(key):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 12345))
    sock.send(key.encode(encoding='UTF-8'))
    try:
        result = ast.literal_eval(sock.recv(1048576).decode('utf-8'))
    except:
        result = []
    sock.close()
    return result

def search_form_db2(key):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 12345))
    sock.send(key.encode(encoding='UTF-8'))
    try:
        result = sock.recv(1048576).decode('utf-8')
    except:
        result = ''
    sock.close()
    return result

def segment(query):
    query_split = query.split(' ')#這裡假設所有query都沒有標點符號，只有空格隔開
    segment = {}
    tt = 0
    for i in range(len(query_split)):
        if i >= tt:
            current_name = ''
            tmp_name = ''
            tmp_result = []
            for j in range(len(query_split[i:])):
                current_name = current_name + query_split[i:][j] + ' '    
                search_result = search_form_db(current_name[:-1])
                if search_result != []:
                    tmp_name = current_name[:-1]
                    tmp_result = search_result  
                    tt = j+i+1  
            if tmp_name!='' and tmp_result!=[]:
                segment.update({tmp_name:tmp_result})
            else:
                segment.update({query_split[i]:['0']})
    return segment

def chang_seg_result_to_dic(seg):
    seg2={}
    for entity in seg:
        seg2.update({entity:{}})
        for candidate in seg[entity]:
            seg2[entity].update({candidate:0})
    return seg2

def stop_list():#build stop word list , 記得stop_word.txt每行最後都要換行
    stop_word = open('stop_word2.txt','r',encoding='utf-8')
    stops = []
    for line in stop_word:
        stops.append(line[:-1])
    stop_word.close()
    return stops

def download_from_wiki(seg):
    for entity in seg:  
        for candidate in seg[entity]:
            if candidate != '0'and candidate != '-1':
                try:
                    wiki_page = urllib.request.urlopen("http://en.wikipedia.org/wiki/" + search_form_db2(candidate)).read()
                    f = open('./page/'+candidate[3:],'w',encoding='utf-8')
                    f.write(wiki_page.decode("utf-8"))
                    print("http://en.wikipedia.org/wiki/" + search_form_db2(candidate))
                    f.close()
                except:
                    print("Cant download : http://en.wikipedia.org/wiki/" + search_form_db2(candidate))

def inter_search_for_each_other_wiki_link_in_wiki_page(seg):
    for entity in seg:
        for candidate in seg[entity]:
            flag = 0
            try:
                wiki_page = open('./page/'+candidate[3:],'r',encoding='utf-8')
                flag = 1
            except:
                do = 'nothing'
            if flag == 1:
                link_file = open('./page/l_'+candidate[3:],'w',encoding='utf-8')
                for line in wiki_page:
                    for entity2 in seg:
                        if entity != entity2:
                            for candidate2 in seg[entity2]:  
                                if candidate2 != '0' and candidate2 != '-1':
                                    if "/wiki/" + search_form_db2(candidate2) in line:
                                        link_file.write(candidate2+'\n')
                link_file.close()


def write_ans(seg,file):
    f = open('./ans/'+file,'w',encoding='utf-8')
    for entity in seg:
        max_candidate = ''
        max_score = -1
        for candidate in seg[entity]:
            if max_score < seg[entity][candidate]:
                max_candidate = candidate
                max_score = seg[entity][candidate]
        f.write(max_candidate+'	'+entity+'\n')
    f.close()
