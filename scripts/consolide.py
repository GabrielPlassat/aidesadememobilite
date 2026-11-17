import re, sys
import pandas as pd

import os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "brut") + "/"

CODES = {
 "VLO": ("Développer le Vélotourisme", "Vélo & mobilités actives"),
 "IDV": ("Industries du Vélo", "Vélo & mobilités actives"),
 "AVELO1": ("AVELO 1 (programme CEE)", "Programme CEE AVELO (politiques cyclables)"),
 "AVELO2": ("AVELO 2 (programme CEE)", "Programme CEE AVELO (politiques cyclables)"),
 "AVELO22": ("AVELO 2.2 (programme CEE)", "Programme CEE AVELO (politiques cyclables)"),
 "AVELO31": ("AVELO 3 - 1er relevé (programme CEE)", "Programme CEE AVELO (politiques cyclables)"),
 "AVELO32": ("AVELO 3 - 2e relevé (programme CEE)", "Programme CEE AVELO (politiques cyclables)"),
 "AVELO33": ("AVELO 3 - 3e relevé (programme CEE)", "Programme CEE AVELO (politiques cyclables)"),
 "MDQ": ("Marche du quotidien (programme CEE)", "Programme CEE Marche du quotidien"),
 "LSOC": ("Location sociale de voitures électriques (programme CEE PRO-INNO-85)", "Programme CEE Location sociale de voitures électriques"),
 "MAP": ("Mobilités actives et partagées : changement de comportements", "Services de mobilité & changement de comportement"),
 "MAPS": ("Mobilités actives, partagées et solidaires : changement de comportements", "Services de mobilité & changement de comportement"),
 "SMD": ("Services de mobilités douces en entreprise", "Services de mobilité & changement de comportement"),
 "SMDR": ("Services de mobilité douce en entreprises (Réunion/Mayotte)", "Services de mobilité & changement de comportement"),
 "TEN21": ("AMI TenMod 2021 - Territoires de nouvelles mobilités durables", "Services de mobilité & changement de comportement"),
 "TEN22": ("AMI TenMod 2022 - Projets lauréats", "Services de mobilité & changement de comportement"),
 "ETMD": ("Aide aux études en matière de mobilité durable", "Services de mobilité & changement de comportement"),
 "OCCAIR": ("Solutions de mobilité à co-bénéfices qualité de l'air (Occitanie)", "Services de mobilité & changement de comportement"),
 "PCTE": ("Plan de circulation pour la transition écologique", "Services de mobilité & changement de comportement"),
 "PMS": ("Plans de mobilité simplifiés, schémas directeurs modes actifs", "Services de mobilité & changement de comportement"),
 "MOB": ("Mobilogs - mobilités et logistiques soutenables (recherche)", "Recherche & connaissances"),
 "XD": ("L'eXtrême Défi (XD)", "Véhicules intermédiaires (eXtrême Défi)"),
 "XDP": ("Prototypes de l'eXtrême Défi", "Véhicules intermédiaires (eXtrême Défi)"),
 "XDU": ("Usine Distribuée pour l'eXtrême Défi", "Véhicules intermédiaires (eXtrême Défi)"),
 "XDI2": ("Idéation Saison 2 (2023) - XD", "Véhicules intermédiaires (eXtrême Défi)"),
 "XDI3": ("Idéation Saison 3 (2024) - XD", "Véhicules intermédiaires (eXtrême Défi)"),
 "XDV": ("Industrie des Véhicules Intermédiaires (XD)", "Véhicules intermédiaires (eXtrême Défi)"),
 "SKATE": ("Habitacles pour plateformes skateboard de véhicules intermédiaires", "Véhicules intermédiaires (eXtrême Défi)"),
 "PEVER": ("Protocole d'expérimentation sur l'usage de véhicules intermédiaires", "Véhicules intermédiaires (eXtrême Défi)"),
 "IRVE": ("Soutien au déploiement de stations de recharge VE", "Énergie : recharge électrique"),
 "IRVESS": ("Infrastructures de recharge dans les stations-service indépendantes", "Énergie : recharge électrique"),
 "SDICA": ("Études multi-carburants / SDICA (flottes)", "Énergie : recharge électrique"),
 "ECOH2": ("Écosystèmes territoriaux Hydrogène", "Énergie : hydrogène mobilité"),
 "ECOSYSH2": ("Écosystèmes territoriaux hydrogène - EcosysH2", "Énergie : hydrogène mobilité"),
 "EMH2": ("Écosystèmes Mobilité Hydrogène 2018-2019", "Énergie : hydrogène mobilité"),
 "ETH2": ("Études d'opportunité déploiement hydrogène sur un territoire", "Énergie : hydrogène mobilité"),
 "ETH2B": ("Études déploiement d'écosystèmes et usages de l'hydrogène", "Énergie : hydrogène mobilité"),
 "CIH2_6": ("Concours d'innovation Hydrogène - Vague 6", "Énergie : hydrogène mobilité"),
 "BIOGNV": ("Achat de véhicules - station territoriale BioGNV/GNV", "Énergie : bioGNV"),
 "DDT": ("AMI Digitalisation et Décarbonation du Transport (France 2030)", "Ferroviaire & transports collectifs"),
 "CORIFER": ("CORIFER 2023 (ferroviaire)", "Ferroviaire & transports collectifs"),
 "CIM7": ("Concours d'innovation Mobilité durable et intelligente - Vague 7", "Technologies & numérique de la mobilité"),
 "CIT5": ("Concours d'innovation Transport et mobilité durable - Vague 5", "Technologies & numérique de la mobilité"),
 "CIT5B": ("Concours d'innovation Transport et mobilité durable - Vague 5bis", "Technologies & numérique de la mobilité"),
 "EIT": ("AAP Écosystèmes Innovants Transport", "Technologies & numérique de la mobilité"),
 "ADEIP19": ("ADEIP Transports et mobilité durable 2019", "Technologies & numérique de la mobilité"),
 "ADEIP20": ("ADEIP Transports et mobilité durable 2020", "Technologies & numérique de la mobilité"),
 "AUTO": ("Plan de relance Auto (hors AAP)", "Véhicules : industrie automobile"),
 "CARB": ("CARB AERO - carburants aéronautiques durables", "Énergie : carburants aviation durables"),
 "FEED": ("Carburants aéronautiques durables - études FEED", "Énergie : carburants aviation durables"),
 "CORIMER": ("CORIMER - Navires bas carbone", "Maritime & fluvial"),
 "REMO": ("ReMoVe - Dispositif ReMo (report modal)", "Fret"),
 "IDH2": ("Innovation et démonstration Hydrogène", "Autre"),
 "CIER7": ("Concours d'innovation EnR, stockage, hydrogène - Vague 7", "Autre"),
}

