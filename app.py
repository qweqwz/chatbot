from flask import Flask, escape, request,render_template

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/write')
def write():
    return render_template('write.html')

@app.route('/send')
def send():
    user_input=request.args.get('user_input')

if __name__ == '__main__':
    app.run(debug=True)