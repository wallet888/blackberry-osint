# BlackBerry OSINT
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Description** : BlackBerry OSINT - Outil de corrélation de données personnelles. Conçu pour la recherche éthique et les tests de conformité RGPD.  
**Contact** : Discord : `niquetamadrew`  

---
🔥 GUIDE D’INSTALLATION COMPLET – LINUX & CHROMEBOOK
Étape 0 – Ouvrir un terminal
Sur Linux : Ctrl+Alt+T

Sur Chromebook (mode Linux) : ouvrir l’appli "Terminal"

📥 Étape 1 – Télécharger le code
Option A – Avec Git (le plus simple)

bash
git clone https://github.com/wallet888/blackberry-osint.git
Si ça marche, tu vois un dossier blackberry-osint.

Option B – Si Git n’est pas installé
Va sur https://github.com/wallet888/blackberry-osint → clique sur "Code" → "Download ZIP". Décompresse le ZIP et ouvre un terminal dans le dossier décompressé.

📂 Étape 2 – Entrer dans le dossier
bash
cd blackberry-osint
Vérifie que tu es bien dedans :

bash
ls -la
Tu dois voir des fichiers comme : main.py, cli.py, requirements.txt, .env.example, config.py, api_client.py, utils.py.

🐍 Étape 3 – Créer un environnement virtuel
bash
python3 -m venv venv
(Ça crée un dossier venv qui contient une copie propre de Python.)

🔌 Étape 4 – Activer l’environnement virtuel
bash
source venv/bin/activate
Normalement, tu vois (venv) apparaître au début de la ligne de commande. Si ce n’est pas le cas, recommence.

📦 Étape 5 – Installer les dépendances
bash
pip install -r requirements.txt
Si une erreur apparaît (surtout avec pygame) :

Ouvre requirements.txt avec nano requirements.txt

Supprime la ligne pygame==2.5.0

Sauvegarde (Ctrl+O, Entrée, Ctrl+X)

Relance pip install -r requirements.txt

(Sur un Chromebook, pygame cause souvent des problèmes – cette étape l’élimine.)

🔑 Étape 6 – Configurer ta clé API BrixHub (obligatoire)
bash
cp .env.example .env
Puis ouvre le fichier .env :

bash
nano .env
Tu vois ce contenu :

text
BRIX_API_KEY=ta_cle_ici
BRIX_API_URL=https://api.brixhub.is/api/v1/search
Remplace ta_cle_ici par ta vraie clé API BrixHub.
(Si tu n’as pas de clé, va sur BrixHub pour en acheter une.)
Sauvegarde : Ctrl+O, Entrée – Quitte : Ctrl+X.

▶️ Étape 7 – Lancer le script
bash
python3 main.py
Tu vois :

Effet Matrix (pluie de caractères verts).

Demande de prénom.

Menu principal.

C’est bon, ça tourne !

🪟 POUR WINDOWS (version courte, adaptée)
Ouvre PowerShell ou Invité de commandes.

Télécharge le code :

cmd
git clone https://github.com/wallet888/blackberry-osint.git
cd blackberry-osint
Crée et active l’environnement virtuel :

cmd
python -m venv venv
venv\Scripts\activate
Installe les dépendances :

cmd
pip install -r requirements.txt
(Si python n’est pas reconnu, utilise py à la place.)

Configure .env :

cmd
copy .env.example .env
notepad .env
Mets ta clé, sauvegarde, ferme.

Lance :

cmd
python main.py
❓ QUE FAIRE SI UNE ÉTAPE COINCE ?
Problème	Solution
git : commande introuvable	Installe Git ou télécharge le ZIP (Option B).
python3 : commande introuvable	Installe Python : sudo apt install python3 python3-pip (Linux) / télécharge depuis python.org (Windows).
pip install échoue	Vérifie que (venv) est actif. Sinon, refais source venv/bin/activate.
nano : commande introuvable (Chromebook)	Utilise vim ou vi si présent, ou installe nano : sudo apt install nano.
ModuleNotFoundError: No module named 'dotenv'	Refais pip install -r requirements.txt (après avoir activé venv).
✅ RÉSUMÉ – LA COMMANDE ULTIME (mais pas magique)
Pour Linux / Chromebook :

bash
git clone https://github.com/wallet888/blackberry-osint.git
cd blackberry-osint
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env   # ← remplace ta_cle_ici par TA clé
python3 main.py
Pour Windows :

cmd
git clone https://github.com/wallet888/blackberry-osint.git
cd blackberry-osint
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
notepad .env   # ← remplace ta_cle_ici par TA clé
python main.py
Maintenant, tu peux coller ce guide dans ton README ou dans un fichier INSTALL.md – et même les débutants s’en sortiront. 😉