# Thématique pour les projets France 2030 (par nom de projet)
def theme_f2030(projet):
    p = projet.upper()
    if any(k in p for k in ["ELECTRIFY", "ALLEGO", "ATLANTE", "DREAM", "ELECTRA", "MOBILIZE", "FAST E-CITIES", "GUEST", "BORNE", "CPO", "PICOTY", "SOWATT", "HUREU", "REPART"]):
        return "Énergie : recharge électrique"
    if any(k in p for k in ["BIOTJET", "REUZE", "AVEBIO", "KEREAUZEN", "TAKE KAIR", "HYNOVERA", "DÉZIR", "DEZIR"]):
        return "Énergie : carburants aviation durables"
    if any(k in p for k in ["TRAIN", "SIG4LDFT", "FLEXMOVE", "ECOTRAIN", "INFRALIGHT", "NS2F", "DRAISY", "TAXIRAIL", "FLEXY", "MQSNCF", "URBANLOOP", "DIAM"]):
        return "Ferroviaire & transports collectifs"
    if any(k in p for k in ["AWAKE", "ECO-SUITE"]):
        return "Maritime & fluvial"
    return "Vélo / véhicules intermédiaires (industrie)"

THEME_SHORT = {
 "Vélo & mobilités actives": "Vélo",
}

