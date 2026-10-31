# Observatoire du financement de l'innovation de défense — Charte méthodologique

Version du 1er novembre 2026 · Ulysse Gauchet

## Objet et questions de recherche

L'observatoire recense, une source par ligne, chaque opération de financement d'une jeune entreprise française de défense depuis le 1er janvier 2024. Son but : mesurer comment argent public et argent privé se combinent pour faire émerger l'innovation de défense.

Il répond à quatre questions :

1. **Effet de levier public.** Quand un acteur public investit (Definvest, Bpifrance, EIC, Fonds européen de la défense), combien d'euros privés suivent dans les 18 mois ?
2. **Où va l'argent.** Répartition des montants par segment technologique et par stade de maturité (amorçage, série A, B…).
3. **Qui finance.** Concentration des investisseurs, poids des fonds spécialisés défense face aux fonds généralistes.
4. **Dynamique.** Nombre et montant des opérations par trimestre.

Une *opération* désigne ici un apport d'argent daté et public à une entreprise : levée de fonds, subvention, avance remboursable ou prêt. La définition exacte figure plus bas.

## Périmètre

Une ligne entre dans la base seulement si elle remplit les quatre critères ci-dessous à la fois.

| Critère | Inclus | Exclu |
| --- | --- | --- |
| Géographie | Siège social en France à la date de l'opération | Filiale française d'un groupe étranger ; entreprise étrangère ayant seulement un bureau en France |
| Entreprise | Jeune entreprise indépendante, créée il y a moins de 15 ans, de défense ou duale avec un client défense identifié publiquement | Grands maîtres d'œuvre (Thales, Safran, MBDA, Naval Group, KNDS, Dassault Aviation) et filiales détenues à plus de 50 % par un groupe |
| Opération | Levée de fonds privée ; investissement ou aide publique (Definvest, Bpifrance, Agence de l'innovation de défense, EIC, Fonds européen de la défense) | Rachats et cessions d'entreprises ; contrats commerciaux et commandes ; prêts bancaires ordinaires |
| Période | Opération annoncée publiquement le 1er janvier 2024 ou après | Opération antérieure, même si elle est annoncée tardivement par une source secondaire |

Un contrat commercial est exclu parce qu'il rémunère un produit livré : c'est du chiffre d'affaires, pas un financement de l'innovation. Il peut en revanche servir de preuve du « client défense identifié ».

## Définitions

Chaque terme ci-dessous a un sens fixe dans la base ; un cas qui n'y entre pas clairement va dans la liste des cas limites.

- **Entreprise de défense** : son produit principal est conçu d'abord pour un usage militaire ou de sécurité nationale (munition rôdeuse, système de commandement, lutte anti-drones…).
- **Entreprise duale** : son produit sert des clients civils et militaires (imagerie spatiale, cybersécurité, IA, quantique…).
- **Client défense identifié** : au moins une preuve publique d'un lien défense avant ou au moment de l'opération. Valent preuve : un contrat avec la DGA, l'AID ou une armée, un programme RAPID, un financement Definvest, une participation à un projet du Fonds européen de la défense ou un contrat OTAN.
- **Opération** : un apport d'argent à une entreprise, annoncé publiquement et daté. Un tour de table compte pour une ligne, quel que soit le nombre d'investisseurs.
- **Instrument public** : tout financement dont la décision relève d'un acteur public français ou européen. Exemples : Definvest (fonds du ministère des Armées géré par Bpifrance), Fonds Innovation Défense, RAPID (subvention DGA-AID aux PME), EIC Accelerator, Fonds européen de la défense.
- **Stade** : la maturité financière de l'entreprise au moment de l'opération. Valeurs : amorçage (*seed*), série A, B, C ou plus, subvention, autre.
- **Montant** : le montant total annoncé de l'opération, en millions d'euros. Une somme annoncée dans une autre devise est convertie au taux du jour de l'annonce.

## Schéma des données

La base est un tableau de 20 colonnes, une ligne par opération. Les noms de colonnes sont sans accents ni espaces pour rester lisibles par le code ; une liste fermée signifie que seules les valeurs indiquées sont acceptées.

| Colonne | Contenu | Format ou valeurs autorisées | Exemple |
| --- | --- | --- | --- |
| id | Identifiant unique | OP-AAAA-NNN | OP-2024-001 |
| date_annonce | Date de la première annonce publique | AAAA-MM-JJ | 2024-03-12 |
| entreprise | Nom commercial | Texte | Exemple SAS |
| siren | Numéro d'entreprise, pour éviter les doublons | 9 chiffres ou vide | 123456789 |
| annee_creation | Année de création | AAAA | 2019 |
| region | Région du siège | Région française | Île-de-France |
| profil | Défense ou duale | defense, dual | dual |
| preuve_defense | Lien vers la preuve du client défense (obligatoire si dual) | URL | |
| segment | Technologie principale | Liste fermée, voir règles | drones_robotique |
| type_operation | Nature du financement | levee_privee, financement_public, mixte | mixte |
| stade | Maturité au moment de l'opération | amorcage, serie_a, serie_b, serie_c_plus, subvention, autre | serie_a |
| montant_meur | Montant total, en millions d'euros | Décimal, point comme séparateur ; vide si non communiqué | 12.5 |
| montant_statut | Le montant est-il public ? | communique, non_communique | communique |
| montant_public_meur | Part publique identifiée, en millions d'euros | Décimal ou vide | 3 |
| instruments_publics | Instruments publics présents | definvest, fid, bpifrance_autre, rapid, aid_autre, eic, fed, autre_public (séparés par ;) | definvest;eic |
| investisseurs | Tous les investisseurs nommés | Noms séparés par ; | Fonds A;Fonds B |
| chef_de_file | Investisseur qui mène le tour | Texte ou vide | Fonds A |
| source_url | Source principale | URL | |
| source_type | Nature de la source | entreprise, investisseur, institution, presse | entreprise |
| statut_validation | Vérifié à la main ? | a_verifier, valide | valide |

Trois colonnes de suivi s'y ajoutent hors analyse : date_collecte, notes (cas limite, doute) et source_secondaire (deuxième URL qui confirme).

## Règles de classement et cas limites

Une règle prime toujours : on n'estime jamais une donnée absente, on la laisse vide et on l'explique dans les notes.

**Segments.** Une entreprise reçoit un seul segment, celui de son produit principal. S'il y en a deux, on retient celui que l'annonce de financement met en avant. Valeurs : drones_robotique, anti_drones, ia_logiciel, spatial, cyber, quantique, capteurs_optronique, energie_propulsion, munitions_effecteurs, naval, materiaux_fabrication, autre.

| Cas | Règle |
| --- | --- |
| Montant non communiqué | montant_meur vide, montant_statut = non_communique. Un chiffre « selon nos informations » de la presse va dans les notes, pas dans la colonne. |
| Tour privé avec un investisseur public (ex. Definvest parmi d'autres) | Une seule ligne, type_operation = mixte, l'instrument dans instruments_publics, la part publique seulement si elle est annoncée. |
| EIC Accelerator (subvention + prise de participation) | Une seule ligne, type_operation = financement_public, stade = subvention. |
| Projet du Fonds européen de la défense en consortium | La part revenant à l'entreprise si elle est publiée ; sinon montant vide et budget total du projet dans les notes. |
| Extension d'un tour déjà recensé | Nouvelle ligne si de l'argent frais est annoncé séparément, avec « extension » dans les notes. |
| Date de signature différente de la date d'annonce | On retient la date de la première annonce publique. |
| Même opération dans plusieurs articles | Une seule ligne : la source la plus directe en source_url, une autre en source_secondaire. |
| Doute sur le périmètre | statut_validation = a_verifier et une note. La décision est prise lors de la revue mensuelle puis consignée dans le journal des décisions du dépôt. |

Le journal des décisions rend la base reproductible : quelqu'un d'autre, avec la charte et le journal, doit pouvoir classer une nouvelle opération de la même façon.

## Sources

Chaque ligne cite la source la plus proche de l'opération ; une source de rang 4 sert à repérer une opération, jamais à la justifier.

| Rang | Type de source | Exemples | Usage |
| --- | --- | --- | --- |
| 1 | Institution qui finance | Commission européenne (résultats du Fonds européen de la défense), EIC, ministère des Armées, AID, Bpifrance | Source principale à privilégier |
| 2 | Communiqué officiel de l'entreprise ou de l'investisseur | Site, salle de presse, compte LinkedIn officiel | Source principale |
| 3 | Presse économique et spécialisée | Maddyness, Les Echos, L'Usine Nouvelle, Le Journal des entreprises, Sifted, Air & Cosmos | Source principale si rien de mieux, sinon source secondaire |
| 4 | Bases commerciales | Crunchbase, Dealroom, PitchBook | Repérage seulement : leurs conditions interdisent de republier leurs données |

**Sources à surveiller chaque mois :**

- [Résultats des appels du Fonds européen de la défense](https://defence-industry-space.ec.europa.eu/funding-opportunities-0/calls-proposals/results-edf-2023-calls-proposals_en) et la [décision d'attribution 2024](https://defence-industry-space.ec.europa.eu/system/files/2025-10/EDF-2024%20Adopted%20Award%20Decision%20-%20C%282025%29%206378%20EN.pdf), qui listent les projets retenus et leurs participants.
- [Fiche ministérielle sur Definvest et le Fonds Innovation Défense](https://armement.defense.gouv.fr/sites/default/files/2025-05/025_fiche%20fonds%20defense_PEPS.pdf), pour la doctrine de chaque fonds.
- Les communiqués de Bpifrance, de l'AID et de la DGA.
- Les bilans mensuels de levées de [Maddyness](https://www.maddyness.com/hashtag/frenchtech), à filtrer sur la défense.
- Les pages « portefeuille » des fonds spécialisés défense français.

## Processus de collecte et de validation

Toute ligne passe par cinq étapes, et seules les lignes au statut valide entrent dans les chiffres publiés.

1. **Repérage (chaque semaine, environ 30 minutes).** L'agrégateur de veille signale les articles qui mentionnent une levée ou une aide ; on complète avec les sources à surveiller.
2. **Saisie.** Une ligne par opération dans le tableau, au statut a_verifier. Un LLM peut pré-remplir les colonnes à partir de l'article, mais son résultat reste une proposition.
3. **Vérification humaine.** On ouvre la source, contrôle chaque cellule, ajoute une source secondaire si elle existe, puis passe la ligne en valide.
4. **Contrôle automatique.** `scripts/valider.py` vérifie les formats, les valeurs autorisées, les doublons, les dates hors période et la cohérence des montants (part publique inférieure ou égale au total).
5. **Revue mensuelle.** On tranche les cas a_verifier, note chaque décision dans le journal, puis publie une version datée de la base.

Le LLM ne remplit jamais seul la colonne montant : un modèle de langage peut inventer un chiffre plausible, ce qu'on appelle une *hallucination*, et une seule erreur de ce type décrédibilise toute la base.

## Indicateurs prévus et limites connues

Six indicateurs répondent aux quatre questions de départ ; chacun est publié avec le nombre d'opérations sur lequel il repose.

| Indicateur | Calcul | Question |
| --- | --- | --- |
| Volume trimestriel | Nombre d'opérations et somme des montants communiqués, par trimestre | Dynamique |
| Taux de transparence | Part des opérations dont le montant est communiqué | Fiabilité des autres chiffres |
| Ticket médian | Médiane des montants par stade et par segment | Où va l'argent |
| Part publique | Somme des parts publiques ÷ somme des montants, sur les opérations où les deux sont connus | Effet de levier |
| Effet d'entraînement | Part des entreprises soutenues par un instrument public qui lèvent des fonds privés dans les 18 mois | Effet de levier |
| Concentration | Part des opérations où figure au moins un des cinq investisseurs les plus actifs | Qui finance |

La *médiane* est la valeur qui partage les opérations en deux moitiés ; contrairement à la moyenne, une méga-levée ne la déforme pas.

**Limites à afficher avec chaque publication :**

- **Sous-estimation.** Les sommes ne comptent que les montants communiqués ; le total réel est plus élevé.
- **Biais de visibilité.** Les entreprises qui communiquent beaucoup sont mieux couvertes, et certaines opérations de défense ne sont jamais annoncées.
- **Petit échantillon.** Sur le seul périmètre français, quelques dizaines d'opérations par an : on arrondit les pourcentages et on évite les comparaisons trop fines.
- **Corrélation, pas causalité.** Si les entreprises soutenues par Definvest lèvent davantage ensuite, c'est peut-être parce que Definvest choisit déjà les plus prometteuses. On appelle cela un *effet de sélection* ; l'indicateur d'entraînement ne prouve donc pas que l'argent public a causé la levée.

## Cadre juridique et déontologique

La base ne contient que des faits publics sur des entreprises, avec un lien vers leur source.

- **Droit d'auteur.** Un fait (date, montant, nom d'investisseur) n'est pas protégé ; le texte d'un article l'est. On reprend donc les faits et le lien, jamais de passage d'article.
- **Conditions d'utilisation des sites.** Aucune donnée tirée d'une base commerciale n'est republiée. La collecte automatique respecte les fichiers robots.txt et reste peu fréquente.
- **Données personnelles.** La base décrit des entreprises, pas des personnes : ni nom de fondateur, ni de dirigeant.
- **Informations sensibles.** Uniquement des informations publiques sur le financement ; aucune information sur des unités, des capacités ou des localisations militaires.
- **Licences.** Code sous licence MIT. Données sous CC BY 4.0. Analyses et newsletter : tous droits réservés.
