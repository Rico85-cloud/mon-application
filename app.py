from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Salut ! coucou."

@app.route('/contact')
def contact():
    return "Contactez-moi à l'adresse email : exemple@mail.com"


if __name__ == '__main__':
    app.run(port=5000)
