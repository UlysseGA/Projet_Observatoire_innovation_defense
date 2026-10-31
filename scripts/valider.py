"""Contrôle automatique de data/operations.csv (étape 4 de la charte).

Usage : python scripts/valider.py [chemin_du_csv]
Renvoie un code de sortie 1 s'il trouve au moins une erreur, ce qui fait échouer
la vérification GitHub Actions. Les avertissements n'empêchent pas la publication.
"""
import csv
import re
import sys
from datetime import date
from pathlib import Path

COLONNES = [
    "id", "date_annonce", "entreprise", "siren", "annee_creation", "region", "profil",
    "preuve_defense", "segment", "type_operation", "stade", "montant_meur", "montant_statut",
    "montant_public_meur", "instruments_publics", "investisseurs", "chef_de_file",
    "source_url", "source_type", "statut_validation", "source_secondaire", "date_collecte", "notes",
]

OBLIGATOIRES = ["id", "date_annonce", "entreprise", "profil", "segment", "type_operation",
                "stade", "montant_statut", "source_url", "source_type", "statut_validation"]

LISTES = {
    "profil": {"defense", "dual"},
    "segment": {"drones_robotique", "anti_drones", "ia_logiciel", "spatial", "cyber", "quantique",
                "capteurs_optronique", "energie_propulsion", "munitions_effecteurs", "naval",
                "materiaux_fabrication", "autre"},
    "type_operation": {"levee_privee", "financement_public", "mixte"},
    "stade": {"amorcage", "serie_a", "serie_b", "serie_c_plus", "subvention", "autre"},
    "montant_statut": {"communique", "non_communique"},
    "source_type": {"entreprise", "investisseur", "institution", "presse"},
    "statut_validation": {"a_verifier", "valide"},
}
INSTRUMENTS = {"definvest", "fid", "bpifrance_autre", "rapid", "aid_autre", "eic", "fed", "autre_public"}

DEBUT_PERIODE = date(2024, 1, 1)
RE_ID = re.compile(r"^OP-(\d{4})-\d{3}$")
RE_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def nombre(valeur):
    try:
        return float(valeur)
    except ValueError:
        return None


def valider(chemin):
    erreurs, avertissements = [], []
    with open(chemin, newline="", encoding="utf-8") as f:
        lecteur = csv.DictReader(f)
        if lecteur.fieldnames != COLONNES:
            erreurs.append("En-têtes différents du schéma de la charte.")
            return erreurs, avertissements
        lignes = list(lecteur)

    ids, operations = set(), set()
    for n, l in enumerate(lignes, start=2):  # ligne 1 = en-têtes
        ref = f"ligne {n} ({l['id'] or '?'})"

        for col in OBLIGATOIRES:
            if not l[col].strip():
                erreurs.append(f"{ref} : colonne obligatoire vide « {col} ».")

        for col, autorisees in LISTES.items():
            if l[col] and l[col] not in autorisees:
                erreurs.append(f"{ref} : valeur « {l[col]} » non autorisée pour {col}.")

        m = RE_ID.match(l["id"])
        if not m:
            erreurs.append(f"{ref} : identifiant au mauvais format (OP-AAAA-NNN).")
        if l["id"] in ids:
            erreurs.append(f"{ref} : identifiant en double.")
        ids.add(l["id"])

        if not RE_DATE.match(l["date_annonce"]):
            erreurs.append(f"{ref} : date_annonce au mauvais format (AAAA-MM-JJ).")
        else:
            d = date.fromisoformat(l["date_annonce"])
            if d < DEBUT_PERIODE:
                erreurs.append(f"{ref} : opération antérieure au 1er janvier 2024, hors périmètre.")
            if d > date.today():
                erreurs.append(f"{ref} : date dans le futur.")
            if m and m.group(1) != l["date_annonce"][:4]:
                avertissements.append(f"{ref} : l'année de l'identifiant ne correspond pas à la date.")

        if l["annee_creation"]:
            annee = nombre(l["annee_creation"])
            if annee and RE_DATE.match(l["date_annonce"]) and int(l["date_annonce"][:4]) - annee >= 15:
                erreurs.append(f"{ref} : entreprise créée il y a 15 ans ou plus, hors périmètre.")

        # Montants : jamais d'estimation, cohérence entre colonnes.
        total, public = l["montant_meur"], l["montant_public_meur"]
        if l["montant_statut"] == "communique" and not total:
            erreurs.append(f"{ref} : montant dit communiqué mais colonne vide.")
        if l["montant_statut"] == "non_communique" and total:
            erreurs.append(f"{ref} : montant non communiqué mais colonne remplie.")
        if total and nombre(total) is None:
            erreurs.append(f"{ref} : montant_meur n'est pas un nombre (séparateur décimal = point).")
        if public and nombre(public) is None:
            erreurs.append(f"{ref} : montant_public_meur n'est pas un nombre.")
        if total and public and nombre(total) is not None and nombre(public) is not None:
            if nombre(public) > nombre(total):
                erreurs.append(f"{ref} : part publique supérieure au montant total.")

        # Instruments publics et type d'opération.
        instr = [i for i in l["instruments_publics"].split(";") if i]
        for i in instr:
            if i not in INSTRUMENTS:
                erreurs.append(f"{ref} : instrument public inconnu « {i} ».")
        if l["type_operation"] in {"mixte", "financement_public"} and not instr:
            erreurs.append(f"{ref} : opération {l['type_operation']} sans instrument public.")
        if l["type_operation"] == "levee_privee" and instr:
            erreurs.append(f"{ref} : levée privée avec instrument public (passer en mixte ?).")

        # Une entreprise duale validée doit prouver son client défense.
        if l["profil"] == "dual" and l["statut_validation"] == "valide" and not l["preuve_defense"]:
            erreurs.append(f"{ref} : entreprise duale validée sans preuve de client défense.")

        for col in ("source_url", "preuve_defense", "source_secondaire"):
            if l[col] and not l[col].startswith("https://"):
                avertissements.append(f"{ref} : {col} ne commence pas par https://.")

        if not l["region"]:
            avertissements.append(f"{ref} : région à compléter.")

        cle = (l["entreprise"].lower(), l["date_annonce"])
        if cle in operations:
            erreurs.append(f"{ref} : même entreprise et même date qu'une autre ligne (doublon ?).")
        operations.add(cle)

    return erreurs, avertissements


if __name__ == "__main__":
    chemin = Path(sys.argv[1] if len(sys.argv) > 1 else "data/operations.csv")
    erreurs, avertissements = valider(chemin)
    for a in avertissements:
        print(f"AVERTISSEMENT  {a}")
    for e in erreurs:
        print(f"ERREUR         {e}")
    print(f"\n{len(erreurs)} erreur(s), {len(avertissements)} avertissement(s).")
    sys.exit(1 if erreurs else 0)