naf_asso = set(open(D + "naf_asso.txt").read().split())

# ---------- Source A : Les aides financières de l'ADEME ----------
a = pd.read_csv(D + "raw_aides.csv", sep=";", dtype=str)
a = a[a["flag"].isin(list("PMFXCO"))].copy()
a["montant"] = a["montant"].astype(float)
a = a.drop_duplicates(subset=["siret", "montant", "date", "code"])
a["siren"] = a["siret"].str[:9]
a["dispositif"] = a["code"].map(lambda c: CODES.get(c, (c, "Autre"))[0])
a["thematique"] = a["code"].map(lambda c: CODES.get(c, (c, "Autre"))[1])
a["source"] = "Aides financières ADEME"
a["projet"] = ""
a["programme"] = ""
a["region"] = ""
a["categorie_f2030"] = ""
a["is_asso_naf"] = a["siret"].isin(naf_asso)

# ---------- Source C : programmes CEE portés par l'ADEME (AVELO, Marche du quotidien, location sociale) ----------
CEE_CODES = {"AVELO1", "AVELO2", "AVELO22", "AVELO31", "AVELO32", "AVELO33", "MDQ", "LSOC"}
a = a[~a["code"].isin(CEE_CODES)].copy()   # ces aides sont reprises en totalité dans la source C
c = pd.concat([pd.read_csv(D + "raw_cee.csv", sep=";", dtype=str),
               pd.read_csv(D + "raw_cee_leasing.csv", sep=";", dtype=str)], ignore_index=True)
c["montant"] = c["montant"].astype(float)
c = c.drop_duplicates()
c["siren"] = c["siret"].str[:9]
c["dispositif"] = c["code"].map(lambda k: CODES[k][0])
c["thematique"] = c["code"].map(lambda k: CODES[k][1])
c["source"] = "Programmes CEE (ADEME)"
c["projet"] = ""
c["flag"] = "P"
c["is_asso_naf"] = c["siret"].isin(naf_asso)

# ---------- Source B : Programmes d'Etat (France 2030 / PIA) ----------
b = pd.read_csv(D + "raw_f2030.csv", sep=";", dtype=str)
b["montant"] = b["montant"].astype(float)
b = b.drop_duplicates()
b["siret"] = ""
b["code"] = ""
b["dispositif"] = "France 2030 - " + b["projet"]
b["thematique"] = b["projet"].map(theme_f2030)
b["source"] = "Programmes d'Etat (France 2030)"
b["categorie_f2030"] = b["categorie"]
b["is_asso_naf"] = b["categorie"].eq("Association")

# Taille d'entreprise connue via France 2030 (par SIREN) : on garde la plus fréquente
taille = (b[b["categorie"] != "Association"].groupby("siren")["categorie"]
          .agg(lambda s: s.value_counts().index[0]))
asso_siren_b = set(b.loc[b["categorie"] == "Association", "siren"])

# Lignes B qui ne doublonnent pas une aide déjà présente dans A (même SIREN + même montant)
keyA = set(zip(a["siren"], a["montant"].round(0)))
b["doublon_A"] = [(s, round(m, 0)) in keyA for s, m in zip(b["siren"], b["montant"])]
b_new = b[(~b["doublon_A"]) & (b["montant"] > 0)].copy()

a["region"] = ""; c["region"] = ""
cols = ["source", "nom", "siren", "siret", "montant", "date", "dispositif", "projet",
        "thematique", "flag", "is_asso_naf", "region"]
allrows = pd.concat([a[cols], b_new[cols], c[cols]], ignore_index=True)
allrows["cee"] = allrows["source"].eq("Programmes CEE (ADEME)")

