"""Les chiffres du site, et rien qu'eux.

Un site politique se juge à ses chiffres. Celui-ci en cite une centaine : s'ils
étaient écrits dans les pages, personne — ni l'auteur, ni le lecteur, ni le
contradicteur — ne saurait dire d'où ils viennent ni quand ils ont été relevés.
Ils sont donc TOUS ici, chacun avec sa source, son millésime et son degré de
fiabilité, et les pages ne font que les appeler par leur clé.

Trois conséquences, et c'est pour elles que ce module existe :

* un chiffre ne peut pas dériver d'une page à l'autre — il n'existe qu'une
  fois ;
* la page « Données et sources » est ENGENDRÉE par cette table, et ne peut donc
  pas être en retard sur le texte ;
* un chiffre dont la fiabilité est « à vérifier » le dit partout où il paraît,
  et non dans une note de bas de page que personne n'ouvre.

**Sur la fiabilité.** Trois niveaux, et ils sont honnêtes :

``"publie"``
    Chiffre publié tel quel par une source officielle nommée (DREES, CNAM,
    Cour des comptes, OCDE, LFSS). Il est recopié, pas calculé.
``"ordre"``
    Ordre de grandeur : le chiffre est arrondi, agrégé ou reconstitué à partir
    de plusieurs publications. Il dit une magnitude, pas une valeur exacte.
``"verifier"``
    Chiffre de mémoire ou de seconde main, qu'il faut confronter à la source
    avant toute publication ou tout débat. Le site l'affiche en le disant.
``"estime"``
    Chiffre PRODUIT par un calcul de ce dépôt, à partir d'entrées qui sont
    elles-mêmes dans cette table. Il n'est pas publié par une source : il est
    reproductible, ce qui n'est pas la même chose et se dit autrement.

Ce site ne modélise rien : il compare un système à un autre. Il fait deux
calculs, et deux seulement, tous deux à ciel ouvert — celui du simulateur,
dans ``moteur/js/simulateur.js``, et le chiffrage de l'allocation santé, dans
``src/sante/allocation.py``. Leurs résultats portent l'étiquette « estimé » et
jamais « publié ». Un programme qui refuse de chiffrer ses économies ne peut
pas refuser de chiffrer une dépense qu'il crée ; ce qu'il refuse, c'est
d'inventer ce qui exigerait un modèle de comportement.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Chiffre:
    """Un chiffre, ce qu'il mesure, d'où il vient et ce qu'il vaut."""

    cle: str
    valeur: str
    """Le chiffre TEL QU'IL S'ÉCRIT dans la page, unité comprise.

    C'est une chaîne et non un nombre, et c'est voulu : « 8,8 % du PIB »,
    « ≈ 250 Md€ » et « 13,7 millions » ne se formatent pas de la même façon, et
    aucun code de mise en forme ne rattrape un chiffre mal arrondi à la source.
    """

    libelle: str
    """Ce que le chiffre mesure, en une ligne — l'étiquette sous le nombre."""

    annee: str
    source: str
    fiabilite: str = "publie"
    precision: str = ""
    """Ce qu'il faut savoir avant de le citer : périmètre, réserve, définition."""

    lien: str = ""

    def __post_init__(self) -> None:
        if self.fiabilite not in ("publie", "ordre", "verifier", "estime"):
            raise ValueError(f"fiabilité inconnue : {self.fiabilite}")


@dataclass(frozen=True)
class Pays:
    """Un système de santé étranger, tel qu'il se compare au nôtre."""

    nom: str
    drapeau: str
    depense: str
    """Dépense courante de santé, en part du PIB."""

    publique: str
    """Part financée par les régimes publics ou obligatoires."""

    modele: str
    """Le mécanisme, en une phrase."""

    annee: str = ""
    source: str = ""
    fiabilite: str = "verifier"
    """D'où viennent la dépense et la part publique de ce pays.

    Un tableau de comparaison internationale sans millésime ni source est la
    pièce la plus facile à retourner contre celui qui la publie : les
    périmètres comptables diffèrent, les éditions se succèdent, et deux
    chiffres vrais pris dans deux éditions différentes font un tableau faux.
    """

    detail: list[str] = field(default_factory=list)
    lecon: str = ""
    reserve: str = ""
    """Ce qui interdit de lire la ligne de ce pays comme une mesure exacte."""


# -- les chiffres ------------------------------------------------------------
#
# L'ordre est celui de la lecture : ce que le système coûte, comment il est
# financé, ce qu'il produit, ce qu'il coûte à gérer, et ce qui ne marche pas.

