from flask import Flask, request
import os
import requests
import base64

app = Flask(__name__)

# CONFIGURATION DIRECTE GITHUB
TOKEN = os.environ.get("GITHUB_TOKEN")
URL_API = "https://github.com"

MENU = """
<nav style="background-color: #f0f0f0; padding: 10px; margin-bottom: 20px; font-family: sans-serif;">
    <a href="/" style="margin-right: 15px; text-decoration: none; color: #007bff; font-weight: bold;">Accueil</a>
    <a href="/livredor" style="text-decoration: none; color: #007bff; font-weight: bold;">Livre d'or Permanent</a>
</nav>
"""

def lire_messages_depuis_github():
    if not TOKEN:
        return ["Configuration incomplète : La clé GITHUB_TOKEN est introuvable dans Render."]
    
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Flask-Livre-Dor-Application"  # Ajout de l'identifiant pour GitHub
    }
    
    try:
        reponse = requests.get(URL_API, headers=headers, timeout=5)
        if reponse.status_code == 200:
            donnees = reponse.json()
            contenu_decode = base64.b64decode(donnees['content']).decode('utf-8')
            return [l.strip() for l in contenu_decode.split("\n") if l.strip()]
        elif reponse.status_code == 404:
            return ["Bienvenue ! Le fichier de sauvegarde va se créer lors du premier message."]
        elif reponse.status_code == 401:
            return ["Erreur d'authentification : Votre GITHUB_TOKEN n'est pas valide."]
        else:
            return [f"Erreur GitHub (Code {reponse.status_code}) : Problème d'accès."]
    except Exception as e:
        return [f"Impossible de joindre GitHub pour le moment : {str(e)}"]

def sauvegarder_sur_github(nouveau_msg):
    if not TOKEN: 
        return
    
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Flask-Livre-Dor-Application"
    }
    
    sha = ""
    contenu_actuel = ""
    
    try:
        reponse = requests.get(URL_API, headers=headers, timeout=5)
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
            
        requests.put(URL_API, headers=headers, json=payload, timeout=5)
    except Exception:
        pass

@app.route('/')
def hello():
    etat_token = "<span style='color:green;'>Configuration détectée !</span>" if TOKEN else "<span style='color:red;'>Clé GITHUB_TOKEN manquante dans Render.</span>"
    return MENU + f"<h1>Accueil</h1><p>Statut de la connexion : {etat_token}</p><p>Rendez-vous sur l'onglet Livre d'or pour tester.</p>"

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