# ---------- Localisation (département / région) ----------
REG_DEP = {
 "Auvergne-Rhône-Alpes": "01 03 07 15 26 38 42 43 63 69 73 74",
 "Bourgogne-Franche-Comté": "21 25 39 58 70 71 89 90",
 "Bretagne": "22 29 35 56",
 "Centre-Val de Loire": "18 28 36 37 41 45",
 "Corse": "20 2A 2B",
 "Grand Est": "08 10 51 52 54 55 57 67 68 88",
 "Hauts-de-France": "02 59 60 62 80",
 "Île-de-France": "75 77 78 91 92 93 94 95",
 "Normandie": "14 27 50 61 76",
 "Nouvelle-Aquitaine": "16 17 19 23 24 33 40 47 64 79 86 87",
 "Occitanie": "09 11 12 30 31 32 34 46 48 65 66 81 82",
 "Pays de la Loire": "44 49 53 72 85",
 "Provence-Alpes-Côte d'Azur": "04 05 06 13 83 84",
 "Guadeloupe": "971", "Martinique": "972", "Guyane": "973", "La Réunion": "974", "Mayotte": "976",
}
DEP2REG = {d: r for r, ds in REG_DEP.items() for d in ds.split()}
REG_NORM = {r.lower().replace("-", " ").replace("î", "i").replace("é", "e").replace("ô", "o"): r for r in REG_DEP}
REG_NORM["reunion"] = "La Réunion"
def norm_reg(x):
    if not isinstance(x, str) or not x.strip():
        return ""
    k = x.strip().lower().replace("-", " ").replace("î", "i").replace("é", "e").replace("ô", "o")
    return REG_NORM.get(k, next((v for kk, v in REG_NORM.items() if kk in k), ""))
locs = pd.read_csv(D + "localisation.csv", sep=";", dtype=str)
SIRET_DEP = dict(zip(locs["siret"], locs["dept"].str.zfill(2)))
def dep_from_siren(siren):
    # SIREN des collectivités : 21=commune, 22=département, 24=EPCI, 25=syndicat, suivi du n° de département
    s = str(siren)
    if s[:2] in ("21", "22", "24", "25"):
        d = s[2:4]
        if d == "97":
            return s[2:5]
        if d == "20":
            return "20"
        if d.isdigit() and d != "00":
            return d
    return ""
allrows["region"] = allrows["region"].fillna("").map(norm_reg)
allrows["departement"] = [SIRET_DEP.get(st) or dep_from_siren(sn) for st, sn in zip(allrows["siret"].fillna(""), allrows["siren"])]
allrows.loc[allrows["departement"] != "", "region"] = allrows.loc[allrows["departement"] != "", "departement"].map(DEP2REG).fillna("")
# Une organisation présente seulement dans France 2030 : région connue par SIREN dans les autres lignes
reg_by_siren = allrows[allrows["region"] != ""].groupby("siren")["region"].agg(lambda s: s.value_counts().index[0])
dep_by_siren = allrows[allrows["departement"] != ""].groupby("siren")["departement"].agg(lambda s: s.value_counts().index[0])
m = allrows["region"] == ""
allrows.loc[m, "region"] = allrows.loc[m, "siren"].map(reg_by_siren).fillna("")
m = allrows["departement"] == ""
allrows.loc[m, "departement"] = allrows.loc[m, "siren"].map(dep_by_siren).fillna("")
print("localisation : région connue sur", (allrows["region"] != "").mean().round(3), "des lignes")

# ---------- Typologie ----------
PUBLIC_RE = re.compile(r"^(COMMUNE|COMMUNAUTE|CA |CC |PETR|SM |SM4CC|SYNDICAT MIXTE|SYND MIXTE|SYNDICAT DEPARTEMENTAL|SYNDICAT DES MOBILITES|SYNDICAT VALORISATION|CENTRE HOSPITALIER|CHAMBRE DE COMMERCE|REGIE|ETS PUB|CENTRE NATIONAL|IFP ENERGIES|ECOLE |INSTITUT DE RECHERCHE TECH|PAYS D'ORANGE)")
ASSO_NAME_RE = re.compile(r"^(ASS |ASSOCIATION|FEDERATION|FEDE |FAMILLES |CROIX ROUGE|COLLECTIF|SECOURS|FONDATION|SYND PROFESSION|SYNDICAT PROFESSIONNEL)")

