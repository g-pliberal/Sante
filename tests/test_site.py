"""Ce que le site doit vérifier de lui-même.

    python3 -m unittest discover -s tests

Aucune dépendance : ces témoins n'utilisent que la bibliothèque standard, comme
le script de construction. Ils ne jugent pas la mise en forme — un navigateur
seul sait la juger — mais ce qu'un site de programme politique ne peut pas se
permettre de rater : un chiffre sans source, un onglet qui mène nulle part, une
page engendrée qui a divergé de son texte.
"""

from __future__ import annotations

import pathlib
import re
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "src"))
sys.path.insert(0, str(RACINE / "scripts"))

from sante import donnees, gabarit  # noqa: E402
import construire_site  # noqa: E402


class PagesEngendrees(unittest.TestCase):
    """Les fichiers HTML du dépôt sont-ils bien ceux que le script écrirait ?

    C'est le seul témoin qui compte vraiment : une correction faite à la main
    dans une page engendrée survit jusqu'à la construction suivante, puis
    disparaît sans bruit. Mieux vaut qu'elle échoue tout de suite.
    """

    def test_le_html_du_depot_est_a_jour(self) -> None:
        for fichier, titre, description, rendu in construire_site.PAGES:
            with self.subTest(page=fichier):
                attendu = gabarit.page(
                    fichier, titre, description, rendu(),
                    construire_site.SCRIPTS.get(fichier, ""),
                )
                trouve = (RACINE / fichier).read_text(encoding="utf-8")
                self.assertEqual(
                    attendu, trouve,
                    f"{fichier} a divergé de son texte : relancer "
                    "python3 scripts/construire_site.py",
                )


class Navigation(unittest.TestCase):
    def test_chaque_onglet_mene_a_une_page_existante(self) -> None:
        for chemin in gabarit.PAGES:
            with self.subTest(page=chemin):
                self.assertTrue((RACINE / chemin).exists())

    def test_chaque_lien_interne_mene_quelque_part(self) -> None:
        """Aucun lien du site ne doit pointer vers un fichier absent.

        Les ancres ne sont vérifiées que pour la page Données, la seule dont
        les identifiants soient engendrés à partir d'une table plutôt
        qu'écrits à la main.
        """
        fichiers = {fichier for fichier, *_ in construire_site.PAGES}
        for fichier in fichiers:
            texte = (RACINE / fichier).read_text(encoding="utf-8")
            for cible in re.findall(r'href="([^"#:]+\.html)(?:#[^"]*)?"', texte):
                with self.subTest(page=fichier, cible=cible):
                    self.assertIn(cible, fichiers)

    def test_les_ancres_de_la_page_donnees_existent(self) -> None:
        donnees_html = (RACINE / "donnees.html").read_text(encoding="utf-8")
        identifiants = set(re.findall(r'id="([^"]+)"', donnees_html))
        for fichier, *_ in construire_site.PAGES:
            texte = (RACINE / fichier).read_text(encoding="utf-8")
            for ancre in re.findall(r'href="donnees\.html#([^"]+)"', texte):
                with self.subTest(page=fichier, ancre=ancre):
                    self.assertIn(ancre, identifiants)


class Chiffres(unittest.TestCase):
    def test_chaque_chiffre_a_une_source_et_une_annee(self) -> None:
        for chiffre in donnees.CHIFFRES:
            with self.subTest(chiffre=chiffre.cle):
                self.assertTrue(chiffre.source.strip())
                self.assertTrue(chiffre.annee.strip())
                self.assertTrue(chiffre.libelle.strip())

    def test_les_cles_sont_uniques(self) -> None:
        cles = [chiffre.cle for chiffre in donnees.CHIFFRES]
        self.assertEqual(len(cles), len(set(cles)))

    def test_tous_les_chiffres_paraissent_sur_la_page_donnees(self) -> None:
        """Un chiffre qu'on ne peut pas vérifier n'a rien à faire sur le site."""
        donnees_html = (RACINE / "donnees.html").read_text(encoding="utf-8")
        for chiffre in donnees.CHIFFRES:
            with self.subTest(chiffre=chiffre.cle):
                self.assertIn(f'id="{chiffre.cle}"', donnees_html)

    def test_les_chiffres_a_verifier_le_disent(self) -> None:
        """La mention « à vérifier » doit être VISIBLE, sur la bonne rangée.

        Chercher le mot quelque part dans la page ne prouverait rien : il
        suffirait qu'un seul chiffre le porte. C'est la rangée du chiffre qui
        doit le dire, et c'est elle qu'on lit ici.
        """
        donnees_html = (RACINE / "donnees.html").read_text(encoding="utf-8")
        rangees = re.findall(r"<tr>.*?</tr>", donnees_html, re.S)
        for chiffre in donnees.CHIFFRES:
            if chiffre.fiabilite != "verifier":
                continue
            with self.subTest(chiffre=chiffre.cle):
                rangee = next((r for r in rangees
                               if f'id="{chiffre.cle}"' in r), None)
                self.assertIsNotNone(rangee)
                self.assertIn("À vérifier", rangee)


class Simulateur(unittest.TestCase):
    def test_les_parametres_du_json_sont_ceux_du_module(self) -> None:
        """Le taux affiché et le taux appliqué doivent être le même nombre."""
        import json

        paquet = json.loads(
            (RACINE / "moteur" / "donnees.json").read_text(encoding="utf-8"))
        self.assertEqual(paquet["parametres"], donnees.PARAMETRES_SIMULATEUR)

    def test_chaque_reserve_porte_sur_un_parametre_existant(self) -> None:
        for cle, _ in donnees.RESERVES_SIMULATEUR:
            with self.subTest(parametre=cle):
                self.assertIn(cle, donnees.PARAMETRES_SIMULATEUR)


class RessourcesTierces(unittest.TestCase):
    """Le site ne doit rien demander à un serveur qui n'est pas le sien.

    Une police, une feuille de style ou un script chargés ailleurs emportent
    l'adresse IP du lecteur. La page du simulateur promet le contraire en
    toutes lettres : ce témoin est là pour que la promesse reste vraie.
    """

    def test_aucune_ressource_externe(self) -> None:
        motif = re.compile(
            r'(?:src|href)="(https?://[^"]+)"|@import\s+url\(([^)]+)\)')
        for fichier, *_ in construire_site.PAGES:
            texte = (RACINE / fichier).read_text(encoding="utf-8")
            for balise in re.findall(
                    r'<(?:script|link)\b[^>]*>', texte):
                with self.subTest(page=fichier, balise=balise[:80]):
                    self.assertIsNone(motif.search(balise))


if __name__ == "__main__":
    unittest.main()
