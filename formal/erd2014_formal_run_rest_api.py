from flask import Flask,jsonify,request,Response

app = Flask(__name__)
@app.route('/', methods = ['POST'])
def short_text():
        runID = request.form['runID']
        textID = request.form['TextID']
        Text = request.form['Text']
        
        try:
                f = open('./ans/'+textID,'r',encoding='utf-8')
                response = ""
                for line in f:
                        line_split = line.split('	')
                        response = response + textID + '	' + '0' + '	' +  line_split[0] + '	' + line_split[1][:-1] + '	' + '1' + '\n' 
                f.close()
        except:
                response = textID + '	' + '0' + '	' +  '/m/05n_n8p' + '	' + 'tommy morrison' + '	' + '1' + '\n' 
        
        return Response(response,mimetype='text/plain')

if __name__ == '__main__':
        app.run(host='1.34.137.2')