def org_type(row):
    n = row["nom"]
    if row["flag"] in ("C", "O") or PUBLIC_RE.match(n) or str(row["siren"]).startswith(("13", "18", "2")):
        return "Public / collectivité"
    if row["siren"] in asso_siren_b or row["is_asso_naf"] or ASSO_NAME_RE.match(n):
        return "Association / fondation"
    return "Entreprise"

allrows["type"] = allrows.apply(org_type, axis=1)

REGIONS = ["OCCITANIE", "BRETAGNE", "NOUVELLE AQUITAINE", "NOUVELLE-AQUITAINE", "GRAND EST", "HAUTS DE FRANCE",
           "HAUTS-DE-FRANCE", "PACA", "PROVENCE", "CORSICA", "CORSE", "NORMANDIE", "ILE DE FRANCE", "ILE-DE-FRANCE",
           "BOURGOGNE", "CENTRE - VAL", "CENTRE-VAL", "AUVERGNE", "PAYS DE LA LOIRE", "REUNION", "GUADELOUPE",
           "MAYOTTE", "MAORE", "REGIONAL", "REGION", "PYRENEES", "ALSACE"]
NATIONAL = ["FRANCE", "NATIONAL", "RESEAU VELO ET MARCHE", "FEDE GENERALE", "CROIX ROUGE", "ADMR", "FONDATION",
            "INSTITUT MOBILITES EN TRANSITION", "AGENCE DU DON", "RETROFIT", "VIVACITES", "MIEUX SE DEPLACER"]

OVERRIDE = {"VELO CITE": "Régionale (estimée)", "LA PETITE FERME PEDAGOGIQUE DE SAINT REMY DE PROVENCE": "Locale ou à vérifier",
            "FRANCE VELO TOURISME": "Nationale (estimée)", "CROIX ROUGE FRANCAISE": "Nationale (estimée)"}

def portee(row):
    if row["type"] != "Association / fondation":
        return ""
    n = row["nom"].upper()
    if n in OVERRIDE:
        return OVERRIDE[n]
    if any(k in n for k in REGIONS):
        return "Régionale (estimée)"
    if any(k in n for k in NATIONAL):
        return "Nationale (estimée)"
    return "Locale ou à vérifier"

allrows["portee"] = allrows.apply(portee, axis=1)
allrows["taille"] = allrows["siren"].map(taille).fillna("")
allrows.loc[allrows["type"] == "Association / fondation", "taille"] = "Association"
allrows.loc[(allrows["type"] == "Entreprise") & (allrows["taille"] == ""), "taille"] = "Non renseignée"
allrows.loc[allrows["type"] == "Public / collectivité", "taille"] = "Collectivité / public"
TAILLE_LIB = {"PME": "PME (dont TPE)", "ETI": "ETI", "GE": "Grande entreprise"}
allrows["taille"] = allrows["taille"].replace(TAILLE_LIB)

FLAG_LIB = {"P": "Mobilité des personnes", "M": "Mixte / à vérifier",
            "F": "Exclu : fret / logistique", "X": "Exclu : hors mobilité",
            "C": "Exclu : collectivité", "O": "Exclu : organisme public"}
allrows["perimetre"] = allrows["flag"].map(FLAG_LIB)

# Entreprises et associations hors fret + tous les bénéficiaires des programmes CEE (collectivités comprises)
keep = allrows[(allrows["flag"].isin(["P", "M"]) & allrows["type"].isin(["Entreprise", "Association / fondation"]))
               | allrows["cee"]].copy()
excl = allrows.drop(keep.index).copy()

# ---------- Table organisations ----------
def mode_or_blank(sr):
    sr = sr[sr != ""]
    return sr.value_counts().index[0] if len(sr) else ""