CHIFFRES: tuple[Chiffre, ...] = (
    Chiffre(
        cle="csbm",
        valeur="≈ 250 Md€",
        libelle="de soins et de biens médicaux consommés en un an",
        annee="2023",
        source="DREES, « Les dépenses de santé en 2023 », édition 2024",
        fiabilite="ordre",
        precision="La CSBM — consommation de soins et de biens médicaux — est "
        "l'agrégat des soins hospitaliers, des soins de ville, des médicaments "
        "et des autres biens médicaux. Elle vaut environ 8,8 % du PIB.",
        lien="https://drees.solidarites-sante.gouv.fr/publications-communique-de-presse/"
        "panoramas-de-la-drees/les-depenses-de-sante-en-2023",
    ),
    Chiffre(
        cle="dcs_pib",
        valeur="≈ 12 % du PIB",
        libelle="de dépense courante de santé, au sens international",
        annee="2023",
        source="DREES / OCDE, Health at a Glance",
        fiabilite="ordre",
        precision="La DCSi ajoute à la CSBM la prévention, les soins de longue "
        "durée et les coûts de gestion. Elle place la France au troisième ou "
        "quatrième rang de l'OCDE, derrière les États-Unis et l'Allemagne.",
        lien="https://www.oecd.org/health/health-at-a-glance/",
    ),
    Chiffre(
        cle="ocde_moyenne",
        valeur="≈ 9 % du PIB",
        libelle="la moyenne des pays de l'OCDE",
        annee="2023",
        source="OCDE, Health at a Glance 2023",
        fiabilite="ordre",
        precision="Trois points de PIB d'écart avec la France, soit de l'ordre "
        "de 80 milliards d'euros par an.",
        lien="https://www.oecd.org/health/health-at-a-glance/",
    ),
    Chiffre(
        cle="ondam",
        valeur="≈ 265 Md€",
        libelle="d'objectif national de dépenses d'assurance maladie",
        annee="2025",
        source="Loi de financement de la sécurité sociale pour 2025",
        fiabilite="ordre",
        precision="L'ONDAM est un objectif VOTÉ, pas un plafond : il a été "
        "dépassé la plupart des années depuis sa création en 1996, et son "
        "dépassement n'emporte aucune conséquence automatique.",
        lien="https://www.securite-sociale.fr/la-secu-en-detail/comptes-de-la-securite-sociale",
    ),
    Chiffre(
        cle="deficit_maladie",
        valeur="≈ 15,9 Md€",
        libelle="de déficit de la branche maladie en un an",
        annee="2025",
        source="Commission des comptes de la sécurité sociale, rapport 2026",
        fiabilite="ordre",
        precision="13,8 Md€ en 2024, 15,9 Md€ en 2025 : le déficit se creuse "
        "sans qu'aucune loi n'ait prévu son retour à l'équilibre. Le chiffre "
        "dépend du périmètre — branche maladie seule, ou régime général avec "
        "le FSV, dont le solde d'ensemble s'établit à −21,6 Md€ en 2025. "
        "C'est la branche seule qui est citée ici.",
        lien="https://www.securite-sociale.fr/la-secu-en-detail/comptes-de-la-securite-sociale",
    ),
    Chiffre(
        cle="dette_sociale",
        valeur="≈ 100 Md€",
        libelle="de dette sociale restant à rembourser",
        annee="2024",
        source="CADES, rapport annuel",
        fiabilite="verifier",
        precision="La CADES amortit une dette née de dépenses courantes — des "
        "soins consommés il y a dix ou vingt ans, payés par la CRDS "
        "d'aujourd'hui. Montant repris et montant restant diffèrent : à "
        "vérifier dans le dernier rapport.",
        lien="https://www.cades.fr/",
    ),
    Chiffre(
        cle="part_amo",
        valeur="≈ 80 %",
        libelle="de la dépense de soins payée par la Sécurité sociale",
        annee="2023",
        source="DREES, « Les dépenses de santé en 2023 »",
        fiabilite="publie",
        precision="C'est l'un des taux les plus élevés de l'OCDE, et il a "
        "augmenté : la socialisation de la dépense n'a jamais reculé.",
    ),
    Chiffre(
        cle="part_oc",
        valeur="≈ 12,5 %",
        libelle="payés par les complémentaires santé",
        annee="2023",
        source="DREES, « Les dépenses de santé en 2023 »",
        fiabilite="publie",
        precision="Un second étage d'assurance, obligatoire en entreprise "
        "depuis 2016, qui rembourse le solde de ce que le premier a déjà "
        "remboursé — sur les mêmes factures, avec ses propres frais de gestion.",
    ),
    Chiffre(
        cle="reste_a_charge",
        valeur="≈ 7,5 %",
        libelle="restant à la charge des ménages, après les deux étages",
        annee="2023",
        source="DREES, « Les dépenses de santé en 2023 »",
        fiabilite="publie",
        precision="C'est le reste à charge le plus faible de l'OCDE, et c'est "
        "une réussite réelle du système français. Elle ne dit rien de ce que "
        "coûte le prélèvement qui la finance, ni des soins auxquels on renonce "
        "faute de rendez-vous plutôt que faute d'argent.",
    ),
    Chiffre(
        cle="part_publique_france",
        valeur="≈ 85 %",
        libelle="de la dépense de santé financée par les régimes publics et "
        "obligatoires",
        annee="2023",
        source="OCDE, Health at a Glance ; DREES",
        fiabilite="ordre",
        precision="À ne pas confondre avec les ≈ 80 % remboursés par la "
        "Sécurité sociale : la statistique internationale ajoute à l'assurance "
        "maladie obligatoire les complémentaires que la loi rend obligatoires. "
        "C'est ce chiffre-là, et non l'autre, qui se compare aux parts "
        "publiques néerlandaise, suisse ou allemande.",
    ),
    Chiffre(
        cle="frais_gestion_oc",
        valeur="≈ 7,6 Md€",
        libelle="de frais de gestion des complémentaires en un an",
        annee="2021",
        source="DREES, « La complémentaire santé » ; Cour des comptes, 2021",
        fiabilite="verifier",
        precision="De l'ordre de 20 % des cotisations sur les contrats "
        "individuels, davantage que les frais de gestion de l'assurance "
        "maladie obligatoire rapportés aux mêmes prestations. Le chiffre est "
        "de seconde main : à confronter au dernier panorama de la DREES.",
        lien="https://drees.solidarites-sante.gouv.fr/",
    ),
    Chiffre(
        cle="frais_gestion_amo",
        valeur="≈ 7,3 Md€",
        libelle="de frais de gestion de l'assurance maladie obligatoire",
        annee="2023",
        source="Cour des comptes ; DREES, comptes de la santé",
        fiabilite="verifier",
        precision="À mettre en regard des frais du second étage, et non à "
        "oublier : fusionner les deux étages ne supprime pas la gestion, il "
        "supprime le doublon. Additionnés, les deux étages placent la France "
        "au deuxième rang de l'OCDE pour le coût de gestion de son système de "
        "santé, derrière les États-Unis — c'est l'argument, et il tient "
        "précisément parce qu'on cite les deux chiffres.",
    ),
    Chiffre(
        cle="tsa",
        valeur="15,27 %",
        libelle="de taxe sur votre cotisation de complémentaire santé",
        annee="2025",
        source="Code de la sécurité sociale, art. L.862-4 (TSA) ; LFSS 2025",
        fiabilite="publie",
        precision="Taux applicable aux contrats dits responsables depuis la "
        "loi de financement pour 2025, qui l'a porté de 13,27 % à 15,27 % ; "
        "les contrats non responsables sont taxés davantage. Une taxe sur une "
        "assurance rendue obligatoire par la loi — et une taxe dont le "
        "rendement finance la complémentaire santé solidaire.",
    ),
    Chiffre(
        cle="rendement_tsa",
        valeur="≈ 6,5 Md€",
        libelle="de recettes tirées de la taxe sur les complémentaires",
        annee="2025",
        source="Annexes de la loi de financement de la sécurité sociale",
        fiabilite="verifier",
        precision="Cette taxe finance la complémentaire santé solidaire. "
        "Supprimer l'étage complémentaire supprime aussi cette recette : une "
        "réforme qui le propose doit dire par quoi elle la remplace, sous "
        "peine de déplacer le trou plutôt que de le combler. Chiffre de "
        "seconde main : à confronter à la dernière annexe avant citation.",
    ),
    Chiffre(
        cle="ald",
        valeur="≈ 13,7 millions",
        libelle="de personnes en affection de longue durée",
        annee="2023",
        source="CNAM, cartographie des pathologies et des dépenses",
        fiabilite="ordre",
        precision="Un Français sur cinq. Le dispositif ALD concentre environ "
        "les deux tiers des remboursements de l'assurance maladie : c'est le "
        "vrai cœur de la dépense, et la vraie raison d'assurer le gros risque.",
        lien="https://data.ameli.fr/",
    ),
    Chiffre(
        cle="sans_medecin",
        valeur="≈ 6 millions",
        libelle="de personnes sans médecin traitant",
        annee="2023",
        source="CNAM ; ministère de la Santé",
        fiabilite="verifier",
        precision="Dont plusieurs centaines de milliers de patients en "
        "affection de longue durée. Sans médecin traitant, le parcours de "
        "soins coordonné — celui qui conditionne le remboursement normal — "
        "devient inapplicable.",
    ),
    Chiffre(
        cle="zones_sous_denses",
        valeur="≈ 1 Français sur 3",
        libelle="vit dans une zone où l'accès au médecin est sous-dense",
        annee="2023",
        source="DREES, indicateur d'accessibilité potentielle localisée (APL)",
        fiabilite="verifier",
        precision="L'APL mesure les consultations disponibles par habitant et "
        "par an, en tenant compte du temps de trajet et de l'âge des "
        "praticiens. Le seuil de sous-densité retenu fait varier la part : à "
        "vérifier avant citation.",
        lien="https://drees.solidarites-sante.gouv.fr/",
    ),
    Chiffre(
        cle="medecins",
        valeur="≈ 3,3 pour 1 000",
        libelle="médecins en activité par habitant",
        annee="2023",
        source="OCDE, Health at a Glance ; Ordre des médecins, atlas",
        fiabilite="ordre",
        precision="Contre environ 4,5 en Allemagne et 4,4 en Suisse. La France "
        "dépense davantage que ses voisins et forme moins de médecins : les "
        "deux faits se tiennent, et c'est le numerus clausus qui les relie.",
    ),
    Chiffre(
        cle="numerus",
        valeur="3 500 places",
        libelle="le plancher du numerus clausus, au milieu des années 1990",
        annee="1993",
        source="Ministère de la Santé, arrêtés annuels du numerus clausus",
        fiabilite="ordre",
        precision="Instauré en 1971 à environ 8 500 places, abaissé jusqu'à "
        "environ 3 500 au début des années 1990, remonté ensuite, remplacé en "
        "2021 par un « numerus apertus ». Un médecin se forme en dix ans : la "
        "pénurie de 2026 a été décidée en 1993.",
    ),
    Chiffre(
        cle="urgences",
        valeur="≈ 21 millions",
        libelle="de passages aux urgences en un an",
        annee="2023",
        source="DREES, enquête nationale sur les structures des urgences",
        fiabilite="ordre",
        precision="Deux fois plus qu'au début des années 2000. Les urgences "
        "sont devenues la porte d'entrée par défaut du système, faute de "
        "médecine de ville disponible aux heures où l'on tombe malade.",
    ),
    Chiffre(
        cle="delai_ophtalmo",
        valeur="52 jours",
        libelle="de délai médian pour un rendez-vous chez l'ophtalmologue",
        annee="2018",
        source="DREES, enquête Délais d'attente, Études et Résultats n° 1085",
        fiabilite="publie",
        precision="Deux jours chez le généraliste, 52 jours en médiane chez "
        "l'ophtalmologue — et un écart territorial considérable, de l'ordre de "
        "46 jours en Île-de-France contre 118 en région Centre-Val de Loire. "
        "C'est la dernière enquête nationale de ce type : les délais se sont "
        "aggravés depuis, mais aucun relevé officiel comparable ne le mesure, "
        "et c'est une raison de plus de publier ces délais.",
        lien="https://drees.solidarites-sante.gouv.fr/sources-outils-et-enquetes/"
        "lenquete-delais-dattente",
    ),
    Chiffre(
        cle="esperance_vie",
        valeur="85,7 et 80,0 ans",
        libelle="espérance de vie à la naissance, femmes et hommes",
        annee="2024",
        source="INSEE, bilan démographique",
        fiabilite="ordre",
        precision="Parmi les meilleures d'Europe. Aucune réforme proposée ici "
        "ne doit dégrader ce résultat : c'est l'étalon auquel elle se juge.",
        lien="https://www.insee.fr/",
    ),
    Chiffre(
        cle="prelevements",
        valeur="≈ 43 % du PIB",
        libelle="de prélèvements obligatoires, le plus haut taux de l'UE",
        annee="2024",
        source="INSEE ; Eurostat",
        fiabilite="ordre",
        precision="La santé en est le premier poste avec les retraites. Un "
        "système qui dépense trois points de PIB de plus que ses voisins pour "
        "des résultats comparables prélève ces trois points sur le travail.",
    ),
    Chiffre(
        cle="cotisation_employeur",
        valeur="7 % ou 13 %",
        libelle="de cotisation maladie employeur sur votre salaire brut",
        annee="2025",
        source="URSSAF, barème des cotisations",
        fiabilite="publie",
        precision="7 % jusqu'à 2,5 SMIC annuels, 13 % sur la totalité du "
        "salaire au-delà de ce seuil. Cette somme ne figure pas dans votre "
        "salaire net : elle est prélevée avant, sur ce que votre travail "
        "rapporte.",
        lien="https://www.urssaf.fr/",
    ),
    Chiffre(
        cle="csg",
        valeur="9,2 %",
        libelle="de CSG sur 98,25 % de votre salaire brut",
        annee="2025",
        source="Code de la sécurité sociale, art. L.136-8",
        fiabilite="publie",
        precision="La CSG finance la maladie, la famille, l'autonomie et la "
        "dette sociale. La part qui revient à la branche maladie est fixée par "
        "la loi de financement, et change d'une année à l'autre.",
    ),
    Chiffre(
        cle="cout_moyen",
        valeur="≈ 3 700 €",
        libelle="de soins consommés par personne et par an, en moyenne",
        annee="2023",
        source="Calcul : CSBM (DREES) rapportée à la population (INSEE)",
        fiabilite="ordre",
        precision="C'est la CSBM divisée par la population résidente. Une "
        "moyenne ne décrit aucun cas réel : la moitié des assurés consomme "
        "beaucoup moins, et les 5 % les plus malades concentrent près de la "
        "moitié de la dépense. C'est précisément ce qui rend l'assurance "
        "nécessaire — et ce que la prime moyenne, dans le système proposé, "
        "mutualise.",
    ),
    Chiffre(
        cle="prime_pays_bas",
        valeur="≈ 1 900 € par an",
        libelle="de prime d'assurance de base aux Pays-Bas",
        annee="2026",
        source="Consumentenbond ; Zorgwijzer, primes 2026",
        fiabilite="verifier",
        precision="Environ 159 € par mois, franchise universelle de 385 € en "
        "sus. La hausse de 2026 est la plus forte depuis la réforme de 2006 : "
        "la concurrence entre assureurs discipline le service et la gestion, "
        "elle n'annule pas la dérive du coût des soins. Le dire nous-mêmes "
        "vaut mieux que se le faire opposer.",
    ),
    Chiffre(
        cle="contribution_pays_bas",
        valeur="6,10 %",
        libelle="de contribution employeur assise sur le revenu, aux Pays-Bas",
        annee="2026",
        source="Belastingdienst, inkomensafhankelijke bijdrage Zvw",
        fiabilite="publie",
        precision="Plafonnée à un revenu de 79 409 € par an. La loi "
        "néerlandaise fixe ces taux de sorte que les contributions assises sur "
        "le revenu représentent LA MOITIÉ des ressources de l'assurance de "
        "base ; la prime nominale n'en finance que l'autre moitié. Un modèle "
        "néerlandais présenté comme une prime seule n'est pas le modèle "
        "néerlandais.",
    ),
    Chiffre(
        cle="population",
        valeur="68,6 millions",
        libelle="d'habitants en France",
        annee="2025",
        source="INSEE, bilan démographique",
        fiabilite="publie",
        precision="Au 1ᵉʳ janvier 2025, dont 66,4 millions en France "
        "métropolitaine et 2,3 millions dans les cinq départements d'outre-mer.",
        lien="https://www.insee.fr/fr/statistiques/8719824",
    ),
    Chiffre(
        cle="mineurs",
        valeur="≈ 14,5 millions",
        libelle="de personnes de moins de 18 ans",
        annee="2025",
        source="INSEE, bilan démographique",
        fiabilite="ordre",
        precision="Près de 21 % de la population. Aucune d'elles ne paie de "
        "prime dans le système proposé : c'est ce chiffre qui fixe le nombre "
        "d'adultes redevables, et donc ce que les primes peuvent rapporter.",
        lien="https://www.insee.fr/fr/statistiques/8719824",
    ),
    Chiffre(
        cle="niveau_vie_median",
        valeur="26 740 €",
        libelle="de niveau de vie annuel médian",
        annee="2024",
        source="INSEE, distribution des niveaux de vie",
        fiabilite="publie",
        precision="Le niveau de vie est le revenu disponible du ménage divisé "
        "par ses unités de consommation. Le premier décile s'établit à "
        "13 970 € et le neuvième à 48 580 €. C'est cette distribution, décile "
        "par décile, qui sert d'assiette au chiffrage de l'allocation santé.",
        lien="https://www.insee.fr/fr/statistiques/2416808",
    ),
    Chiffre(
        cle="point_csg",
        valeur="≈ 17,5 Md€",
        libelle="ce que rapporte un point de CSG",
        annee="2024",
        source="Sécurité sociale, évaluation des politiques de sécurité sociale",
        fiabilite="ordre",
        precision="La CSG a rapporté 153,8 Md€ en 2024, dont 67 % sur les "
        "revenus d'activité, 22 % sur les revenus de remplacement et 11 % sur "
        "le patrimoine et les placements. Le point de CSG est l'unité dans "
        "laquelle se compte tout financement social en France : c'est donc "
        "dans cette unité que le coût de l'allocation santé est exprimé.",
        lien="https://evaluation.securite-sociale.fr/home/financement/"
        "1-4-1-valeur-du-point-de-csg-et.html",
    ),
    Chiffre(
        cle="zorgtoeslag",
        valeur="≈ 6,5 Md€",
        libelle="ce que coûte l'allocation santé néerlandaise en un an",
        annee="2025",
        source="Dienst Toeslagen, aantallen en bedragen",
        fiabilite="verifier",
        precision="Versée à 4,76 millions de foyers sur 18 millions "
        "d'habitants, soit environ 360 € par habitant et par an. C'est le seul "
        "instrument comparable dont le coût soit publié : un chiffrage "
        "français qui s'en écarterait d'un ordre de grandeur serait à refaire.",
        lien="https://www.overtoeslagen.nl/over-ons-werk/aantallen-en-bedragen",
    ),
    Chiffre(
        cle="aides_complementaire",
        valeur="≈ 10 Md€",
        libelle="de dépenses publiques déjà consacrées à la couverture "
        "complémentaire",
        annee="2021",
        source="Cour des comptes, rapport sur les complémentaires santé",
        fiabilite="verifier",
        precision="Dont environ 3 Md€ d'exonérations de cotisations sociales "
        "sur la part employeur des contrats collectifs, la complémentaire "
        "santé solidaire, et la déduction de l'impôt sur les bénéfices. "
        "L'allocation santé ne s'ajoute pas à ces dépenses : elle les "
        "remplace, et son coût NET est l'écart entre les deux. Chiffre de "
        "seconde main et daté : à reprendre dans le dernier rapport.",
    ),
    Chiffre(
        cle="c2s",
        valeur="≈ 3,2 Md€",
        libelle="de dépense nette de complémentaire santé solidaire",
        annee="2023",
        source="Rapport annuel de la complémentaire santé solidaire",
        fiabilite="verifier",
        precision="Pour 7,45 millions de bénéficiaires, soit 13 % des "
        "assurés. C'est le dispositif que l'allocation santé absorbe, et dont "
        "elle élargit considérablement le champ.",
        lien="https://www.complementaire-sante-solidaire.gouv.fr/",
    ),
    Chiffre(
        cle="participation",
        valeur="2 € et 1 €",
        libelle="de participation forfaitaire par consultation et par boîte",
        annee="2024",
        source="Décrets du 15 février 2024",
        fiabilite="publie",
        precision="Plafonnées à 50 € par an chacune. C'est aujourd'hui le seul "
        "mécanisme de responsabilisation du système, et il est forfaitaire : "
        "il pèse autant sur un SMIC que sur un très haut revenu.",
    ),
)

