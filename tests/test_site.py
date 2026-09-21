"""Ce que le site doit vérifier de lui-même.

    python3 -m unittest discover -s tests

Aucune dépendance : ces témoins n'utilisent que la bibliothèque standard, comme
le script de construction. Ils ne jugent pas la mise en forme — un navigateur
seul sait la juger — mais ce qu'un site de programme politique ne peut pas se
permettre de rater : un chiffre sans source, un onglet qui mène nulle part, une
page engendrée qui a divergé de son texte.
"""

from __future__ import annotations

import html
import pathlib
import re
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "src"))
sys.path.insert(0, str(RACINE / "scripts"))

from sante import allocation, donnees, gabarit  # noqa: E402
import construire_site  # noqa: E402


def code_seul(source: str) -> str:
    """Le JavaScript débarrassé de ses commentaires, chaînes et littéraux.

    Un nombre dans une phrase — « plafonnés à 50 € par an » — est un mot ; un
    nombre dans une expression est une hypothèse, et une hypothèse doit venir
    de ``donnees.py``. Les distinguer demande de lire le fichier caractère par
    caractère : une expression régulière se déphase sur ``/[&<>"\']/g``, dont
    l'apostrophe ouvre une chaîne qui n'existe pas.
    """
    sortie, i, n = [], 0, len(source)
    precedent = ""
    while i < n:
        c = source[i]
        suivant = source[i + 1] if i + 1 < n else ""
        if c == "/" and suivant == "/":
            i = source.find("\n", i)
            if i == -1:
                break
        elif c == "/" and suivant == "*":
            i = source.find("*/", i) + 2
        elif c in "\"'`":
            i += 1
            while i < n and source[i] != c:
                i += 2 if source[i] == "\\" else 1
            i += 1
            sortie.append(' "" ')
        elif c == "/" and precedent in "(,=:[!&|?{};" :
            # Un littéral d'expression régulière, et non une division : ce qui
            # précède ne peut pas être la fin d'une valeur.
            i += 1
            while i < n and source[i] != "/":
                if source[i] == "\\":
                    i += 1
                elif source[i] == "[":
                    while i < n and source[i] != "]":
                        i += 2 if source[i] == "\\" else 1
                i += 1
            i += 1
            sortie.append(" // ")
        else:
            sortie.append(c)
            if not c.isspace():
                precedent = c
            i += 1
    return "".join(sortie)


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


class ChiffresOrphelins(unittest.TestCase):
    """Aucun nombre ne doit paraître dans une page sans qu'on sache d'où il vient.

    Le site promet que « les chiffres n'existent qu'une fois », dans la table
    de ``donnees.py``. Le témoin précédent vérifie le sens facile : que tout
    chiffre déclaré paraît sur la page Données. Il ne vérifiait pas l'autre, le
    seul qui protège vraiment — qu'aucun chiffre écrit au fil d'une phrase
    n'échappe à la table. C'est par là qu'un « six mois pour un rendez-vous »
    s'était glissé en tête de la page d'accueil, sans source et sans date.
    """

    MOTIF = re.compile(
        r"\d[\d\u202f\u00a0]*(?:,\d+)?\s?(?:%|Md€|€|millions?|milliards?)")

    @classmethod
    def normaliser(cls, texte: str) -> str:
        return re.sub(r"[\u202f\u00a0\s]+", " ", texte).strip()

    def chiffres_connus(self) -> set[str]:
        """Tout ce qui, dans ``donnees.py``, est écrit à côté de sa source.

        Les valeurs déclarées, bien sûr — mais aussi les nombres qui paraissent
        dans une précision, une réserve ou le détail d'un pays : ceux-là sont
        écrits DANS la table, sur la rangée qui porte la source, et la page
        Données les publie avec elle.
        """
        textes = [chiffre.valeur for chiffre in donnees.CHIFFRES]
        textes += [chiffre.precision for chiffre in donnees.CHIFFRES]
        for pays in donnees.PAYS:
            textes += [pays.depense, pays.publique, pays.modele, pays.lecon,
                       pays.reserve, *pays.detail]
        textes += [texte for _, texte in donnees.RESERVES_SIMULATEUR]
        textes += [donnees.parametre_affiche(cle)
                   for cle in donnees.PARAMETRES_SIMULATEUR]
        textes += [chiffre.valeur for chiffre in allocation.chiffres_calcules().values()]
        textes += [chiffre.precision
                   for chiffre in allocation.chiffres_calcules().values()]
        textes += list(allocation.LIMITES)
        textes += [str(valeur) for ligne in allocation.bareme_plafond()
                   for valeur in ligne.values()]
        textes += list(donnees.CHIFFRES_TOLERES)
        return {self.normaliser(trouve.group(0))
                for texte in textes for trouve in self.MOTIF.finditer(texte)}

    def test_aucun_chiffre_orphelin(self) -> None:
        connus = self.chiffres_connus()
        for fichier, *_ in construire_site.PAGES:
            brut = (RACINE / fichier).read_text(encoding="utf-8")
            # Les balises deviennent des sauts de ligne et non des espaces :
            # sinon le rang « 03 » d'une carte et le « 100 % » qui le suit se
            # recollent en un nombre qui n'a jamais été écrit.
            texte = html.unescape(re.sub(r"<[^>]+>", "\n", brut))
            for trouve in self.MOTIF.finditer(texte):
                chiffre_lu = self.normaliser(trouve.group(0))
                with self.subTest(page=fichier, chiffre=chiffre_lu):
                    self.assertIn(
                        chiffre_lu, connus,
                        f"{fichier} écrit « {chiffre_lu} » sans que ce chiffre "
                        "figure dans src/sante/donnees.py. Lui donner une "
                        "rangée avec sa source, ou l'inscrire dans "
                        "CHIFFRES_TOLERES avec la raison.",
                    )

    def test_chaque_tolerance_est_justifiee_et_sert(self) -> None:
        """Une tolérance sans raison, ou devenue inutile, doit disparaître."""
        pages = "\n".join(
            html.unescape(re.sub(r"<[^>]+>", "\n",
                                 (RACINE / fichier).read_text(encoding="utf-8")))
            for fichier, *_ in construire_site.PAGES)
        vus = {self.normaliser(trouve.group(0))
               for trouve in self.MOTIF.finditer(pages)}
        for chiffre_lu, raison in donnees.CHIFFRES_TOLERES.items():
            with self.subTest(chiffre=chiffre_lu):
                self.assertTrue(raison.strip(), "tolérance sans justification")
                self.assertIn(self.normaliser(chiffre_lu), vus,
                              "tolérance qui ne sert plus : la retirer")