def agg_org(g):
    flags = set(g["flag"])
    return pd.Series({
        "Nom": g["nom"].value_counts().index[0],
        "Type": g["type"].iloc[0],
        "Taille (France 2030)": g["taille"].iloc[0],
        "Portée association": g["portee"].iloc[0],
        "Département": mode_or_blank(g["departement"]),
        "Région": mode_or_blank(g["region"]),
        "Périmètre": "Mobilité des personnes" if flags == {"P"} else ("Mixte / à vérifier" if flags == {"M"} else "Personnes + mixte"),
        "Thématiques": " | ".join(sorted(set(g["thematique"]))),
        "Dispositifs": " | ".join(sorted(set(g["dispositif"]))),
        "Nb d'aides": len(g),
        "Montant total (€)": round(g["montant"].sum(), 2),
        "Première aide": g["date"].min(),
        "Dernière aide": g["date"].max(),
        "Programme CEE": "oui" if g["cee"].any() else "non",
        "Sources": " + ".join(sorted(set(g["source"]))),
    })

orgs = keep.groupby("siren").apply(agg_org).reset_index().rename(columns={"siren": "SIREN"})
orgs = orgs.sort_values("Montant total (€)", ascending=False)
orgs.insert(0, "Rang", range(1, len(orgs) + 1))

# ---------- Synthèses ----------
syn_type = (orgs.groupby(["Type", "Taille (France 2030)"])
            .agg(Organisations=("SIREN", "count"), Montant=("Montant total (€)", "sum")).reset_index())
syn_type["% du montant"] = (100 * syn_type["Montant"] / syn_type["Montant"].sum()).round(1)

syn_theme = (keep.groupby("thematique")
             .agg(Aides=("montant", "count"), Organisations=("siren", "nunique"), Montant=("montant", "sum"))
             .reset_index().sort_values("Montant", ascending=False))
syn_theme["% du montant"] = (100 * syn_theme["Montant"] / syn_theme["Montant"].sum()).round(1)

syn_cee = (keep[keep["cee"]].groupby(["thematique", "type"])
           .agg(Aides=("montant", "count"), Beneficiaires=("siren", "nunique"), Montant=("montant", "sum")).reset_index())
def prog_key(d):
    if "AVELO" in d: return "AVELO 1 à 3 (programme CEE)"
    if d.startswith("France 2030 - "): return "France 2030 : projets mobilité non rattachés à un autre dispositif"
    return d
syn_prog = (keep.assign(programme=keep["dispositif"].map(prog_key))
            .groupby("programme").agg(Aides=("montant", "count"), Beneficiaires=("siren", "nunique"),
                                      Montant=("montant", "sum"), CEE=("cee", "any"))
            .reset_index().sort_values("Montant", ascending=False))
syn_prog["CEE"] = syn_prog["CEE"].map({True: "oui", False: ""})
syn_prog["% du montant"] = (100 * syn_prog["Montant"] / syn_prog["Montant"].sum()).round(2)
syn_prog.insert(0, "Rang", range(1, len(syn_prog) + 1))
syn_prog.columns = ["Rang", "Programme / dispositif", "Aides", "Bénéficiaires", "Montant (€)", "Programme CEE", "% du montant"]
syn_reg = (orgs.assign(Région=orgs["Région"].replace("", "Non localisée"))
           .groupby("Région").agg(Organisations=("SIREN", "count"), Montant=("Montant total (€)", "sum"))
           .reset_index().sort_values("Montant", ascending=False))
syn_reg["% du montant"] = (100 * syn_reg["Montant"] / syn_reg["Montant"].sum()).round(2)
syn_reg_hors = (keep[keep["dispositif"].str.contains("Location sociale") == False]
                .assign(region=lambda d: d["siren"].map(dict(zip(orgs["SIREN"], orgs["Région"]))).replace("", "Non localisée"))
                .groupby("region")["montant"].sum())
syn_reg["Montant hors location sociale (€)"] = syn_reg["Région"].map(syn_reg_hors).fillna(0).round(0)
syn_perim = (keep.groupby("perimetre").agg(Aides=("montant", "count"), Montant=("montant", "sum")).reset_index())

detail = keep[["nom", "siren", "siret", "departement", "region", "type", "taille", "portee", "perimetre", "thematique",
               "dispositif", "projet", "date", "montant", "source"]].sort_values(["nom", "date"])
