from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Salut ! Je m'appelle Eric, comment ça va."

if __name__ == '__main__':
    app.run(port=5000)
