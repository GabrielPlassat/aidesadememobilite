# aidesadememobilite

Projets aidés par l'ADEME dans la **mobilité des personnes** : entreprises et associations financées (hors fret et logistique), plus tous les bénéficiaires des **programmes CEE** portés par l'ADEME (AVELO, Marche du quotidien, location sociale de voitures électriques PRO-INNO-85).

**Voir le graphe interactif :** ouvrez `index.html` (ou activez GitHub Pages sur ce dépôt : *Settings → Pages → Branch `main` / root*).

## Contenu

| Fichier | Description |
|---|---|
| `index.html` | Graphe à bulles interactif : organisations regroupées par thématique, surface = montant d'aide, couleur = type (entreprise / association) ou taille d'entreprise, détail des dispositifs de financement au survol et au clic. |
| `data/ADEME_financements_mobilite_personnes.xlsx` | Classeur complet : lisez-moi, organisations, synthèses par taille et par thématique, détail des aides, aides exclues (avec le motif). |
| `data/organisations_mobilite_personnes.csv` | Une ligne par organisation (595), séparateur `;`, prêt pour Colab / Streamlit. |
| `data/bulles.json` | Données du graphe (une entrée par organisation et par thématique). |
| `data/brut/raw_cee.csv`, `data/brut/raw_cee_leasing.csv` | Aides des programmes CEE : AVELO 1 à 3 et Marche du quotidien (1 177 aides, 915 bénéficiaires), location sociale (2 conventions avec l'ASP). |
| `scripts/carte_template.html` | Modèle du graphe ; le script y injecte les données pour produire `index.html`. |
| `data/brut/` | Extractions brutes classées à la main (`P` personnes, `M` mixte, `F` fret, `X` hors mobilité, `C` collectivité, `O` organisme public). |
| `scripts/consolide.py` | Script qui reconstruit l'Excel, le CSV, `data/bulles.json` et `index.html` à partir de `data/brut/` (`pip install pandas openpyxl`, puis `python scripts/consolide.py`). |

## Chiffres clés

- Hors programmes CEE : 595 organisations (514 entreprises, 81 associations ou fondations) et 655 M€ d'aides, dont 385 M€ clairement pour la mobilité des personnes et 270 M€ « mixte / à vérifier ».
- Avec les programmes CEE : 1 504 organisations et 1 444,5 M€ (dont 789,4 M€ de programmes CEE).
- Principales thématiques : hydrogène mobilité (25 %), recharge électrique (21 %), ferroviaire et transports collectifs (21 %), carburants aviation durables (17 %).

## Programmes CEE

| Programme | Aides | Bénéficiaires | Montant |
|---|---|---|---|
| Location sociale de voitures électriques (PRO-INNO-85) | 2 | 1 (Agence de services et de paiement) | 730,6 M€ |
| AVELO 1, 2, 2.2 et 3 (politiques cyclables) | 1 070 | 840 | 54,1 M€ |
| Marche du quotidien | 107 | 106 | 4,7 M€ |

- 98 % des aides AVELO et Marche du quotidien vont à des collectivités (communes, intercommunalités, départements, régions, syndicats mixtes) : pour ces programmes, les collectivités sont donc incluses.
- Location sociale : l'ADEME verse l'enveloppe à l'ASP, qui paie l'aide aux ménages via les loueurs. Les données ne listent ni les loueurs ni les ménages. Dans le graphe, cette bulle est masquée par défaut (case à cocher) car elle dépasse le total de toutes les autres aides.
- Le programme CEE E-Trans (poids lourds, engins) reste exclu car il concerne le fret.

## Sources et méthode

- [Les aides financières de l'ADEME](https://data.ademe.fr/datasets/les-aides-financieres-de-l'ademe) (aides engagées depuis 2021).
- [Programmes d'État – Bénéficiaires des projets financés par l'ADEME](https://data.ademe.fr/datasets/programmes-detat-partenaires-des-projets-finances-par-lademe) (France 2030), qui donne la taille des entreprises (PME / ETI / GE).
- Licence Ouverte / Open Licence (Etalab). Extraction du 16/11/2026 via le MCP Data ADEME.

Sélection par dispositif d'aide lié à la mobilité, puis exclusion du fret (dispositifs poids lourds, logistique, report modal, et objets d'aide concernant camions, wagons ou livraisons), des collectivités et des organismes publics.

## Limites

- Taille d'entreprise connue seulement pour les bénéficiaires France 2030 (PME inclut les TPE) ; 282 entreprises restent « non renseignées » et peuvent être complétées via SIRENE à partir du SIREN.
- La portée des associations (nationale / régionale) est estimée à partir du nom.
- Le classement personnes / mixte / fret est un jugement manuel sur l'objet de chaque aide.
- Quelques aides n'ont pas pu être récupérées à cause de la pagination de l'outil d'accès : 7 sur 916 hors CEE, 4 sur 1 181 pour AVELO / Marche du quotidien.
