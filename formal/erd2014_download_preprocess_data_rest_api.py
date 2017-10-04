from flask import Flask,jsonify,request,Response

app = Flask(__name__)
@app.route('/', methods = ['POST'])
def short_text():
        runID = request.form['runID']
        textID = request.form['TextID']
        Text = request.form['Text']
        
        f = open('./data/'+textID,'w')
        f.write(Text)#寫入不經任何處理的query
        f.close()
	
        response = textID + "	0	/m/047sxrj	nicki minaj	1\n"
        return Response(response,mimetype='text/plain')

if __name__ == '__main__':
        app.run(host='1.34.137.2')

