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

Aucun chiffre n'est ici le produit d'un modèle : ce site ne modélise rien, il
compare un système à un autre. Le seul calcul qu'il fait est celui du
simulateur, et il est écrit dans ``moteur/js/simulateur.js``, à ciel ouvert.
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
        if self.fiabilite not in ("publie", "ordre", "verifier"):
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

    detail: list[str] = field(default_factory=list)
    lecon: str = ""


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
        valeur="≈ 14 Md€",
        libelle="de déficit de la branche maladie en un an",
        annee="2024",
        source="Commission des comptes de la sécurité sociale",
        fiabilite="verifier",
        precision="Le déficit de la branche maladie se creuse depuis 2020 sans "
        "qu'aucune loi n'ait prévu son retour à l'équilibre. Le chiffre exact "
        "varie selon qu'on regarde la branche seule ou le régime général avec "
        "le FSV : à vérifier dans le dernier rapport avant citation.",
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
        cle="tsa",
        valeur="13,27 %",
        libelle="de taxe sur votre cotisation de complémentaire santé",
        annee="2025",
        source="Code de la sécurité sociale, art. L.862-4 (TSA)",
        fiabilite="verifier",
        precision="Taux applicable aux contrats dits responsables ; les autres "
        "sont taxés davantage. Une taxe sur une assurance rendue obligatoire "
        "par la loi.",
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
        modele="Assurance de base obligatoire, achetée à des assureurs privés "
        "en concurrence, identique pour tous et sans sélection possible.",
        detail=[
            "Le panier de soins est défini par la loi ; l'assureur ne peut "
            "refuser personne, ni moduler la prime selon l'état de santé.",
            "Une caisse de péréquation des risques verse aux assureurs ce que "
            "coûtent leurs assurés les plus malades : assurer un diabétique "
            "rapporte autant qu'assurer un sportif de vingt ans.",
            "Une franchise universelle d'environ 400 € par an, au-delà de "
            "laquelle tout est pris en charge ; la médecine générale en est "
            "exclue, pour ne pas décourager le premier recours.",
            "Une allocation santé (zorgtoeslag) paie tout ou partie de la "
            "prime des ménages modestes — plusieurs millions de foyers.",
            "Chacun peut changer d'assureur au 1ᵉʳ janvier. Environ un "
            "assuré sur vingt le fait chaque année, ce qui suffit à tenir les "
            "primes.",
        ],
        lecon="C'est la démonstration que concurrence et universalité ne "
        "s'opposent pas : les Pays-Bas couvrent tout le monde, dépensent moins "
        "que la France, et personne n'y est refusé pour son état de santé.",
    ),
    Pays(
        nom="Suisse",
        drapeau="LAMal, 1996",
        depense="≈ 11,5 % du PIB",
        publique="≈ 70 %",
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
        lecon="La franchise choisie est le mécanisme le plus simple jamais "
        "trouvé pour rendre au patient un arbitrage qu'on lui a retiré, sans "
        "toucher au gros risque.",
    ),
    Pays(
        nom="Allemagne",
        drapeau="GKV / PKV",
        depense="≈ 12,5 % du PIB",
        publique="≈ 85 %",
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
        lecon="La concurrence entre caisses ne détruit ni la solidarité ni le "
        "financement par cotisations : elle donne au cotisant le seul pouvoir "
        "qui compte, celui de partir.",
    ),
    Pays(
        nom="Singapour",
        drapeau="MediSave, MediShield Life",
        depense="≈ 5 % du PIB",
        publique="≈ 50 %",
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
        lecon="Un système peut être frugal sans être dur, à condition que le "
        "gros risque soit couvert sans condition et que les prix soient "
        "connus. Il n'est pas transposable tel quel — la démographie et "
        "l'histoire diffèrent — mais il prouve que l'argent dépensé n'est pas "
        "ce qui fait la qualité.",
    ),
)


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
    "taux_csg": 0.092,
    "taux_csg_retraite": 0.083,
    "assiette_csg": 0.9825,
    "part_csg_maladie": 0.55,
    "part_employeur_complementaire": 0.5,
    "participations_annuelles": 100.0,
    "cout_moyen_par_personne": 3700.0,
    "plafond_prime_part_revenu": 0.10,
    "franchise_part_revenu": 0.04,
    "franchise_plafond": 1500.0,
    "depense_moyenne_petit_risque": 450.0,
}

RESERVES_SIMULATEUR: tuple[tuple[str, str], ...] = (
    (
        "part_csg_maladie",
        "La part de la CSG affectée à la branche maladie est fixée chaque "
        "année par la loi de financement et n'est pas un taux stable. La "
        "valeur retenue ici — 55 % — est un ORDRE DE GRANDEUR, à vérifier "
        "dans la dernière LFSS avant d'être citée.",
    ),
    (
        "cout_moyen_par_personne",
        "La prime du système proposé est adossée au coût moyen des soins par "
        "habitant — la CSBM divisée par la population. C'est un chiffre "
        "vérifiable, mais une moyenne : elle ne dit pas ce que coûterait votre "
        "propre contrat, qui dépend du panier retenu et de la péréquation.",
    ),
    (
        "plafond_prime_part_revenu",
        "Le plafond au-delà duquel l'allocation santé prend le relais — 10 % "
        "du revenu — est une HYPOTHÈSE de travail, pas une mesure chiffrée. "
        "Le calibrage réel d'une telle allocation relève d'un modèle "
        "budgétaire que ce dépôt ne contient pas.",
    ),
    (
        "depense_moyenne_petit_risque",
        "La dépense annuelle moyenne de petit risque — consultations, "
        "pharmacie courante, analyses — est très inégalement répartie : la "
        "moitié des assurés dépense beaucoup moins, une minorité beaucoup "
        "plus. Une moyenne ne décrit aucun cas réel.",
    ),
)
