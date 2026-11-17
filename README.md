# aidesadememobilite

Projets aidés par l'ADEME dans la **mobilité des personnes** : entreprises et associations financées (hors fret et logistique).

**Voir le graphe interactif :** ouvrez `index.html` (ou activez GitHub Pages sur ce dépôt : *Settings → Pages → Branch `main` / root*).

## Contenu

| Fichier | Description |
|---|---|
| `index.html` | Graphe à bulles interactif : organisations regroupées par thématique, surface = montant d'aide, couleur = type (entreprise / association) ou taille d'entreprise, détail des dispositifs de financement au survol et au clic. |
| `data/ADEME_financements_mobilite_personnes.xlsx` | Classeur complet : lisez-moi, organisations, synthèses par taille et par thématique, détail des aides, aides exclues (avec le motif). |
| `data/organisations_mobilite_personnes.csv` | Une ligne par organisation (595), séparateur `;`, prêt pour Colab / Streamlit. |
| `data/bulles.json` | Données du graphe (une entrée par organisation et par thématique). |
| `data/brut/` | Extractions brutes classées à la main (`P` personnes, `M` mixte, `F` fret, `X` hors mobilité, `C` collectivité, `O` organisme public). |
| `scripts/consolide.py` | Script qui reconstruit l'Excel et le CSV à partir de `data/brut/` (`pip install pandas openpyxl`, puis `python scripts/consolide.py`). |

## Chiffres clés

- 595 organisations : 514 entreprises, 81 associations ou fondations.
- 655 M€ d'aides, dont 385 M€ clairement pour la mobilité des personnes et 270 M€ « mixte / à vérifier ».
- Principales thématiques : hydrogène mobilité (25 %), recharge électrique (21 %), ferroviaire et transports collectifs (21 %), carburants aviation durables (17 %).

## Sources et méthode

- [Les aides financières de l'ADEME](https://data.ademe.fr/datasets/les-aides-financieres-de-l'ademe) (aides engagées depuis 2021).
- [Programmes d'État – Bénéficiaires des projets financés par l'ADEME](https://data.ademe.fr/datasets/programmes-detat-partenaires-des-projets-finances-par-lademe) (France 2030), qui donne la taille des entreprises (PME / ETI / GE).
- Licence Ouverte / Open Licence (Etalab). Extraction du 16/11/2026 via le MCP Data ADEME.

Sélection par dispositif d'aide lié à la mobilité, puis exclusion du fret (dispositifs poids lourds, logistique, report modal, et objets d'aide concernant camions, wagons ou livraisons), des collectivités et des organismes publics.

## Limites

- Taille d'entreprise connue seulement pour les bénéficiaires France 2030 (PME inclut les TPE) ; 282 entreprises restent « non renseignées » et peuvent être complétées via SIRENE à partir du SIREN.
- La portée des associations (nationale / régionale) est estimée à partir du nom.
- Le classement personnes / mixte / fret est un jugement manuel sur l'objet de chaque aide.
- 7 aides sur 916 n'ont pas pu être récupérées dans la première source (pagination).