# -- les chiffres tolérés sans rangée ----------------------------------------
#
# La règle du site est qu'un chiffre porte sa source. Quelques-uns n'ont pas de
# rangée à eux sans être pour autant des affirmations : une borne de formulaire,
# une tournure comme « 100 % du gros risque », un chiffre qu'on cite pour le
# réfuter. Ils sont ici, un par un, avec la raison — et le témoin
# ``test_aucun_chiffre_orphelin`` refuse tous les autres. C'est cette liste, et
# non la bonne volonté du rédacteur, qui empêche un chiffre de se glisser dans
# une page sans qu'on sache d'où il vient.
CHIFFRES_TOLERES: dict[str, str] = {
    "100 %": "Tournure, et non mesure : « 100 % du gros risque couvert », "
             "« 100 % du tarif Sécu ». Désigne l'intégralité d'une prise en "
             "charge, pas un relevé statistique.",
    "30 milliards": "Cité entre guillemets pour être RÉFUTÉ — c'est le type "
                    "d'économie annoncée que ce programme refuse d'avancer.",
    "50 €": "Plafond annuel des participations forfaitaires et des franchises "
            "médicales, pris de la rangée « participation » où il figure avec "
            "son décret.",
    "300 €": "Borne du choix de franchise offert par le formulaire du "
             "simulateur, comme 600 € et 1 200 € : une saisie, pas une mesure.",
    "600 €": "Borne du choix de franchise offert par le formulaire.",
    "200 €": "Fin de « 1 200 € », troisième borne du choix de franchise.",
}


