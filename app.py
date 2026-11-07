from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Salut ! comment tu t'appelle."

@app.route('/contact')
def contact():
    return "Contactez-moi à l'adresse email : exemple@mail.com"

if __name__ == '__main__':
    app.run(port=5000)
