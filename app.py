from flask import Flask
app = Flask(__name__)

# Un menu réutilisable sur toutes les pages pour éviter de répéter le code HTML
MENU = """
<nav style="background-color: #f0f0f0; padding: 10px; margin-bottom: 20px; font-family: sans-serif;">
    <a href="/" style="margin-right: 15px; text-decoration: none; color: #007bff; font-weight: bold;">Accueil</a>
    <a href="/apropos" style="margin-right: 15px; text-decoration: none; color: #007bff; font-weight: bold;">À propos</a>
    <a href="/contact" style="text-decoration: none; color: #007bff; font-weight: bold;">Contact</a>
</nav>
"""

# 1. Page d'accueil principale
@app.route('/')
def hello():
    contenu = "<h1>Bienvenue sur mon site !</h1><p>Cliquez sur le menu ci-dessus pour naviguer.</p>"
    return MENU + contenu

# 2. Page : À propos
@app.route('/apropos')
def apropos():
    contenu = "<h1>À propos</h1><p>Cette application a été créée pour apprendre le développement web et le déploiement cloud.</p>"
    return MENU + contenu

# 3. Page : Contact
@app.route('/contact')
def contact():
    contenu = "<h1>Contact</h1><p>Vous pouvez me contacter par email à : monadresse@exemple.com</p>"
    return MENU + contenu

if __name__ == '__main__':
    app.run(port=5000)