PAR_CLE: dict[str, Chiffre] = {chiffre.cle: chiffre for chiffre in CHIFFRES}


def chiffre(cle: str) -> Chiffre:
    """Le chiffre de clé donnée. Une clé inconnue est une erreur de rédaction."""
    if cle not in PAR_CLE:
        raise KeyError(f"chiffre inconnu : {cle} (voir src/sante/donnees.py)")
    return PAR_CLE[cle]


def valeur(cle: str) -> str:
    """Le chiffre seul, pour l'écrire au fil d'une phrase."""
    return chiffre(cle).valeur


# -- les pays comparés -------------------------------------------------------
#
# Quatre, et c'est un choix. Ce sont les quatre systèmes qui assurent une
# couverture universelle SANS monopole public de l'assurance, c'est-à-dire les
# seuls qui renseignent sur la question posée par ce site. Les États-Unis n'y
# sont pas : personne ne les propose ici, et les citer servirait à faire peur,
# pas à comprendre.

PAYS: tuple[Pays, ...] = (
    Pays(
        nom="Pays-Bas",
        drapeau="Zorgverzekeringswet, 2006",
        depense="≈ 10 % du PIB",
        publique="≈ 85 %",
        annee="2023",
        source="OCDE, Système de comptes de la santé ; Zorginstituut Nederland "
        "(mécanisme)",
        fiabilite="verifier",
        modele="Assurance de base obligatoire, achetée à des assureurs privés "
        "en concurrence, identique pour tous et sans sélection possible.",
        detail=[
            "Le panier de soins est défini par la loi ; l'assureur ne peut "
            "refuser personne, ni moduler la prime selon l'état de santé.",
            "Une caisse de péréquation des risques verse aux assureurs ce que "
            "coûtent leurs assurés les plus malades : assurer un diabétique "
            "rapporte autant qu'assurer un sportif de vingt ans.",
            "Une franchise universelle de 385 € par an — inchangée depuis "
            "2016 — au-delà de laquelle tout est pris en charge ; la "
            "médecine générale en est exclue, pour ne pas décourager le "
            "premier recours.",
            "Une allocation santé (zorgtoeslag) paie tout ou partie de la "
            "prime des ménages modestes — plusieurs millions de foyers.",
            "<strong>La prime nominale ne finance que la moitié du "
            "système.</strong> L'autre moitié vient d'une contribution "
            "assise sur le revenu, prélevée par l'employeur ("
            + valeur("contribution_pays_bas") + " en 2026, plafonnée), qui "
            "alimente la caisse de péréquation. La loi fixe les taux pour que "
            "le partage reste à 50-50. C'est la pièce que les présentations "
            "françaises du modèle néerlandais oublient le plus souvent, et "
            "c'est elle qui porte la progressivité.",
            "Les mineurs ne paient aucune prime : l'État verse la leur au "
            "fonds. Une famille de quatre ne paie donc pas quatre primes.",
            "Chacun peut changer d'assureur au 1ᵉʳ janvier. Environ un "
            "assuré sur vingt le fait chaque année, ce qui suffit à "
            "discipliner le service et les frais de gestion. Cela ne suspend "
            "pas la dérive du coût des soins : la prime de base ("
            + valeur("prime_pays_bas") + ") connaît en 2026 sa plus forte "
            "hausse depuis la réforme de 2006, et il vaut mieux le dire que "
            "se le faire opposer.",
        ],
        reserve="Dépense et part publique recopiées de seconde main : elles "
        "doivent être confrontées à UNE SEULE édition de Health at a "
        "Glance avant toute reprise publique — la même pour les cinq "
        "lignes du tableau.",
        lecon="C'est la démonstration que concurrence et universalité ne "
        "s'opposent pas : les Pays-Bas couvrent tout le monde, dépensent moins "
        "que la France, et personne n'y est refusé pour son état de santé. "
        "Ce n'est pas la démonstration qu'une prime forfaitaire suffit à "
        "financer un système de santé — aux Pays-Bas, elle n'en finance que "
        "la moitié.",
    ),
    Pays(
        nom="Suisse",
        drapeau="LAMal, 1996",
        depense="≈ 11,5 % du PIB",
        publique="≈ 70 %",
        annee="2023",
        source="OCDE, Système de comptes de la santé ; Office fédéral de la "
        "santé publique (LAMal)",
        fiabilite="verifier",
        modele="Assurance obligatoire individuelle auprès de l'assureur de son "
        "choix, avec franchise choisie par l'assuré.",
        detail=[
            "La franchise annuelle se choisit entre environ 300 et 2 500 "
            "francs : plus elle est haute, plus la prime baisse. L'assuré "
            "arbitre lui-même entre prime et risque.",
            "Une réduction de prime, versée par les cantons, couvre les "
            "ménages modestes — de l'ordre d'un quart de la population.",
            "Les délais d'attente sont parmi les plus courts d'Europe et la "
            "densité médicale parmi les plus élevées.",
            "La prime est la même pour tous à l'intérieur d'un canton et d'une "
            "classe d'âge : l'assureur ne peut pas trier ses clients sur le "
            "risque.",
            "Le reste à charge y est plus élevé qu'en France, et c'est la "
            "critique principale du modèle : il faut la regarder en face.",
        ],
        reserve="Même réserve, et elle mord ici : selon l'édition retenue, la "
        "Suisse dépense un peu moins ou un peu plus que la France. La "
        "phrase « trois de ces pays dépensent moins que nous » dépend "
        "donc de l'édition, et ne doit pas être avancée sans elle.",
        lecon="La franchise choisie est le mécanisme le plus simple jamais "
        "trouvé pour rendre au patient un arbitrage qu'on lui a retiré, sans "
        "toucher au gros risque.",
    ),
    Pays(
        nom="Allemagne",
        drapeau="GKV / PKV",
        depense="≈ 12,5 % du PIB",
        publique="≈ 85 %",
        annee="2023",
        source="OCDE, Système de comptes de la santé ; Bundesministerium für "
        "Gesundheit (GKV)",
        fiabilite="verifier",
        modele="Une centaine de caisses d'assurance maladie en concurrence, "
        "entre lesquelles chaque assuré choisit librement.",
        detail=[
            "Les caisses sont des organismes de droit public, mais elles se "
            "font concurrence sur la cotisation additionnelle, le service et "
            "les programmes de prévention.",
            "Changer de caisse prend quelques minutes et n'exige aucun motif.",
            "Au-delà d'un certain revenu, un assuré peut quitter le régime "
            "public pour une assurance privée — environ un Allemand sur dix.",
            "L'Allemagne compte nettement plus de médecins et de lits par "
            "habitant que la France, et n'a jamais pratiqué de numerus clausus "
            "aussi restrictif.",
        ],
        reserve="Même réserve. L'Allemagne dépense davantage que la France dans "
        "toutes les éditions récentes : c'est l'exemple qui porte sur "
        "la concurrence entre caisses, jamais sur le coût.",
        lecon="La concurrence entre caisses ne détruit ni la solidarité ni le "
        "financement par cotisations : elle donne au cotisant le seul pouvoir "
        "qui compte, celui de partir.",
    ),
    Pays(
        nom="Singapour",
        drapeau="MediSave, MediShield Life",
        depense="≈ 5 % du PIB",
        publique="≈ 50 %",
        annee="2022",
        source="Ministry of Health Singapore ; Banque mondiale",
        fiabilite="verifier",
        modele="Comptes d'épargne santé individuels pour le petit risque, "
        "assurance obligatoire pour le gros, filet public pour les démunis.",
        detail=[
            "Chacun épargne une part de son revenu sur un compte santé "
            "personnel, qui lui appartient et se transmet.",
            "MediShield Life couvre les hospitalisations lourdes, avec "
            "franchise et co-assurance ; MediFund prend le relais pour ceux "
            "qui ne peuvent pas payer.",
            "Les prix des actes hospitaliers sont publiés, établissement par "
            "établissement : le patient sait ce qu'il paie avant de choisir.",
            "Les résultats de santé — espérance de vie, mortalité infantile — "
            "sont parmi les meilleurs du monde, pour moitié moins de dépense "
            "que la France.",
        ],
        reserve="Périmètre non aligné sur le Système de comptes de la santé de "
        "l'OCDE, population beaucoup plus jeune, épargne santé "
        "obligatoire comptée à part : la part de PIB singapourienne ne "
        "se compare pas terme à terme à la française.",
        lecon="Un système peut être frugal sans être dur, à condition que le "
        "gros risque soit couvert sans condition et que les prix soient "
        "connus. Il n'est pas transposable tel quel — la démographie et "
        "l'histoire diffèrent — mais il prouve que l'argent dépensé n'est pas "
        "ce qui fait la qualité.",
    ),
)


