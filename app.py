from flask import Flask, request
app = Flask(__name__)

# Le menu de navigation
MENU = """
<nav style="background-color: #f0f0f0; padding: 10px; margin-bottom: 20px; font-family: sans-serif;">
    <a href="/" style="margin-right: 15px; text-decoration: none; color: #007bff; font-weight: bold;">Accueil</a>
    <a href="/apropos" style="margin-right: 15px; text-decoration: none; color: #007bff; font-weight: bold;">À propos</a>
    <a href="/contact" style="margin-right: 15px; text-decoration: none; color: #007bff; font-weight: bold;">Contact</a>
    <a href="/livredor" style="text-decoration: none; color: #007bff; font-weight: bold;">Livre d'or</a>
</nav>
"""

# Une liste temporaire pour stocker les messages dans la mémoire du serveur
MESSAGES_SAUVEGARDES = ["Super site ! Bravo.", "Bienvenue sur mon application."]

@app.route('/')
def hello():
    contenu = "<h1>Bienvenue sur mon site !</h1><p>Utilisez le menu pour naviguer et tester le formulaire.</p>"
    return MENU + contenu

@app.route('/apropos')
def apropos():
    contenu = "<h1>À propos</h1><p>Application Python créée pour apprendre le développement web.</p>"
    return MENU + contenu

@app.route('/contact')
def contact():
    contenu = "<h1>Contact</h1><p>Contactez-moi par email à : monadresse@exemple.com</p>"
    return MENU + contenu

# 4. NOUVELLE PAGE : Le Livre d'or avec le formulaire
@app.route('/livredor', methods=['GET', 'POST'])
def livredor():
    # Si le visiteur a validé le formulaire (méthode POST)
    if request.method == 'POST':
        message_visiteur = request.form.get('message')
        if message_visiteur: # On vérifie que le texte n'est pas vide
            MESSAGES_SAUVEGARDES.append(message_visiteur)

    # Création du formulaire HTML
    formulaire_html = """
    <h1>Livre d'or</h1>
    <p>Laissez-moi un petit mot ci-dessous :</p>
    <form method="POST" style="font-family: sans-serif; margin-bottom: 30px;">
        <textarea name="message" rows="4" cols="50" placeholder="Écrivez votre message ici..." required style="padding: 10px; border-radius: 5px; border: 1px solid #ccc;"></textarea>
        <br><br>
        <button type="submit" style="background-color: #28a745; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold;">Envoyer le message</button>
    </form>
    """

    # Affichage des messages sous le formulaire
    liste_messages_html = "<h3>Messages précédents :</h3><ul>"
    for msg in reversed(MESSAGES_SAUVEGARDES): # Du plus récent au plus ancien
        liste_messages_html += f"<li style='margin-bottom: 10px; font-family: sans-serif;'>{msg}</li>"
    liste_messages_html += "</ul>"

    return MENU + formulaire_html + liste_messages_html

if __name__ == '__main__':
    app.run(port=5000)
