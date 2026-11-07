from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Bonjour ! Mon application Python fonctionne sur Internet grâce à Render."

if __name__ == '__main__':
    app.run(port=5000)
