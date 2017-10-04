import urllib.request,socket,ast,urllib.parse

def search_form_db(key):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 12345))
    sock.send(key.encode(encoding='UTF-8'))
    if key[:5] == "wikww" or key[:5] == "tbtbt":
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

def segment(query):
    query_split = query.split(' ')
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
                segment.update({query_split[i]:[]})
    return segment

def chang_seg_result_to_dic(seg):
    seg2={}
    for entity in seg:
        seg2.update({entity:{}})
        for candidate in seg[entity]:
            seg2[entity].update({candidate:0})
    return seg2

def stop_list():
    stop_word = open('stop_word.txt','r',encoding='utf-8')
    stops = []
    for line in stop_word:
        stops.append(line[:-1])
    stop_word.close()
    return stops

def tagme_api(query):
    url = r'http://tagme.di.unipi.it/tag'
    data = {
                'text':query
                ,'key':'Yen-PIN-ChIU.2014.tw'
    }
    freebase_id_tageme_found = {}
    try:
        s = urllib.request.urlopen(url, bytes(urllib.parse.urlencode(data),'UTF-8'))   
        for annotation in ast.literal_eval(s.read().decode(encoding='UTF-8'))['annotations']:
            if float(annotation['rho']) > 0.1:
                freebase_id_found = search_form_db("wikww"+str(annotation['id']))
                if freebase_id_found != '':
                    freebase_id_tageme_found.update({freebase_id_found:float(annotation['rho'])})
    except:
        do = 'nothing'
    return freebase_id_tageme_found





    
    

