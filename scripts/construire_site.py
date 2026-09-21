#!/usr/bin/env python3
"""Écrit le site : sept pages HTML, et le paquet de données du simulateur.

    python3 scripts/construire_site.py

Rien à installer : le script n'utilise que la bibliothèque standard, et écrit
à la racine du dépôt les fichiers que GitHub Pages sert tels quels. Les pages
engendrées ne doivent jamais être corrigées à la main — la construction
suivante effacerait la correction. Le texte est dans ``src/sante/pages.py``,
les chiffres dans ``src/sante/donnees.py``.
"""

from __future__ import annotations

import json
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "src"))

from sante import allocation, donnees, gabarit, pages  # noqa: E402  (après sys.path)

# Chaque page : son fichier, son titre d'onglet, sa description pour les
# moteurs de recherche et les aperçus de partage, et la fonction qui l'écrit.
# L'ordre est celui de la navigation.
PAGES = (
    ("index.html",
     "Santé : le programme du Parti libéral français",
     "Le système de santé français coûte trois points de PIB de plus que la "
     "moyenne des pays riches et ne trouve plus de médecin pour six millions "
     "de personnes. Notre programme : un seul assureur par facture, le choix "
     "de sa caisse, le gros risque couvert à 100 %, et plus de médecins.",
     pages.programme),
    ("diagnostic.html",
     "Le système de santé actuel — ce qu'il coûte, ce qui ne marche pas",
     "Comment fonctionne l'assurance maladie française, ce qu'elle coûte, et "
     "les six défauts qui se tiennent : prix invisibles, doublon de gestion, "
     "pénurie organisée, hôpital piloté par circulaire, déficit structurel, "
     "rationnement par l'attente.",
     pages.diagnostic),
    ("comparaisons.html",
     "Ailleurs : quatre systèmes universels sans monopole",
     "Pays-Bas, Suisse, Allemagne, Singapour : quatre pays couvrent toute "
     "leur population avec des assureurs en concurrence, sans que personne y "
     "soit refusé pour son état de santé.",
     pages.comparaisons),
    ("reforme.html",
     "La réforme, en six mesures",
     "Un seul assureur par facture, le libre choix de sa caisse, un bouclier "
     "sanitaire, une franchise plutôt qu'un forfait, plus de médecins libres "
     "de s'installer, des prix et des résultats publics.",
     pages.reforme),
    ("simulateur.html",
     "Ce que la santé vous coûte vraiment — le simulateur",
     "Cotisation maladie de l'employeur, part de CSG, complémentaire, "
     "participations : quatre prélèvements, dont trois invisibles. Le "
     "simulateur les additionne dans votre navigateur, sans rien envoyer "
     "nulle part.",
     pages.simulateur),
    ("objections.html",
     f"Les {pages.nombre_objections()} objections, y compris les bonnes",
     "Privatisation, sélection des risques, prime forfaitaire, enfants à "
     "charge, renoncement aux soins, absence de chiffrage : les "
     f"{pages.nombre_objections()} objections les plus sérieuses à ce "
     "programme, et nos réponses — y compris quand elles sont incomplètes.",
     pages.objections),
    ("donnees.html",
     "Données et sources",
     "Tous les chiffres cités sur ce site, avec leur source, leur millésime "
     "et leur degré de fiabilité — publié, ordre de grandeur, ou à vérifier.",
     pages.page_donnees),
)

# Le simulateur est la seule page qui charge un second module : les autres se
# lisent sans JavaScript, et doivent continuer de le faire.
SCRIPTS = {
    "simulateur.html": '\n<script type="module" src="moteur/js/simulateur.js"></script>',
}


def paquet_donnees() -> dict[str, object]:
    """Ce que le simulateur lit au chargement : ses paramètres et ses réserves.

    Il est écrit depuis ``donnees.py`` et ``allocation.py`` pour la même raison
    que le reste : une hypothèse qui vaut 9 % dans la page Données et 10 %
    dans le calcul ne serait découverte par personne. La table écrite ici est
    la COMPLÈTE — les paramètres saisis, plus les deux que le chiffrage en
    déduit.
    """
    return {
        "avertissement": "Écrit par scripts/construire_site.py depuis "
                         "src/sante/donnees.py. Ne pas modifier à la main.",
        "parametres": allocation.parametres(),
        "reserves": [
            {"parametre": cle, "texte": texte}
            for cle, texte in donnees.RESERVES_SIMULATEUR
        ],
    }


def construire() -> int:
    ecrits = 0
    for fichier, titre, description, rendu in PAGES:
        corps = rendu()
        html = gabarit.page(fichier, titre, description, corps,
                            SCRIPTS.get(fichier, ""))
        (RACINE / fichier).write_text(html, encoding="utf-8")
        print(f"  {fichier:22} {len(html):>7} octets")
        ecrits += 1

    chemin = RACINE / "moteur" / "donnees.json"
    chemin.write_text(
        json.dumps(paquet_donnees(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"  {'moteur/donnees.json':22} {chemin.stat().st_size:>7} octets")

    # Les pages de la navigation et les pages construites doivent être les
    # mêmes : un onglet qui pointe vers un fichier qui n'existe pas est une
    # erreur qu'aucun test d'apparence ne rattrape.
    manquantes = set(gabarit.PAGES) - {fichier for fichier, *_ in PAGES}
    if manquantes:
        raise SystemExit(f"navigation vers des pages non construites : {manquantes}")

    print(f"\n{ecrits} pages écrites dans {RACINE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(construire())