# -- les entrées du chiffrage de l'allocation --------------------------------
#
# Elles ne paraissent pas telles quelles dans une page — ce sont des nombres de
# calcul, pas des arguments — mais elles portent leur source comme les autres,
# et ``src/sante/allocation.py`` ne lit rien d'autre.

POPULATION = 68_600_000.0
"""INSEE, bilan démographique 2025 — voir le chiffre ``population``."""

MINEURS = 14_500_000.0
"""INSEE, bilan démographique 2025 — voir le chiffre ``mineurs``."""

DEPENSE_TOTALE = 250_000_000_000.0
"""DREES, CSBM 2023 — voir le chiffre ``csbm``."""

DECILES_NIVEAU_VIE: tuple[float, ...] = (
    9_960.0, 15_890.0, 19_400.0, 22_430.0, 25_310.0,
    28_290.0, 31_670.0, 36_040.0, 43_010.0, 76_970.0,
)
"""Niveau de vie annuel MOYEN de chacun des dix déciles, en euros.

INSEE, « Niveau de vie moyen par décile », édition 2024, euros constants 2024.
Le niveau de vie est le revenu disponible du ménage — après impôts et
transferts — divisé par ses unités de consommation.
"""

UNITES_COUPLE = 1.5
"""Unités de consommation d'un couple, échelle d'équivalence OCDE modifiée.

1 pour le premier adulte, 0,5 par personne de 14 ans ou plus. C'est ce
coefficient qui fait qu'une allocation assise sur le foyer coûte PLUS qu'une
allocation assise sur la personne : deux primes pour une fois et demie le
revenu.
"""

