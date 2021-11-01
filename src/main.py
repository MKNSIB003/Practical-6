from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "<p><h1>Tutorial 6 </h1><br> Sibusiso MKNSIB003<br> Khumodiatla MTLKHU004</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
