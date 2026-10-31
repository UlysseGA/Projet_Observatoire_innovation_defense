# Observatoire du financement de l'innovation de défense (France)

Base de données ouverte et sourcée des levées de fonds et financements publics des jeunes entreprises françaises de défense, depuis le 1er janvier 2024.

**Questions suivies**

1. Effet de levier public : quand Definvest, Bpifrance, l'EIC ou le Fonds européen de la défense investissent, combien d'argent privé suit ?
2. Où va l'argent : montants par segment technologique et par stade de maturité.
3. Qui finance : concentration des investisseurs, fonds spécialisés face aux fonds généralistes.
4. Dynamique : nombre et montant des opérations par trimestre.

## État de la base

| | |
| --- | --- |
| Opérations recensées | 10 |
| Dont validées | 5 |
| Dernière mise à jour | 2026-11-01 |

Seules les lignes validées entrent dans les indicateurs publiés.

## Périmètre

- Entreprise au siège en France, créée il y a moins de 15 ans, indépendante d'un grand groupe.
- De défense, ou duale avec un client défense identifié publiquement.
- Levées de fonds privées et financements publics ; ni rachats, ni contrats commerciaux.
- Opérations annoncées à partir du 1er janvier 2024.

Les définitions complètes, les règles de classement et les cas limites figurent dans la [charte méthodologique](docs/charte-methodologique.md). Chaque arbitrage est consigné dans le [journal des décisions](docs/journal-decisions.md).

## Organisation du dépôt

```
data/operations.csv        la base, une ligne par opération
docs/                      charte, dictionnaire des colonnes, journal des décisions
scripts/valider.py         contrôle automatique des formats et de la cohérence
scripts/indicateurs.py     calcul des indicateurs sur les lignes validées
.github/workflows/         relance le contrôle à chaque modification de la base
```

## Utilisation

Python 3.10 ou plus récent, sans dépendance externe.

```bash
python scripts/valider.py       # 0 erreur attendu avant toute publication
python scripts/indicateurs.py   # indicateurs avec leur nombre d'observations
```

## Limites

- Les sommes ne comptent que les montants publiés : le total réel est plus élevé.
- Les entreprises qui communiquent beaucoup sont mieux couvertes.
- L'échantillon est petit ; un pourcentage s'affiche toujours avec son nombre d'observations.
- Une corrélation entre soutien public et levée privée ultérieure ne prouve pas que le premier a causé la seconde.

## Licences

- Code : [MIT](LICENSE).
- Données : [CC BY 4.0](LICENSE-DATA.md) — réutilisation libre, y compris commerciale, en citant l'observatoire.

## Sources et déontologie

La base ne contient que des faits publics sur des entreprises, avec un lien vers leur source. Aucun texte d'article n'est reproduit, aucune donnée de base commerciale n'est republiée et aucune donnée personnelle n'est collectée.

Auteur : Ulysse Gauchet.