RENDEMENT_POINT_CSG = 17_500_000_000.0
"""Ce que rapporte un point de CSG — voir le chiffre ``point_csg``."""

ZORGTOESLAG_COUT = 6_520_000_000.0
"""Dienst Toeslagen, exercice 2025 — voir le chiffre ``zorgtoeslag``."""

POPULATION_PAYS_BAS = 18_000_000.0
"""Ordre de grandeur, Centraal Bureau voor de Statistiek."""

DEPENSE_PUBLIQUE_COMPLEMENTAIRE = 10_000_000_000.0
"""Cour des comptes — voir le chiffre ``aides_complementaire``."""


# -- les paramètres du simulateur --------------------------------------------
#
# Ils sont ici pour la même raison que les chiffres : le simulateur tourne dans
# le navigateur, mais ses hypothèses se lisent, se discutent et se recopient
# dans la page Données. Elles ne sont écrites qu'une fois, et
# ``scripts/construire_site.py`` les dépose dans ``moteur/donnees.json``.

PARAMETRES_SIMULATEUR: dict[str, object] = {
    "smic_brut_mensuel": 1802.0,
    "seuil_taux_plein_smic": 2.5,
    "taux_maladie_reduit": 0.07,
    "taux_maladie_plein": 0.13,
    "taux_maladie_independant": 0.065,
    "seuil_independant_smic": 1.1,
    "taux_csg": 0.092,
    "taux_csg_retraite": 0.083,
    "assiette_csg": 0.9825,
    "part_csg_maladie": 0.55,
    "part_employeur_complementaire": 0.5,
    "participations_annuelles": 100.0,
    "cout_moyen_par_personne": 3700.0,
    "part_prime_nominale": 0.5,
    "part_franchise_rendue": 0.6,
    "plafond_prime_part_revenu": 0.08,
    "franchise_part_revenu": 0.04,
    "franchise_plafond": 1500.0,
    "depense_moyenne_petit_risque": 450.0,
}

