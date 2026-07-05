#by niquetamadrew 888 wallet 
#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════╗
# ║        BLACK BERRY BETA - OSINT FRAMEWORK          ║
# ║               WALLET / 888                         ║
# ╚══════════════════════════════════════════════════════╝

import os
import sys
import time
import random
import string
import threading
from datetime import datetime
from config import AUTO_SAVE, DATA_DIR, MAX_RESULTS, TIMEOUT
from api_client import search_person
from utils import sauvegarder_fiche, afficher_resultat, export_csv, export_pdf

# ==========================================
# 1. MUSIQUE (Optionnelle)
# ==========================================
try:
    import pygame
    PYGAME_OK = True
except ImportError:
    PYGAME_OK = False

MUSIC_DIR = "music"
MUSIC_ON = False
music_thread = None
music_paused = False
current_track = ""
playlist = []

# ==========================================
# 2. COULEURS ET THEMES
# ==========================================
R = '\033[0;31m'
G = '\033[0;32m'
Y = '\033[1;33m'
B = '\033[0;34m'
C = '\033[0;36m'
P = '\033[0;35m'
W = '\033[0m'

USER_NAME = ""
THEME = "PURPLE"        # Thème par défaut
ANIMATION_ON = True     # Matrix rain au démarrage ?

# ==========================================
# 3. FONCTIONS MUSICALES (inchangées)
# ==========================================
def ensure_mixer_init():
    if PYGAME_OK and not pygame.mixer.get_init():
        pygame.mixer.init()

def update_playlist():
    global playlist
    playlist = []
    if os.path.exists(MUSIC_DIR):
        for f in os.listdir(MUSIC_DIR):
            if f.lower().endswith('.mp3'):
                playlist.append(f)
    return playlist

def jouer_morceau(track_path):
    global current_track
    if PYGAME_OK:
        ensure_mixer_init()
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.play()
        current_track = os.path.basename(track_path)

def play_random():
    update_playlist()
    if playlist:
        jouer_morceau(os.path.join(MUSIC_DIR, random.choice(playlist)))

def play_music_thread():
    global MUSIC_ON, music_paused
    ensure_mixer_init()
    while MUSIC_ON:
        if not pygame.mixer.music.get_busy() and not music_paused:
            play_random()
        time.sleep(0.5)
    pygame.mixer.music.stop()

def start_music():
    global MUSIC_ON, music_thread, music_paused
    if not PYGAME_OK:
        print(f"{R}[!] pygame non installé. pip install pygame{W}")
        return
    update_playlist()
    if not playlist:
        print(f"{R}[!] Aucun fichier mp3 dans '{MUSIC_DIR}/'{W}")
        return
    if not MUSIC_ON:
        MUSIC_ON = True
        music_paused = False
        music_thread = threading.Thread(target=play_music_thread, daemon=True)
        music_thread.start()
        print(f"\n{G}[✓] Musique lancée (playlist aléatoire){W}")
    else:
        MUSIC_ON = False
        if music_thread:
            music_thread.join(timeout=1)
        print(f"\n{G}[✓] Musique arrêtée{W}")

def pause_music():
    global music_paused
    if PYGAME_OK and MUSIC_ON:
        if music_paused:
            pygame.mixer.music.unpause()
            music_paused = False
            print(f"\n{G}[✓] Musique reprise{W}")
        else:
            pygame.mixer.music.pause()
            music_paused = True
            print(f"\n{Y}[!] Musique en pause{W}")

def next_music():
    if PYGAME_OK and MUSIC_ON:
        play_random()
        print(f"\n{G}[✓] Morceau suivant : {current_track}{W}")

def select_track():
    update_playlist()
    if not playlist:
        print(f"\n{R}[X] Aucune musique dans '{MUSIC_DIR}/'{W}")
        return
    print(f"\n{Y}┌── Playlist ({len(playlist)}) ──{W}")
    for i, t in enumerate(playlist, 1):
        print(f"  {C}[{i}]{W} {t}")
    try:
        choix = int(input(f"{Y}[?] Numéro du morceau (0 = retour) : {W}"))
        if choix == 0:
            return
        if 1 <= choix <= len(playlist):
            chemin = os.path.join(MUSIC_DIR, playlist[choix-1])
            if not os.path.exists(chemin):
                print(f"\n{R}[X] Fichier introuvable{W}")
                return
            jouer_morceau(chemin)
            if not MUSIC_ON:
                start_music()
            print(f"\n{G}[✓] Lecture de {playlist[choix-1]}{W}")
        else:
            print(f"\n{R}[X] Numéro invalide{W}")
    except ValueError:
        print(f"\n{R}[X] Entrée invalide{W}")