class ChiffresCalcules(unittest.TestCase):
    """Un chiffre que ce dépôt produit doit dire qu'il le produit.

    C'est la seule entorse du site à sa règle — « il ne modélise rien » — et
    elle n'est tenable qu'à une condition : que le résultat porte l'étiquette
    « estimé », que sa méthode soit publiée, et qu'il ne se glisse jamais dans
    la table des chiffres recopiés d'une source officielle.
    """

    def test_aucun_chiffre_calcule_ne_se_fait_passer_pour_publie(self) -> None:
        cles_publiees = {chiffre.cle for chiffre in donnees.CHIFFRES}
        for cle, chiffre in allocation.chiffres_calcules().items():
            with self.subTest(chiffre=cle):
                self.assertEqual(chiffre.fiabilite, "estime")
                self.assertNotIn(cle, cles_publiees)
                self.assertIn("allocation.py", chiffre.source)

    def test_chaque_chiffre_calcule_parait_avec_sa_methode(self) -> None:
        page = (RACINE / "donnees.html").read_text(encoding="utf-8")
        for cle, chiffre in allocation.chiffres_calcules().items():
            with self.subTest(chiffre=cle):
                self.assertIn(f'id="{cle}"', page)
                self.assertIn(chiffre.precision, page)
        self.assertIn("scripts/cout_allocation.py", page)

    def test_le_bareme_designe_le_reglage_retenu(self) -> None:
        """Le tableau des réglages doit montrer lequel le programme applique.

        Un barème qui n'indique pas la ligne choisie donne l'impression que
        tout se vaut, et laisse le lecteur croire qu'on lui cache laquelle.
        """
        lignes = allocation.bareme_plafond()
        retenues = [ligne for ligne in lignes if ligne["retenu"]]
        self.assertEqual(len(retenues), 1)
        page = (RACINE / "reforme.html").read_text(encoding="utf-8")
        for ligne in lignes:
            with self.subTest(plafond=ligne["plafond"]):
                self.assertIn(str(ligne["cout"]), page)

    def test_le_chiffrage_lit_la_prime_du_simulateur(self) -> None:
        """Le chiffrage et le calcul du navigateur doivent lire le même nombre.

        Sans quoi le coût publié resterait celui d'une prime que le simulateur
        n'applique plus.
        """
        self.assertEqual(allocation.prime_pleine(),
                         float(donnees.PARAMETRES_SIMULATEUR["prime_nominale"]))

    def test_le_repere_etranger_confirme_l_ordre_de_grandeur(self) -> None:
        """Le coût calculé doit rester du même ORDRE que le seul comparable.

        Pas égal : l'allocation proposée est volontairement plus serrée que le
        zorgtoeslag, et un écart du simple au double est un choix, pas une
        faute. Un écart d'un facteur trois, en revanche, voudrait dire que le
        calcul ou ses entrées sont à refaire — c'est cela que ce témoin garde.
        """
        calcule = allocation.chiffrer("personne").cout
        repere = allocation.repere_neerlandais()
        self.assertLess(max(calcule, repere) / min(calcule, repere), 3.0,
                        "le coût calculé s'écarte d'un facteur trois du "
                        "zorgtoeslag transposé : refaire le calcul")

    def test_la_prime_est_deduite_et_non_saisie(self) -> None:
        """La prime doit lever la part du financement que la loi lui assigne.

        C'est la faute que le chiffrage a trouvée : une prime calée sur le coût
        moyen par HABITANT ne peut pas lever sa part, puisque les mineurs n'en
        paient aucune. Le paramètre est désormais déduit ; ce témoin est là
        pour qu'il le reste.
        """
        adultes = donnees.POPULATION - donnees.MINEURS
        attendu = (float(donnees.PARAMETRES_SIMULATEUR["part_prime_nominale"])
                   * donnees.DEPENSE_TOTALE)
        self.assertAlmostEqual(allocation.prime_pleine() * adultes,
                               attendu, delta=attendu * 0.001)

    def test_le_partage_voulu_par_la_loi_reste_atteignable(self) -> None:
        """Le plafond ne doit pas interdire le partage que les garanties visent.

        Au-delà d'un certain montant de prime, tout le monde est au plafond et
        chaque euro ajouté est repris par l'allocation : ce que les primes
        peuvent rapporter est borné. Si cette borne passe sous la moitié de la
        dépense, la sixième garantie devient impossible à tenir — ce qui était
        le cas avant le chiffrage, et ne doit plus le redevenir.
        """
        self.assertGreaterEqual(allocation.encaissement_maximal(),
                                donnees.DEPENSE_TOTALE / 2,
                                "à ce plafond, les primes ne peuvent pas "
                                "porter la moitié du financement")


