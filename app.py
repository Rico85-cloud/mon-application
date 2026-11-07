from flask import Flask
app = Flask(__name__)

# 1. Votre page d'accueil principale
@app.route('/')
def hello():
    return "<h1>Bienvenue sur mon site !</h1><p>Mon application Python fonctionne sur Internet grâce à Render.</p>"

# 2. NOUVELLE PAGE : À propos
@app.route('/apropos')
def apropos():
    return "<h1>À propos</h1><p>Cette application a été créée pour apprendre le développement web et le déploiement cloud.</p>"

# 3. NOUVELLE PAGE : Contact
@app.route('/contact')
def contact():
    return "<h1>Contact</h1><p>Vous pouvez me contacter par email à : monadresse@exemple.com</p>"

if __name__ == '__main__':
    app.run(port=5000)
    
