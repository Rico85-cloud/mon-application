from flask import Flask, request
import os
import requests
import base64

app = Flask(__name__)

# CONFIGURATION GITHUB (Remplissez avec vos informations)
GITHUB_USER = "Rico85-cloud"  # <-- Mettez votre vrai pseudo GitHub ici !
GITHUB_REPO = "mon-application"
FICHIER_PATH = "messages.txt"

TOKEN = os.environ.get("GITHUB_TOKEN")
URL_API = f"https://github.com{GITHUB_USER}/{GITHUB_REPO}/contents/{FICHIER_PATH}"

MENU = """
<nav style="background-color: #f0f0f0; padding: 10px; margin-bottom: 20px; font-family: sans-serif;">
    <a href="/" style="margin-right: 15px; text-decoration: none; color: #007bff; font-weight: bold;">Accueil</a>
    <a href="/livredor" style="text-decoration: none; color: #007bff; font-weight: bold;">Livre d'or Permanent</a>
</nav>
"""

def lire_messages_depuis_github():
    if not TOKEN:
        return ["Erreur : Clé GITHUB_TOKEN manquante dans Render."]
    
    headers = {"Authorization": f"token {TOKEN}"}
    reponse = requests.get(URL_API, headers=headers)
    
    if reponse.status_code == 200:
        donnees = reponse.json()
        contenu_decode = base64.b64decode(donnees['content']).decode('utf-8')
        return [l.strip() for l in contenu_decode.split("\n") if l.strip()]
    return ["Bienvenue sur mon livre d'or permanent ! Laissez le premier message."]

def sauvegarder_sur_github(nouveau_msg):
    if not TOKEN: 
        return
    headers = {"Authorization": f"token {TOKEN}"}
    
    reponse = requests.get(URL_API, headers=headers)
    sha = ""
    contenu_actuel = ""
    
    if reponse.status_code == 200:
        donnees = reponse.json()
        sha = donnees['sha']
        contenu_actuel = base64.b64decode(donnees['content']).decode('utf-8')
    
    nouveau_contenu = contenu_actuel + nouveau_msg + "\n"
    contenu_encode = base64.b64encode(nouveau_contenu.encode('utf-8')).decode('utf-8')
    
    payload = {
        "message": "Nouveau message dans le livre d'or",
        "content": contenu_encode
    }
    if sha:
        payload["sha"] = sha
        
    requests.put(URL_API, headers=headers, json=payload)

@app.route('/')
def hello():
    return MENU + "<h1>Accueil</h1><p>Allez sur le livre d'or pour tester la sauvegarde gratuite sans disque !</p>"

@app.route('/livredor', methods=['GET', 'POST'])
def livredor():
    if request.method == 'POST':
        message_visiteur = request.form.get('message')
        if message_visiteur:
            sauvegarder_sur_github(message_visiteur.replace("\n", " "))

    tous_les_messages = lire_messages_depuis_github()

    formulaire_html = """
    <h1>Livre d'or 100% Gratuit</h1>
    <form method="POST" style="font-family: sans-serif; margin-bottom: 30px;">
        <textarea name="message" rows="4" cols="50" placeholder="Votre message sauvegardé sur GitHub..." required style="padding: 10px; border-radius: 5px; border: 1px solid #ccc;"></textarea>
        <br><br>
        <button type="submit" style="background-color: #28a745; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold;">Enregistrer</button>
    </form>
    """

    liste_messages_html = "<h3>Messages :</h3><ul>"
    for msg in reversed(tous_les_messages):
        liste_messages_html += f"<li style='margin-bottom: 10px; font-family: sans-serif;'>{msg}</li>"
    liste_messages_html += "</ul>"

    return MENU + formulaire_html + liste_messages_html

if __name__ == '__main__':
    app.run(port=5000)
