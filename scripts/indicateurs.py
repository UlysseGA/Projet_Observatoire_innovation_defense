"""Calcule les premiers indicateurs de la charte à partir des seules lignes validées.

Usage : python scripts/indicateurs.py [chemin_du_csv]
Chaque indicateur est affiché avec le nombre d'opérations sur lequel il repose (n),
comme l'exige la charte : avec quelques dizaines de lignes, un chiffre sans son n trompe.
"""
import csv
import sys
from collections import defaultdict
from statistics import median


def trimestre(date_iso):
    annee, mois = int(date_iso[:4]), int(date_iso[5:7])
    return f"{annee}-T{(mois - 1) // 3 + 1}"


def main(chemin):
    with open(chemin, newline="", encoding="utf-8") as f:
        toutes = list(csv.DictReader(f))
    lignes = [l for l in toutes if l["statut_validation"] == "valide"]
    print(f"Lignes validées : {len(lignes)} sur {len(toutes)} recensées.\n")
    if not lignes:
        return

    montants = [float(l["montant_meur"]) for l in lignes if l["montant_meur"]]
    print("Taux de transparence")
    print(f"  {len(montants)}/{len(lignes)} opérations avec montant communiqué "
          f"({len(montants) / len(lignes):.0%})\n")

    print("Volume par trimestre (somme des montants communiqués, M€)")
    par_trimestre = defaultdict(list)
    for l in lignes:
        par_trimestre[trimestre(l["date_annonce"])].append(l)
    for t in sorted(par_trimestre):
        groupe = par_trimestre[t]
        somme = sum(float(l["montant_meur"]) for l in groupe if l["montant_meur"])
        print(f"  {t} : {len(groupe)} opération(s), {somme:.1f} M€")
    print()

    for dimension in ("stade", "segment"):
        print(f"Ticket médian par {dimension} (M€)")
        groupes = defaultdict(list)
        for l in lignes:
            if l["montant_meur"]:
                groupes[l[dimension]].append(float(l["montant_meur"]))
        for cle, valeurs in sorted(groupes.items()):
            print(f"  {cle} : {median(valeurs):.1f} (n={len(valeurs)})")
        print()

    avec_public = [l for l in lignes if l["instruments_publics"]]
    print("Présence d'un instrument public")
    print(f"  {len(avec_public)}/{len(lignes)} opérations ({len(avec_public) / len(lignes):.0%})")
    connus = [l for l in lignes if l["montant_meur"] and l["montant_public_meur"]]
    if connus:
        part = sum(float(l["montant_public_meur"]) for l in connus) / sum(float(l["montant_meur"]) for l in connus)
        print(f"  Part publique là où elle est publiée : {part:.0%} (n={len(connus)})")
    else:
        print("  Part publique : aucune opération validée ne la publie encore.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/operations.csv")
