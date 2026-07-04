import csv
import json
import os
from datetime import datetime
from config import DATA_DIR

# Créer le dossier de données s'il n'existe pas
os.makedirs(DATA_DIR, exist_ok=True)

def sauvegarder_fiche(identite, resultats, pseudo="", email=""):
    """
    Sauvegarde une fiche de recherche au format JSON dans DATA_DIR.
    Retourne le chemin du fichier créé.
    """
    timestamp = datetime.now().isoformat()
    fiche = {
        "identite": identite,
        "pseudo": pseudo,
        "email": email,
        "date": timestamp,
        "resultats": resultats
    }
    nom_fichier = f"fiche_{identite.get('nom','inconnu')}_{identite.get('prenom','inconnu')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    chemin = os.path.join(DATA_DIR, nom_fichier)
    with open(chemin, 'w', encoding='utf-8') as f:
        json.dump(fiche, f, indent=2, ensure_ascii=False)
    return chemin

def afficher_resultat(item, num=1):
    """
    Affiche un résultat de manière lisible dans le terminal.
    """
    print(f"\n┌── Résultat #{num} ──")
    champs_principaux = [
        'nom_famille','prenom','pseudo','email','telephone','adresse',
        'ville','code_postal','pays','date_naissance','iban','phone',
        'societe','siret','bic','nir','mobile','civilite'
    ]
    for k in champs_principaux:
        if k in item and item[k] not in (None, ''):
            val = str(item[k])
            if len(val) > 55:
                val = val[:52] + "..."
            print(f"  {k:<18}: {val}")
    # Champs supplémentaires
    for k, v in item.items():
        if k not in champs_principaux and not k.startswith('_') and v not in (None, ''):
            vs = str(v)
            if len(vs) > 55:
                vs = vs[:52] + "..."
            print(f"  {k:<18}: {vs}")

def export_csv(fiche, filename=None):
    """
    Exporte les résultats en CSV.
    """
    if not fiche.get('resultats'):
        print("Aucun résultat à exporter.")
        return
    if not filename:
        filename = f"rapport_{fiche['identite']['nom']}_{fiche['identite']['prenom']}.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Récupérer tous les champs présents dans les résultats
        headers = set()
        for res in fiche['resultats']:
            headers.update(res.keys())
        headers = sorted([h for h in headers if not h.startswith('_')])
        writer.writerow(headers)
        for res in fiche['resultats']:
            row = [str(res.get(h, '')) for h in headers]
            writer.writerow(row)
    print(f"✅ CSV exporté : {filename}")

def export_pdf(fiche, filename=None):
    """
    Exporte les résultats en PDF (nécessite fpdf2).
    """
    try:
        from fpdf import FPDF
    except ImportError:
        print("❌ fpdf2 non installé. pip install fpdf2")
        return
    if not fiche.get('resultats'):
        print("Aucun résultat à exporter.")
        return
    if not filename:
        filename = f"rapport_{fiche['identite']['nom']}_{fiche['identite']['prenom']}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 20)
    pdf.cell(0, 15, "BLACKBERRY OSINT - Rapport", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.set_font("Helvetica", size=14)
    pdf.cell(0, 10, f"Fiche de {fiche['identite']['nom']} {fiche['identite']['prenom']}", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.cell(0, 10, f"Date: {fiche['date'][:19]}", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 10)
    pdf.cell(0, 7, "Résultats détaillés", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", size=9)
    for i, res in enumerate(fiche['resultats'], 1):
        pdf.cell(0, 7, f"--- Résultat #{i} ---", new_x="LMARGIN", new_y="NEXT")
        for k, v in res.items():
            if k.startswith('_'): continue
            txt = f"{k}: {str(v)[:60]}"
            pdf.multi_cell(0, 6, txt)
        pdf.ln(2)
    pdf.output(filename)
    print(f"✅ PDF exporté : {filename}")