def music_status_line():
    if not PYGAME_OK:
        return ""
    if MUSIC_ON:
        if music_paused:
            return f"{Y}[PAUSE]{W} "
        else:
            return f"{G}[♪ {current_track[:20]}]{W} "
    else:
        return f"{R}[MUSIC OFF]{W} "

# ==========================================
# 4. EFFETS HACKER (Matrix rain + boot)
# ==========================================
def matrix_rain(duration=3):
    if not ANIMATION_ON:
        return
    os.system('clear')
    print("\033[40m")
    try:
        rows, cols = os.popen('stty size', 'r').read().split()
        rows, cols = int(rows), int(cols)
    except:
        rows, cols = 24, 80
    num_cols = max(1, cols // 2)
    drops = []
    for _ in range(num_cols):
        drops.append({
            'y': random.randint(-rows, -1),
            'speed': random.uniform(0.4, 1.2),
            'tail': random.randint(3, 12),
            'head_char': random.choice(string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?/\\")
        })
    end_time = time.time() + duration
    while time.time() < end_time:
        print("\033[H", end="")
        screen = [[' '] * num_cols for _ in range(rows)]
        for i, drop in enumerate(drops):
            y = int(drop['y'])
            for j in range(drop['tail']):
                row = y - j
                if 0 <= row < rows:
                    if j == 0:
                        screen[row][i] = f"\033[1;32m{drop['head_char']}\033[0m"
                    else:
                        shade = 22 + min(j, 10)
                        screen[row][i] = f"\033[38;5;{shade}m{random.choice(string.ascii_letters + string.digits)}\033[0m"
            drop['y'] += drop['speed']
            if drop['y'] - drop['tail'] > rows:
                drop['y'] = random.randint(-10, -1)
                drop['speed'] = random.uniform(0.4, 1.2)
                drop['tail'] = random.randint(3, 12)
                drop['head_char'] = random.choice(string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?/\\")
        for row in screen:
            print("".join(row))
        time.sleep(0.05)
    print("\033[0m")

def hacker_boot():
    """Écran de boot style hacker avec pourcentage."""
    os.system('clear')
    print(f"{G}Initialisation du système BLACK BERRY...{W}\n")
    modules = ["Kernel", "Network", "API", "UI", "Audio", "Security"]
    for i in range(1, 101):
        # Barre de progression
        bar = "█" * (i // 2) + "░" * (50 - i // 2)
        print(f"\r{G}[{bar}] {i}%{W}", end="")
        if i % 15 == 0 and i < 100:
            mod = random.choice(modules)
            print(f"\n{Y}[+] Chargement du module {mod}... OK{W}")
        time.sleep(random.uniform(0.02, 0.08))
    print(f"\n\n{G}✅ Système opérationnel. Lancement en cours...{W}")
    time.sleep(1)

# ==========================================
# 5. DEMANDE DU PRÉNOM
# ==========================================
def demander_prenom():
    global USER_NAME
    os.system('clear')
    print(f"""
{G}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         ██████╗ ██╗      █████╗  ██████╗██╗  ██╗          ║
║         ██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝          ║
║         ██████╔╝██║     ███████║██║     █████╔╝           ║
║         ██╔══██╗██║     ██╔══██║██║     ██╔═██╗           ║
║         ██████╔╝███████╗██║  ██║╚██████╗██║  ██╗          ║
║         ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝          ║
║                                                              ║
║         ██████╗ ███████╗██████╗ ██████╗ ██╗   ██╗          ║
║         ██╔══██╗██╔════╝██╔══██╗██╔══██╗╚██╗ ██╔╝          ║
║         ██████╔╝█████╗  ██████╔╝██████╔╝ ╚████╔╝           ║
║         ██╔══██╗██╔══╝  ██╔══██╗██╔══██╗  ╚██╔╝            ║
║         ██████╔╝███████╗██║  ██║██║  ██║   ██║             ║
║         ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{W}
""")
    USER_NAME = input(f"{G}[?] Entrez votre prénom : {W}").strip().upper()
    if not USER_NAME:
        USER_NAME = "USER"
    os.system('clear')
    print(f"""
{G}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           ✦ BONJOUR {USER_NAME} ✦                                ║
║           Bienvenue dans BLACK BERRY BETA                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{W}
""")
    time.sleep(2)

# ==========================================
# 6. SPLASH SCREEN (avec boot)
# ==========================================
def splash():
    global USER_NAME
    if ANIMATION_ON:
        matrix_rain(3)
        hacker_boot()
    demander_prenom()
    os.system('clear')
    print(f"""
{P}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    {C}██████╗ ██╗      █████╗  ██████╗██╗  ██╗{P}              ║
║    {C}██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝{P}              ║
║    {C}██████╔╝██║     ███████║██║     █████╔╝ {P}              ║
║    {C}██╔══██╗██║     ██╔══██║██║     ██╔═██╗ {P}              ║
║    {C}██████╔╝███████╗██║  ██║╚██████╗██║  ██╗{P}              ║
║    {C}╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝{P}              ║
║                                                              ║
║    {Y}██████╗ ███████╗██████╗ ██████╗ ██╗   ██╗{P}              ║
║    {Y}██╔══██╗██╔════╝██╔══██╗██╔══██╗╚██╗ ██╔╝{P}              ║
║    {Y}██████╔╝█████╗  ██████╔╝██████╔╝ ╚████╔╝ {P}              ║
║    {Y}██╔══██╗██╔══╝  ██╔══██╗██╔══██╗  ╚██╔╝  {P}              ║
║    {Y}██████╔╝███████╗██║  ██║██║  ██║   ██║   {P}              ║
║    {Y}╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   {P}              ║
║                                                              ║
║         {Y}╔═══ BLACK BERRY BETA ═══════════════════╗{P}           ║
║         {Y}║  {W}OSINT FRAMEWORK v2.0              {Y}║{P}           ║
║         {Y}║  {W}Créé le 04/07/2026                {Y}║{P}           ║
║         {Y}╚══════════════════════════════════════╝{P}           ║
║                                                              ║
║    {R}━━━━━━━━━━ CREDITS ━━━━━━━━━━━━{P}                        ║
║    {Y}👤 WALLET • 888{P}                                       ║
║    {C}💬 Discord : niquetamadrew{P}                              ║
║    {W}Version BETA — Créé le 04/07/2026{P}                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{W}
""")
    time.sleep(2.5)

# ==========================================
# 7. BANNIÈRE AVEC STATUT MUSIQUE
# ==========================================
def banner():
    os.system('clear')
    status = music_status_line()
    print(f"""
{P}╔══════════════════════════════════════════════════════════════╗
║  {Y}BLACK BERRY BETA {W}| {C}WALLET • 888 {W}| {G}Discord: niquetamadrew{P}        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║    {C}██████╗ ██╗      █████╗  ██████╗██╗  ██╗               ║
║    ██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝               ║
║    ██████╔╝██║     ███████║██║     █████╔╝                ║
║    ██╔══██╗██║     ██╔══██║██║     ██╔═██╗                ║
║    ██████╔╝███████╗██║  ██║╚██████╗██║  ██╗               ║
║    ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝               ║
║                                                              ║
║    {G}██████╗ ███████╗██████╗ ██████╗ ██╗   ██╗               ║
║    ██╔══██╗██╔════╝██╔══██╗██╔══██╗╚██╗ ██╔╝               ║
║    ██████╔╝█████╗  ██████╔╝██████╔╝ ╚████╔╝                ║
║    ██╔══██╗██╔══╝  ██╔══██╗██╔══██╗  ╚██╔╝                 ║
║    ██████╔╝███████╗██║  ██║██║  ██║   ██║                  ║
║    ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{status}
""")

# ==========================================
# 8. AFFICHAGE DES DONS
# ==========================================
def afficher_dons():
    os.system('clear')
    print(f"""
{P}╔══════════════════════════════════════════════════════════════╗
║  {Y}            💰 SOUTENIR BLACK BERRY OSINT 💰{P}              ║
╠══════════════════════════════════════════════════════════════╣
║  {W}Si le projet t'est utile, tu peux faire un don :{P}          ║
║                                                              ║
║  {C}Bitcoin (BTC){W}   : bc1qlyuhxmg0h8l9cac6usmeu9a4rlc4nkkwp3gsk7{P}  ║
║  {C}Ethereum (ETH){W}  : 0x205B39E0451F2ab6c14CE91e647de23A019cDA40{P}  ║
║  {C}Solana (SOL){W}    : D8L5L7dbbVwUMtu3zdKgqsR2LhydmoG3q1Z5NKT2F22e{P}  ║
║                                                              ║
║  {Y}Tous les dons servent à améliorer l'outil et payer les frais d'API.{P} ║
║                                                              ║
║  {G}Merci pour ton soutien ! 🙌{P}                             ║
╚══════════════════════════════════════════════════════════════╝{W}
""")
    input(f"\n{Y}[?] Appuie sur Entrée pour revenir au menu...{W}")

# ==========================================
# 9. NOUVEAU MENU PARAMÈTRES (avec couleurs et plus d'options)
# ==========================================
def parametres():
    global AUTO_SAVE, MAX_RESULTS, TIMEOUT, THEME, ANIMATION_ON
    while True:
        os.system('clear')
        print(f"""
{P}╔══════════════════════════════════════════════════════════════╗
║  {Y}                     ⚙️  PARAMÈTRES{P}                         ║
╠══════════════════════════════════════════════════════════════╣
║  {G}[1]{W}  Sauvegarde auto         : {G if AUTO_SAVE else R}{'ON' if AUTO_SAVE else 'OFF'}{W}          ║
║  {G}[2]{W}  Résultats max           : {Y}{MAX_RESULTS}{W}                       ║
║  {G}[3]{W}  Timeout (sec)           : {Y}{TIMEOUT}{W}                       ║
║  {G}[4]{W}  Thème                   : {P}{THEME}{W}                       ║
║  {G}[5]{W}  Animation Matrix        : {G if ANIMATION_ON else R}{'ON' if ANIMATION_ON else 'OFF'}{W}          ║
║  {G}[6]{W}  🗑️  Vider les archives{P}                                  ║
║  {R}[0]{W}  ↩️  RETOUR{P}                                          ║
╚══════════════════════════════════════════════════════════════╝{W}""")
        choix = input(f"{Y}[?] PARAMÈTRES > {W}").strip()
        if choix == '0':
            return
        elif choix == '1':
            AUTO_SAVE = not AUTO_SAVE
            print(f"\n{G}[✓] Sauvegarde auto : {'ON' if AUTO_SAVE else 'OFF'}{W}")
            input(f"\n{Y}[?] Appuie sur Entrée...{W}")
        elif choix == '2':
            try:
                val = int(input(f"{Y}[?] Résultats max (1-50) : {W}"))
                if 1 <= val <= 50:
                    MAX_RESULTS = val
                    print(f"\n{G}[✓] Résultats max : {MAX_RESULTS}{W}")
                else:
                    print(f"\n{R}[X] Entre 1 et 50{W}")
            except:
                print(f"\n{R}[X] Nombre invalide{W}")
            input(f"\n{Y}[?] Appuie sur Entrée...{W}")
        elif choix == '3':
            try:
                val = int(input(f"{Y}[?] Timeout secondes (5-30) : {W}"))
                if 5 <= val <= 30:
                    TIMEOUT = val
                    print(f"\n{G}[✓] Timeout : {TIMEOUT}s{W}")
                else:
                    print(f"\n{R}[X] Entre 5 et 30{W}")
            except:
                print(f"\n{R}[X] Nombre invalide{W}")
            input(f"\n{Y}[?] Appuie sur Entrée...{W}")
        elif choix == '4':
            print(f"\n{C}Thèmes disponibles : PURPLE, RED, GREEN, BLUE, MATRIX{W}")
            th = input(f"{Y}[?] Nouveau thème : {W}").strip().upper()
            if th in ["PURPLE", "RED", "GREEN", "BLUE", "MATRIX"]:
                THEME = th
                print(f"\n{G}[✓] Thème changé en {THEME}{W}")
                # On applique la couleur directement dans les messages (la variable P change)
                # Nous gérerons la couleur via des conditions dans les affichages, mais ici on le garde en mémoire.
            else:
                print(f"\n{R}[X] Thème invalide{W}")
            input(f"\n{Y}[?] Appuie sur Entrée...{W}")
        elif choix == '5':
            ANIMATION_ON = not ANIMATION_ON
            print(f"\n{G}[✓] Animation Matrix : {'ON' if ANIMATION_ON else 'OFF'}{W}")
            input(f"\n{Y}[?] Appuie sur Entrée...{W}")
        elif choix == '6':
            conf = input(f"{R}[!] Vider TOUTES les archives ? (OUI) : {W}")
            if conf.upper() == "OUI":
                for f in os.listdir(DATA_DIR):
                    os.remove(os.path.join(DATA_DIR, f))
                print(f"\n{G}[✓] Archives vidées{W}")
            else:
                print(f"\n{Y}[!] Annulé{W}")
            input(f"\n{Y}[?] Appuie sur Entrée...{W}")
        else:
            print(f"\n{R}[X] Option invalide{W}")
            input(f"\n{Y}[?] Appuie sur Entrée...{W}")

# ==========================================
# 10. MENU PRINCIPAL (avec option Dons)
# ==========================================
def menu_principal():
    while True:
        banner()
        print(f"""
{P}╔══════════════════════════════════════════════════════════════╗
║  {Y}                   MENU PRINCIPAL{P}                          ║
╠══════════════════════════════════════════════════════════════╣
║  {G}[1]{W}  📝 FICHE PERSO + RECHERCHE{P}                              ║
║  {G}[2]{W}  📂 ARCHIVES BLACK BERRY{P}                                 ║
║  {G}[3]{W}  ⚙️  PARAMETRES{P}                                         ║
║  {G}[4]{W}  👤 CREDITS{P}                                             ║
║  {G}[5]{W}  💰 DONS (Soutenir le projet){P}                           ║
║  {R}[0]{W}  QUITTER{P}                                               ║
║                                                              ║
║  {Y}[M]{W} Play/Stop  {Y}[P]{W} Pause  {Y}[N]{W} Suivant  {Y}[S]{W} Choisir morceau{P}    ║
╚══════════════════════════════════════════════════════════════╝{W}""")
        choix = input(f"{Y}[?] BLACK BERRY > {W}").strip().upper()
        if choix == '0':
            print("\n👋 Au revoir, revenez vite !")
            sys.exit(0)
        elif choix == '1':
            nouvelle_recherche()
        elif choix == '2':
            lister_fiches()
        elif choix == '3':
            parametres()
        elif choix == '4':
            credits()
        elif choix == '5':
            afficher_dons()
        elif choix == 'M':
            start_music()
            input("Appuyez sur Entrée pour continuer...")
        elif choix == 'P':
            pause_music()
            input("Appuyez sur Entrée pour continuer...")
        elif choix == 'N':
            next_music()
            input("Appuyez sur Entrée pour continuer...")
        elif choix == 'S':
            select_track()
            input("Appuyez sur Entrée pour continuer...")
        else:
            print("\n❌ Choix invalide.")
            input("Appuyez sur Entrée pour continuer...")

# ==========================================
# 11. FONCTIONS RECHERCHE ET GESTION FICHIERS (inchangées)
# ==========================================
def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def nouvelle_recherche():
    clear()
    print("=== NOUVELLE RECHERCHE ===\n")
    nom = input("Nom (vide pour ignorer) : ").strip()
    prenom = input("Prénom (vide pour ignorer) : ").strip()
    pseudo = input("Pseudo (vide pour ignorer) : ").strip()
    email = input("Email (vide pour ignorer) : ").strip()

    if not any([nom, prenom, pseudo, email]):
        print("❌ Vous devez fournir au moins un critère.")
        input("Appuyez sur Entrée...")
        return

    print("\n🔍 Recherche en cours...")
    resultats = search_person(
        nom_famille=nom if nom else None,
        prenom=prenom if prenom else None,
        pseudo=pseudo if pseudo else None,
        email=email if email else None
    )

    if not resultats:
        print("❌ Aucun résultat trouvé.")
        input("Appuyez sur Entrée...")
        return

    for i, res in enumerate(resultats, 1):
        afficher_resultat(res, i)

    if AUTO_SAVE:
        identite = {"nom": nom, "prenom": prenom}
        chemin = sauvegarder_fiche(identite, resultats, pseudo, email)
        print(f"\n✅ Fiche sauvegardée : {chemin}")
    else:
        print("\n⚠️  Sauvegarde automatique désactivée.")

    input("\nAppuyez sur Entrée pour continuer...")

def lister_fiches():
    import json
    clear()
    print("=== FICHES SAUVEGARDÉES ===\n")
    fichiers = [f for f in os.listdir(DATA_DIR) if f.endswith('.json')]
    if not fichiers:
        print("Aucune fiche.")
        input("Appuyez sur Entrée...")
        return
    for i, f in enumerate(fichiers, 1):
        chemin = os.path.join(DATA_DIR, f)
        try:
            with open(chemin, 'r', encoding='utf-8') as file:
                data = json.load(file)
            nom = data['identite'].get('nom', '?')
            prenom = data['identite'].get('prenom', '?')
            date = data.get('date', '')[:10]
            nb = len(data.get('resultats', []))
            print(f"{i}. {prenom} {nom} - {date} - {nb} résultats")
        except:
            print(f"{i}. {f}")
    print("\nEntrez le numéro d'une fiche pour la consulter, ou 0 pour revenir.")
    choix = input("> ").strip()
    if choix.isdigit() and int(choix) != 0:
        idx = int(choix) - 1
        if 0 <= idx < len(fichiers):
            consulter_fiche(os.path.join(DATA_DIR, fichiers[idx]))
        else:
            print("Numéro invalide.")
            input("Appuyez sur Entrée...")

def consulter_fiche(chemin):
    import json
    with open(chemin, 'r', encoding='utf-8') as f:
        data = json.load(f)
    clear()
    print(f"Fiche : {chemin}\n")
    print(f"Identité : {data['identite'].get('prenom','')} {data['identite'].get('nom','')}")
    print(f"Pseudo : {data.get('pseudo','')}")
    print(f"Email : {data.get('email','')}")
    print(f"Date : {data.get('date','')[:19]}")
    print("\nRésultats :")
    for i, res in enumerate(data.get('resultats', []), 1):
        afficher_resultat(res, i)
    input("\nAppuyez sur Entrée pour revenir...")

def credits():
    clear()
    print(f"""
{P}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    {Y}╔═══ BLACK BERRY BETA ═════════════════════╗{P}             ║
║    {Y}║  {W}OSINT FRAMEWORK v2.0              {Y}║{P}               ║
║    {Y}╚══════════════════════════════════════╝{P}               ║
║                                                              ║
║    {R}━━━━━━━━━━ CREDITS ━━━━━━━━━━━━{P}                        ║
║    {Y}👤 WALLET{P}                                             ║
║    {C}     Créateur • OSINT Specialist{P}                       ║
║    {C}     Discord : niquetamadrew{P}                           ║
║                                                              ║
║    {Y}👤 888{P}                                                ║
║    {C}     Créateur • Designer{P}                               ║
║    {C}     Discord : niquetamadrew{P}                           ║
║                                                              ║
║    {R}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{P}                 ║
║    {W}  BLACK BERRY • OSINT FRAMEWORK{P}                        ║
║    {W}  Version BETA — Créé le 04/07/2026{P}                    ║
║    {W}  © 2026 • Tous droits réservés{P}                        ║
║    {R}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{P}                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{W}
""")
    input("\nAppuyez sur Entrée pour revenir...")

# ==========================================
# 12. POINT D'ENTRÉE
# ==========================================
if __name__ == "__main__":
    splash()
    menu_principal()