detail.columns = ["Nom", "SIREN", "SIRET", "Département", "Région", "Type", "Taille", "Portée association", "Périmètre", "Thématique",
                  "Dispositif", "Projet (France 2030)", "Date convention", "Montant (€)", "Source"]
excl_out = excl[["nom", "siren", "type", "perimetre", "thematique", "dispositif", "date", "montant", "source"]]
excl_out.columns = ["Nom", "SIREN", "Type", "Motif", "Thématique", "Dispositif", "Date", "Montant (€)", "Source"]

lisez = pd.DataFrame({"Lisez-moi": [
 "Extraction des entreprises et associations financées par l'ADEME dans les mobilités des personnes (hors fret/logistique).",
 "Date d'extraction : 16/11/2026, via le MCP Data ADEME (data.ademe.fr).",
 "Source 1 : 'Les aides financières de l'ADEME' (aides engagées depuis 2021) - https://data.ademe.fr/datasets/les-aides-financieres-de-l'ademe",
 "Source 2 : 'Programmes d'Etat - Bénéficiaires des projets financés par l'ADEME' (France 2030), axes 'Mobilités - véhicules' et 'Avion bas-carbone' - https://data.ademe.fr/datasets/programmes-detat-partenaires-des-projets-finances-par-lademe",
 "Licence : Licence Ouverte / Open Licence (Etalab).",
 "Sélection : dispositifs d'aide liés à la mobilité (vélo, véhicules intermédiaires/XD, recharge, hydrogène mobilité, ferroviaire, services de mobilité, TenMod, AVELO, carburants aviation, maritime...).",
 "Exclusions : dispositifs fret (véhicules lourds E-Trans, XD Logistique, Logistique 4.0, ReMoVe report modal...), lignes dont l'objet est clairement du fret (poids lourds, wagons, livraison), collectivités et organismes publics.",
 "Périmètre 'Mixte / à vérifier' : projets qui servent à la fois personnes et marchandises ou dont l'usage n'est pas précisé (ex. stations hydrogène, carburants aviation, navires, vélos cargo).",
 "Taille d'entreprise : disponible uniquement pour les entreprises présentes dans France 2030 (catégories PME/ETI/GE de l'ADEME ; les TPE sont incluses dans PME). Sinon 'Non renseignée' : à compléter via la base SIRENE.",
 "Type association : code NAF 94 (organisations associatives) ou nom ; la 'portée' (nationale/régionale) est une ESTIMATION à partir du nom.",
 "Doublons : une aide présente dans les deux sources (même SIREN, même montant) n'est comptée qu'une fois.",
 "Source 3 : programmes CEE portés par l'ADEME, repris de 'Les aides financières de l'ADEME' : AVELO 1 à 3 (politiques cyclables), Marche du quotidien, et Location sociale de voitures électriques (programme CEE PRO-INNO-85). Pour ces programmes, TOUS les bénéficiaires sont inclus, collectivités comprises (98 % des aides AVELO / Marche du quotidien vont à des collectivités).",
 "Location sociale (PRO-INNO-85) : l'ADEME verse l'enveloppe à l'Agence de services et de paiement (ASP), qui paie ensuite l'aide aux ménages via les loueurs. Les données ne listent donc qu'un bénéficiaire (ASP, 2 conventions : 350 M€ en 2025 et 380,6 M€ en 2026), pas les loueurs ni les ménages.",
 "Le programme CEE E-Trans (poids lourds, engins) reste exclu car il concerne le fret.",
 "Localisation : département de l'établissement bénéficiaire (SIRET) issu de la base SIRENE jointe par l'ADEME ; pour les collectivités, déduit du SIREN ; pour les projets France 2030, région déclarée dans le jeu 'Programmes d'Etat'. C'est le lieu du siège ou de l'établissement signataire, pas forcément le lieu du projet.",
 "Limite : la pagination du MCP a pu faire perdre quelques lignes (909 lignes récupérées sur 916 dans la source 1).",
]})

