from flask import Flask, request, Response
from erd2014_module import *
import re

def remove_stop_word(seg, stops):
    seg2 = {}
    for entity in seg:
        if entity not in stops:
            seg2.update({entity: seg[entity].copy()})
        else:
            seg2.update({entity: {}})
    return seg2

def by_wiki_title(seg):
    seg2 = {}
    for entity in seg:
        seg2.update({entity:{}})
        for candidate in seg[entity]:
            seg2[entity].update({candidate:seg[entity][candidate]})
            title = search_form_db("tbtbt"+candidate).lower()
            title = title.replace('_',':')
            title_split = re.findall(r"[\w']+",title)
            for context in seg:
                if entity != context:
                    flag = True
                    for context_seg in re.findall(r"[\w']+",context):
                        if context_seg not in title_split:
                            flag = False
                    if flag == True and len(context) >= 4:
                        try:
                            text = int(context)
                            seg2[entity].update({candidate:seg2[entity][candidate]+1})
                        except:
                            do = 'nothing'
                        

    return seg2

def tagme_delete(seg, query):
    tagme_result = tagme_api(query)
    seg2 = {}
    for entity in seg:
        seg2.update({entity: {}})
        for candidate in seg[entity]:
            if candidate in tagme_result or seg[entity][candidate] > 0:
                seg2[entity].update({candidate: seg[entity][candidate]})
                if candidate in tagme_result:
                    seg2[entity].update({candidate: seg2[entity][candidate]+tagme_result[candidate]})
    return seg2

app = Flask(__name__)
@app.route('/', methods=['POST'])
def short_text():
        textID = request.form['TextID']
        Text = request.form['Text']

        seg = segment(Text)
        seg_dic = chang_seg_result_to_dic(seg)
        seg_stop = remove_stop_word(seg_dic, stops)
        seg_title = by_wiki_title(seg_stop)
        seg_tagme = tagme_delete(seg_title, Text)

        response = ""
        for entity in seg_tagme:
            tmp_score = 0
            tmp_string = ''
            for candidate in seg_tagme[entity]:
                if seg_tagme[entity][candidate] >= tmp_score:
                    tmp_string = textID + '	' + '0' + '	' + candidate + '	' + entity + '	' + '1' + '\n'
                    tmp_score = seg_tagme[entity][candidate]
            response = response + tmp_string

        '''
        response = ""
        for entity in seg_tagme:
            for candidate in seg_tagme[entity]:
                response = response + textID + '	' + '0' + '	' + candidate + '	' + entity + '	' + '1' + '\n'
    '''
        return Response(response, mimetype='text/plain')
    
if __name__ == '__main__':
    stops = stop_list()
    app.run(host='1.34.137.2')
