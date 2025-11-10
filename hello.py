from flask import Flask

app =Flask(__name__)

@app.route("/gomma")

def hello_world():
		
	return "<tr> <th>Name</th> <th>date of upload</th> <th>size</th> <th>file_link</th></tr>"
	
	

if __name__ == '__main__':
    app.run(debug=True)