out = D + "../ADEME_financements_mobilite_personnes.xlsx"
with pd.ExcelWriter(out, engine="openpyxl") as w:
    lisez.to_excel(w, sheet_name="Lisez-moi", index=False)
    syn_prog.to_excel(w, sheet_name="Plus gros programmes", index=False)
    orgs.to_excel(w, sheet_name="Organisations", index=False)
    syn_type.to_excel(w, sheet_name="Synthèse taille", index=False)
    syn_reg.to_excel(w, sheet_name="Synthèse région", index=False)
    syn_theme.to_excel(w, sheet_name="Synthèse thématique", index=False)
    detail.to_excel(w, sheet_name="Détail des aides", index=False)
    syn_cee.to_excel(w, sheet_name="Synthèse CEE", index=False)
    excl_out.to_excel(w, sheet_name="Exclus", index=False)
    for ws in w.book.worksheets:
        ws.freeze_panes = "A2"
        for col in ws.columns:
            width = min(60, max(10, max(len(str(c.value or "")) for c in col[:200]) + 2))
            ws.column_dimensions[col[0].column_letter].width = width
orgs.to_csv(D + "../organisations_mobilite_personnes.csv", index=False, sep=";", encoding="utf-8-sig")

print("lignes gardées:", len(keep), "| exclues:", len(excl), "| B ajoutées:", len(b_new), "| B doublons:", int(b["doublon_A"].sum()))
print("organisations:", len(orgs))
print(orgs["Type"].value_counts().to_string())
print(orgs["Périmètre"].value_counts().to_string())
print(syn_type.to_string())
print(syn_theme.to_string())
print("TOTAL €", round(orgs["Montant total (€)"].sum()))
print(orgs.head(25)[["Nom", "Type", "Taille (France 2030)", "Périmètre", "Montant total (€)"]].to_string())
print(orgs[orgs["Type"] == "Association / fondation"][["Nom", "Portée association", "Montant total (€)"]].to_string())

# ---------- Données du graphe à bulles + page index.html ----------
import json
MERGE = {"Vélo / véhicules intermédiaires (industrie)": "Vélo & mobilités actives"}
TY = {"Entreprise": "E", "Association / fondation": "A", "Public / collectivité": "C"}
TZ = {"PME (dont TPE)": "PME", "Grande entreprise": "GE", "ETI": "ETI", "Association": "ASSO",
      "Collectivité / public": "COLL", "Non renseignée": "NR"}
k2 = keep.copy()
k2["thematique"] = k2["thematique"].replace(MERGE)
bulles = []
DEP_ORG = dict(zip(orgs["SIREN"], orgs["Département"])); REG_ORG = dict(zip(orgs["SIREN"], orgs["Région"]))
for (sir, th), g in k2.groupby(["siren", "thematique"]):
    disp = g.groupby("dispositif")["montant"].sum().sort_values(ascending=False)
    bulles.append(dict(n=g["nom"].value_counts().index[0], s=str(sir), t=th, ty=TY[g["type"].iloc[0]],
                       z=TZ.get(g["taille"].iloc[0], "NR"), p=g["portee"].iloc[0].replace(" (estimée)", ""),
                       m="M" if (g["flag"] == "M").all() else "P", c=1 if g["cee"].any() else 0,
                       v=round(g["montant"].sum()), k=len(g), dp=DEP_ORG.get(sir, ""), r=REG_ORG.get(sir, ""), d=[[i, round(v)] for i, v in disp.items()]))
data_json = json.dumps(bulles, ensure_ascii=False, separators=(",", ":"))
open(D + "../bulles.json", "w").write(data_json)
tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "carte_template.html")).read()
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "index.html"), "w").write(tpl.replace("__DATA__", data_json))
print("bulles:", len(bulles), "| CEE:", sum(b["c"] for b in bulles))
print(syn_cee.to_string())
print(syn_reg.to_string())
print("orgs localisées:", (orgs["Région"] != "").sum(), "/", len(orgs))
print(syn_prog.head(20).to_string())
