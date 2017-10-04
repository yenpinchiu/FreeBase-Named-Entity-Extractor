import os
from erd2014_module import *
from erd2014_api_server import *

stops = stop_list()
for subdir, dirs, files in os.walk('./data/'):
    for file in files:
        
        f = open('./data/'+file,'r',encoding='utf-8')
        for line in f:
            print(line)
            seg = segment(line)
            seg_dic = chang_seg_result_to_dic(seg)
            seg_stop = remove_stop_word(seg_dic, stops)
            seg_title = by_wiki_title(seg_stop)
            seg_tagme = tagme_delete(seg_title, line)
            print(seg_tagme)

            response = ""
            for entity in seg_tagme:
                tmp_score = 0
                tmp_string = ''
                for candidate in seg_tagme[entity]:
                    if seg_tagme[entity][candidate] >= tmp_score:
                        tmp_string = "textID" + '	' + '0' + '	' + candidate + '	' + entity + '	' + '1' + '\n'
                        tmp_score = seg_tagme[entity][candidate]
                response = response + tmp_string
            print(response)

            '''
            response = ""
            for entity in seg_tagme:
                for candidate in seg_tagme[entity]:
                    response = response + "textID" + '	' + '0' + '	' + candidate + '	' + entity + '	' + '1' + '\n'
            print(response)
            '''
        f.close()