# Deux paramètres manquent à cette table, et c'est voulu : la PRIME et le TAUX
# DE CONTRIBUTION ne sont pas des choix, ce sont des conséquences. La prime est
# la part de la dépense que la loi laisse au second étage, rapportée aux
# adultes qui la paient ; le taux est ce qu'il reste à lever une fois
# l'allocation déduite. Les deux se calculent dans ``allocation.py``, et
# ``allocation.parametres()`` rend la table complète — celle que le navigateur
# lit et que la page Données publie.
#
# Ils ont été écrits à la main, et les deux étaient faux : la prime était calée
# sur le coût par HABITANT alors que les mineurs n'en versent aucune, et le
# taux était un chiffre rond posé avant tout calcul. Les déduire est le seul
# moyen que l'erreur ne revienne pas.

# Ce que chaque paramètre représente, et l'unité dans laquelle il s'écrit. La
# page « Données et sources » est ENGENDRÉE à partir de ces deux tables : un
# paramètre ajouté au calcul sans description casse la construction, et ne peut
# donc pas rester invisible. Un simulateur dont une hypothèse ne figure pas
# dans la page qui prétend les donner toutes n'est pas vérifiable.
DESCRIPTIONS_SIMULATEUR: dict[str, tuple[str, str]] = {
    "smic_brut_mensuel": ("euros", "SMIC brut mensuel, qui sert de référence "
                          "au seuil de la cotisation employeur"),
    "seuil_taux_plein_smic": ("smic", "Seuil, en SMIC annuels, au-delà duquel "
                              "le taux plein s'applique à la totalité du "
                              "salaire"),
    "taux_maladie_reduit": ("part", "Cotisation maladie employeur jusqu'à ce "
                            "seuil"),
    "taux_maladie_plein": ("part", "Cotisation maladie employeur au-delà de ce "
                           "seuil"),
    "taux_maladie_independant": ("part", "Cotisation maladie-maternité des "
                                 "indépendants, haut de la fourchette "
                                 "progressive <strong>(ordre de "
                                 "grandeur)</strong>"),
    "seuil_independant_smic": ("smic", "Seuil, en SMIC annuels, à partir "
                               "duquel cette cotisation est due"),
    "taux_csg": ("part", "CSG sur les revenus d'activité"),
    "taux_csg_retraite": ("part", "CSG sur les pensions, au taux normal"),
    "assiette_csg": ("part", "Part du brut soumise à la CSG"),
    "part_csg_maladie": ("part", "Fraction de la CSG affectée à la branche "
                         "maladie <strong>(ordre de grandeur)</strong>"),
    "part_employeur_complementaire": ("part", "Part minimale payée par "
                                      "l'employeur en contrat collectif"),
    "participations_annuelles": ("euros", "Participations forfaitaires et "
                                 "franchises médicales, plafonds cumulés"),
    "cout_moyen_par_personne": ("euros", "Coût moyen des soins par habitant, "
                                "sur lequel les deux étages du financement "
                                "sont adossés"),
    "part_prime_nominale": ("part", "Part de ce coût portée par la prime "
                            "versée à l'assureur ; le reste est porté par la "
                            "contribution assise sur le revenu. C'est le "
                            "partage néerlandais <strong>(hypothèse de "
                            "travail)</strong>"),
    "prime_nominale": ("euros", "Prime annuelle avant allocation. "
                       "<strong>Déduite</strong> : cette part de la dépense "
                       "rapportée aux seuls adultes qui la paient, les "
                       "mineurs n'en versant aucune"),
    "taux_contribution_revenu": ("part", "Taux de la contribution santé, "
                                 "assis sur la même assiette que la CSG. "
                                 "<strong>Déduit</strong> : c'est ce qu'il "
                                 "reste à lever une fois les primes "
                                 "encaissées, rapporté au rendement du point "
                                 "de CSG"),
    "part_franchise_rendue": ("part", "Part de la franchise choisie qui est "
                              "rendue en baisse de prime <strong>(hypothèse de "
                              "travail)</strong>"),
    "plafond_prime_part_revenu": ("part", "Part du revenu au-delà de laquelle "
                                  "l'allocation santé prend en charge la "
                                  "prime. Porté de 5 % à 8 % après chiffrage "
                                  "<strong>(hypothèse de travail)</strong>"),
    "franchise_part_revenu": ("part", "Plafond de reste à charge annuel, en "
                              "part du revenu <strong>(hypothèse de "
                              "travail)</strong>"),
    "franchise_plafond": ("euros", "Plafond de reste à charge annuel, en "
                          "valeur absolue <strong>(hypothèse de "
                          "travail)</strong>"),
    "depense_moyenne_petit_risque": ("euros", "Dépense annuelle moyenne de "
                                     "petit risque par assuré <strong>(ordre "
                                     "de grandeur)</strong>"),
}


