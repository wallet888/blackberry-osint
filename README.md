# BlackBerry OSINT
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Description** : BlackBerry OSINT - Outil de corrélation de données personnelles. Conçu pour la recherche éthique et les tests de conformité RGPD.  
**Contact** : Discord : `niquetamadrew`  

---
📘 GUIDE D'INSTALLATION POUR LINUX (et Chromebook)
Titre :
BlackBerry OSINT – Installation rapide (Linux / Chrome OS)

🔧 1. PRÉ-REQUIS
Avant de commencer, assure-toi d’avoir :

Python 3.8+ (vérifie avec python3 --version)

pip (vérifie avec pip3 --version)

Git (optionnel, pour cloner) ou simplement un navigateur pour télécharger le ZIP

📥 2. TÉLÉCHARGER LE CODE
Option A – Via Git (recommandé si tu as Git)

bash
git clone https://github.com/wallet888/blackberry-osint.git
cd blackberry-osint
Option B – Via ZIP (plus simple, sans login)

Va sur https://github.com/wallet888/blackberry-osint

Clique sur "Code" → "Download ZIP"

Décompresse le fichier et ouvre un terminal dans le dossier :

bash
unzip blackberry-osint-main.zip -d blackberry-osint
cd blackberry-osint
🐍 3. CRÉER L'ENVIRONNEMENT VIRTUEL (recommandé)
bash
python3 -m venv venv
source venv/bin/activate
(Quand tu vois (venv) devant ton prompt, c’est bon !)

📦 4. INSTALLER LES DÉPENDANCES
bash
pip install -r requirements.txt
🎉 Bonne nouvelle : Plus de pygame ! L’installation est 100% sans erreur sur Linux et Chromebook.

⚙️ 5. CONFIGURATION (optionnel)
Le script utilise l’API HaveIBeenPwned (gratuite). Pas besoin de clé API – c'est déjà configuré.

Si tu veux juste tester, lance-le directement :

bash :
python3 main.py

▶️ 6. LANCER LE TOOL
bash
python3 main.py

🧠 7. COMMENT FAIRE UNE RECHERCHE
Dans le menu, tape 1.

Remplis les champs. 

Valide, et les fuites connues s’afficheront.

Exemple de recherche :

text
Nom (vide pour ignorer) : 
Prénom (vide pour ignorer) : 
Pseudo (vide pour ignorer) : 
Email (vide pour ignorer) : toi@exemple.com
Le script affichera les fuites

❓ DÉPANNAGE RAPIDE
Problème	Solution
python3: command not found	Installe Python : sudo apt install python3 python3-pip
pip install -r requirements.txt échoue	Vérifie que tu es bien dans venv (le (venv) doit apparaître)
Recherche ne donne rien	Certains emails n’ont jamais fuité → c’est normal. Essaie avec un email connu (ex: le tien)
Veux-tu arrêter le script ?	Tape 0 dans le menu, ou fais Ctrl+C
🔥 RÉSUMÉ POUR TES POTES (commande unique)
S’ils veulent tout faire d’une traite :

bash
git clone https://github.com/wallet888/blackberry-osint.git
cd blackberry-osint
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
Et voilà ! C’est open-source, gratuit, et ça tourne sur n’importe  quel linux 
