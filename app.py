from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Salut ! coucou."

if __name__ == '__main__':
    app.run(port=5000)