def _francais(nombre: float, decimales: int) -> str:
    texte = f"{nombre:,.{decimales}f}".replace(",", "\u202f").replace(".", ",")
    return texte.rstrip("0").rstrip(",") if decimales else texte


def formater_parametre(cle: str, valeur: float) -> str:
    """La valeur d'un paramètre, TELLE QU'ELLE SE LIT dans la page.

    Elle est mise en forme depuis le paramètre lui-même, et non recopiée : une
    valeur recopiée à la main dans un tableau est une valeur qui finira par
    dire autre chose que le calcul — c'est arrivé, et c'est la raison de cette
    fonction. Elle prend la valeur en argument plutôt que d'aller la chercher,
    parce que deux des paramètres ne sont pas dans cette table : ils sont
    déduits, et ``allocation.parametres()`` les porte.
    """
    unite = DESCRIPTIONS_SIMULATEUR[cle][0]
    if unite == "part":
        return _francais(valeur * 100, 2) + "\u202f%"
    if unite == "euros":
        return _francais(valeur, 0) + "\u202f€"
    return _francais(valeur, 2) + "\u202fSMIC"

RESERVES_SIMULATEUR: tuple[tuple[str, str], ...] = (
    (
        "part_csg_maladie",
        "La part de la CSG affectée à la branche maladie est fixée chaque "
        "année par la loi de financement et n'est pas un taux stable. La "
        "valeur retenue ici — 55 % — est un ORDRE DE GRANDEUR, à vérifier "
        "dans la dernière LFSS avant d'être citée.",
    ),
    (
        "part_prime_nominale",
        "Le partage entre la prime versée à l'assureur et la contribution "
        "assise sur le revenu est LE choix politique de cette réforme, et non "
        "un paramètre technique. La valeur retenue — moitié-moitié — est celle "
        "que la loi néerlandaise impose. Plus la part de la prime est élevée, "
        "plus le financement pèse également sur tous, quel que soit le "
        "revenu ; plus elle est basse, moins la concurrence entre assureurs a "
        "de prise. Il n'existe pas de valeur techniquement juste : il existe "
        "une valeur qu'on assume.",
    ),
    (
        "taux_contribution_revenu",
        "Ce taux n'est plus posé, il est DÉDUIT : c'est ce qu'il reste à "
        "lever une fois les primes encaissées, rapporté au rendement d'un "
        "point de CSG. Il suppose donc que la contribution ait l'assiette de "
        "la CSG — revenus d'activité, de remplacement ET du capital. Une "
        "assiette plus étroite exigerait un taux plus élevé, et c'est la "
        "question que la loi tranche, pas le calcul.",
    ),
    (
        "cout_moyen_par_personne",
        "Le financement du système proposé est adossé au coût moyen des soins "
        "par habitant — la CSBM divisée par la population. C'est un chiffre "
        "vérifiable, mais une moyenne : elle ne dit pas ce que coûterait votre "
        "propre contrat, qui dépend du panier retenu et de la péréquation.",
    ),
    (
        "plafond_prime_part_revenu",
        "Le plafond au-delà duquel l'allocation santé prend le relais est une "
        "HYPOTHÈSE de travail, mais elle n'est plus arbitraire : elle a été "
        "portée de 5 % à 8 % du revenu après chiffrage. À 5 %, l'allocation "
        "touchait quatre adultes sur cinq et bornait ce que les primes "
        "peuvent rapporter au tiers de la dépense, rendant le partage "
        "moitié-moitié arithmétiquement impossible. À 8 %, elle redevient "
        "finançable sans cesser de couvrir les revenus modestes — c'est le "
        "réglage le plus protecteur qui tienne l'arithmétique. Le barème "
        "complet est publié, et le calcul est dans src/sante/allocation.py.",
    ),
    (
        "depense_moyenne_petit_risque",
        "La dépense annuelle moyenne de petit risque — consultations, "
        "pharmacie courante, analyses — est très inégalement répartie : la "
        "moitié des assurés dépense beaucoup moins, une minorité beaucoup "
        "plus. Une moyenne ne décrit aucun cas réel.",
    ),
)