class Comparaisons(unittest.TestCase):
    """Un pays comparé engage autant qu'un chiffre : mêmes exigences."""

    def test_chaque_pays_porte_sa_source_sa_date_et_sa_reserve(self) -> None:
        for pays in donnees.PAYS:
            with self.subTest(pays=pays.nom):
                self.assertTrue(pays.annee.strip())
                self.assertTrue(pays.source.strip())
                self.assertTrue(pays.reserve.strip())
                self.assertIn(pays.fiabilite, ("publie", "ordre", "verifier"))

    def test_la_page_montre_ces_sources(self) -> None:
        page = (RACINE / "comparaisons.html").read_text(encoding="utf-8")
        for pays in donnees.PAYS:
            with self.subTest(pays=pays.nom):
                self.assertIn(pays.source, page)
                self.assertIn(pays.reserve, page)


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

    def test_chaque_parametre_est_decrit(self) -> None:
        """Un paramètre sans description ne peut pas paraître dans la page."""
        self.assertEqual(set(donnees.PARAMETRES_SIMULATEUR),
                         set(donnees.DESCRIPTIONS_SIMULATEUR))

    def test_chaque_parametre_parait_dans_la_page_donnees(self) -> None:
        """La page prétend donner TOUTES les hypothèses : qu'elle les donne.

        Elle en taisait la moitié, et en annonçait une — un taux de prime de
        9 % — que le calcul n'employait pas. Le tableau est désormais engendré
        depuis la table des paramètres ; ce témoin est là pour qu'il le reste.
        """
        page = (RACINE / "donnees.html").read_text(encoding="utf-8")
        for cle in donnees.PARAMETRES_SIMULATEUR:
            with self.subTest(parametre=cle):
                self.assertIn(f"<code>{cle}</code>", page)
                self.assertIn(gabarit.echapper(donnees.parametre_affiche(cle)),
                              page)

    def test_le_calcul_n_emploie_aucun_nombre_qui_lui_soit_propre(self) -> None:
        """Le simulateur ne doit contenir aucune hypothèse écrite en dur.

        Une constante écrite dans le JavaScript ne paraît nulle part, ne se
        discute pas, et dément la page qui prétend publier les hypothèses.
        """
        source = (RACINE / "moteur" / "js" / "simulateur.js").read_text(
            encoding="utf-8")
        code = code_seul(source)
        # Les seuls nombres admis sont ceux de la mise en forme et des bornes
        # neutres : 0, 1, 12 mois, 100 pour un pourcentage.
        admis = {"0", "1", "12", "100", "2", "3"}
        for nombre_lu in re.findall(r"(?<![\w.])\d+(?:\.\d+)?", code):
            with self.subTest(nombre=nombre_lu):
                self.assertIn(nombre_lu, admis,
                              f"le simulateur emploie {nombre_lu} sans que ce "
                              "nombre vienne de moteur/donnees.json")


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
