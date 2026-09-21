"""Ce que coûterait l'allocation santé, et ce qu'elle coûte en points.

Ce module est une EXCEPTION assumée à la règle du site — « ce site ne modélise
rien » — et il faut dire pourquoi elle est faite, sans quoi elle en abîmerait
la discipline plutôt que de la servir.

Un programme qui refuse de chiffrer ses économies ne peut pas refuser de
chiffrer une dépense qu'il crée : l'allocation santé est la seule dépense
nouvelle de cette réforme, et « elle coûte combien ? » est une question à
laquelle il faut savoir répondre en direct. Le refus de chiffrer vaut pour ce
qui exige un modèle de comportement — l'élasticité de la dépense de soins au
reste à charge, la réaction des offreurs. Il ne vaut pas pour une somme
d'arithmétique sur une distribution publiée.

Ce calcul est donc ce qu'il prétend être, et rien de plus :

* ses ENTRÉES sont dans ``donnees.py``, chacune avec sa source et sa date ;
* sa MÉTHODE tient en trente lignes, lisibles ici ;
* son RÉSULTAT porte l'étiquette « estimé », qui n'est ni « publié » ni
  « ordre de grandeur » : il dit qu'un calcul de ce dépôt l'a produit, et que
  relancer ``python3 scripts/cout_allocation.py`` le refait ;
* ses LIMITES sont écrites dans ``LIMITES``, et elles sont sérieuses.

Ce que le calcul fait. L'allocation plafonne la prime à une part du revenu :
elle vaut donc ``max(0, prime − taux × revenu)`` pour chaque adulte. Il suffit
de sommer cette fonction sur la distribution des revenus, que l'INSEE publie
par décile. Il n'y a pas de modèle là-dedans : il y a une soustraction, faite
dix fois.
"""

from __future__ import annotations

from dataclasses import dataclass

from . import donnees


@dataclass(frozen=True)
class Chiffrage:
    """Le coût de l'allocation sous une assiette donnée, et ses conséquences."""

    assiette: str
    taux_effectif: float
    """Part du revenu au-delà de laquelle l'allocation cesse, ramenée à l'adulte."""

    allocation_moyenne: float
    """Allocation annuelle moyenne par adulte, zéros compris."""

    cout: float
    """Coût annuel total, en euros."""

    adultes_aides: float
    """Part des adultes qui touchent quelque chose."""

    a_lever: float
    """Ce que la contribution assise sur le revenu doit lever, en euros."""

    points_csg: float
    """Le même montant, exprimé en points de CSG — l'unité du débat français."""

    part_prime_due: float
    """Part du financement que les primes porteraient si personne n'était aidé."""

    part_prime_reelle: float
    """Part du financement que les assurés versent VRAIMENT de leur poche.

    C'est le nombre que la réforme doit surveiller. La prime est le seul étage
    qu'un assuré peut emporter ailleurs : plus l'allocation en paie, moins il
    reste de levier à la concurrence. Une allocation trop large ne coûte pas
    seulement de l'argent — elle désarme le mécanisme qu'elle sert.
    """


# -- les limites, avant les résultats ----------------------------------------
#
# Elles viennent en tête et non en note de bas de page, parce qu'un chiffrage
# dont on ignore les limites est exactement ce que ce site reproche aux autres.

LIMITES: tuple[str, ...] = (
    "Les déciles de l'INSEE portent sur le NIVEAU DE VIE — le revenu "
    "disponible du ménage par unité de consommation, après impôts et "
    "transferts. Une allocation assise sur le revenu fiscal ne porterait pas "
    "sur la même assiette : le revenu fiscal est plus élevé que le revenu "
    "disponible, et le coût réel serait donc plus BAS que celui calculé ici.",
    "Les déciles comptent des personnes, mineurs compris, et les déciles "
    "modestes comptent plus d'enfants que les autres. Répartir les adultes "
    "également entre les dix déciles surestime donc le nombre d'adultes dans "
    "le bas de la distribution, là où l'allocation est la plus forte : le "
    "coût calculé ici est à ce titre un MAJORANT.",
    "La moyenne d'un décile n'est pas le décile : à l'intérieur du neuvième, "
    "où le plafond mord, une partie des personnes touche encore quelque chose "
    "que ce calcul ignore. L'effet joue en sens inverse du précédent, et il "
    "est plus petit.",
    "Ce que la contribution doit lever est exprimé en POINTS DE CSG, unité "
    "dont le rendement est publié. Le simulateur, lui, applique son taux au "
    "seul revenu brut de l'assuré, qui est une assiette plus étroite : les "
    "deux nombres ne se comparent pas terme à terme, et réconcilier l'un à "
    "l'autre demande de savoir ce que la loi ferait entrer dans l'assiette — "
    "les revenus du capital, notamment.",
    "Aucun effet de comportement n'est pris en compte, et il n'y en a pas "
    "besoin : une allocation qui plafonne un prix ne change pas la "
    "distribution des revenus la première année.",
)


def prime_pleine() -> float:
    """La prime avant allocation : la part du coût moyen que la loi lui laisse."""
    parametres = donnees.PARAMETRES_SIMULATEUR
    return (float(parametres["cout_moyen_par_personne"])  # type: ignore[arg-type]
            * float(parametres["part_prime_nominale"]))  # type: ignore[arg-type]


def _taux_effectif(assiette: str) -> float:
    """Le plafond, ramené à ce qu'il vaut par adulte selon l'assiette retenue.

    Sur une assiette INDIVIDUELLE, c'est le plafond tel quel : chaque adulte
    compare sa prime à une part de son propre revenu.

    Sur une assiette de FOYER, il faut le corriger, et la correction surprend.
    Un couple doit deux primes ; l'échelle d'équivalence de l'OCDE lui compte
    1,5 unité de consommation. Rapporter deux primes à 1,5 fois le niveau de
    vie revient à un plafond de 3,75 % par adulte au lieu de 5 % : l'assiette
    de foyer est donc PLUS généreuse que l'assiette individuelle, et non
    l'inverse. C'est le contraire de l'intuition, et c'est la raison pour
    laquelle ce module calcule les deux.
    """
    plafond = float(
        donnees.PARAMETRES_SIMULATEUR["plafond_prime_part_revenu"])  # type: ignore[arg-type]
    if assiette == "personne":
        return plafond
    if assiette == "foyer":
        return plafond * donnees.UNITES_COUPLE / 2
    raise ValueError(f"assiette inconnue : {assiette}")


def chiffrer(assiette: str = "personne") -> Chiffrage:
    """Le coût annuel de l'allocation, et le taux de contribution qu'il exige."""
    prime = prime_pleine()
    taux = _taux_effectif(assiette)
    deciles = donnees.DECILES_NIVEAU_VIE

    allocations = [max(0.0, prime - taux * niveau) for niveau in deciles]
    moyenne = sum(allocations) / len(allocations)
    aides = sum(1 for montant in allocations if montant > 0) / len(allocations)

    adultes = donnees.POPULATION - donnees.MINEURS
    cout = moyenne * adultes

    # Ce que la contribution doit lever : la dépense totale, moins ce que les
    # primes rapportent RÉELLEMENT — c'est-à-dire les primes dues par les
    # adultes, diminuées de ce que l'allocation paie à leur place.
    # Les primes sont dues par les ADULTES, tandis que le coût moyen est par
    # HABITANT. Multiplier l'un par l'autre ne donne donc pas la moitié de la
    # dépense, et c'est un écart que le paramétrage doit regarder en face.
    primes_dues = adultes * prime
    primes_encaissees = primes_dues - cout
    a_lever = donnees.DEPENSE_TOTALE - primes_encaissees

    return Chiffrage(
        assiette=assiette,
        taux_effectif=taux,
        allocation_moyenne=moyenne,
        cout=cout,
        adultes_aides=aides,
        a_lever=a_lever,
        points_csg=a_lever / donnees.RENDEMENT_POINT_CSG,
        part_prime_due=primes_dues / donnees.DEPENSE_TOTALE,
        part_prime_reelle=primes_encaissees / donnees.DEPENSE_TOTALE,
    )


def encaissement_maximal(assiette: str = "personne") -> float:
    """Le plus que les primes puissent rapporter, quelle que soit leur hauteur.

    C'est le résultat le plus important de ce module, et le moins attendu.

    L'allocation plafonne la prime à une part du revenu. Au-delà d'un certain
    montant, TOUT LE MONDE est au plafond : chaque euro ajouté à la prime est
    alors intégralement repris par l'allocation, et l'assureur n'encaisse pas
    un centime de plus. Ce que les assurés versent de leur poche est donc borné
    par ``adultes × plafond × revenu moyen``, et la hauteur de la prime n'y
    change rien.

    Conséquence directe : avec le plafond actuel, la promesse d'un partage
    moitié-moitié entre prime et contribution est arithmétiquement
    impossible — non pas mal calibrée, impossible. Il faut relever le plafond,
    ou renoncer à la promesse.
    """
    adultes = donnees.POPULATION - donnees.MINEURS
    moyen = sum(donnees.DECILES_NIVEAU_VIE) / len(donnees.DECILES_NIVEAU_VIE)
    return adultes * _taux_effectif(assiette) * moyen


def plafond_pour_partage(cible: float, assiette: str = "personne") -> float:
    """Le plafond d'allocation qu'exige un partage donné entre les deux étages."""
    adultes = donnees.POPULATION - donnees.MINEURS
    moyen = sum(donnees.DECILES_NIVEAU_VIE) / len(donnees.DECILES_NIVEAU_VIE)
    correction = _taux_effectif(assiette) / _taux_effectif("personne")
    return cible * donnees.DEPENSE_TOTALE / (adultes * moyen) / correction


def prime_pour_partage(cible: float) -> float:
    """La prime qui financerait ``cible`` de la dépense si personne n'était aidé.

    Elle est plus élevée que celle du simulateur, et pour une raison
    arithmétique qu'il faut voir : la prime y est calée sur une part du coût
    moyen par HABITANT, alors que seuls les adultes la paient. Quatorze
    millions et demi de mineurs ne versant rien, la même moitié doit être
    portée par cinquante-quatre millions d'adultes et non par soixante-huit.
    """
    adultes = donnees.POPULATION - donnees.MINEURS
    return cible * donnees.DEPENSE_TOTALE / adultes


def cout_scenario(prime: float, plafond: float,
                  assiette: str = "personne") -> tuple[float, float, float]:
    """Coût de l'allocation, part des adultes aidés, part réellement encaissée.

    C'est la fonction qui sert à essayer un autre calibrage que celui du
    simulateur, sans le modifier : on lui donne une prime et un plafond, elle
    répond. Rien d'autre ne change.
    """
    taux = plafond * (_taux_effectif(assiette) / _taux_effectif("personne"))
    adultes = donnees.POPULATION - donnees.MINEURS
    allocations = [max(0.0, prime - taux * niveau)
                   for niveau in donnees.DECILES_NIVEAU_VIE]
    cout = sum(allocations) / len(allocations) * adultes
    aides = sum(1 for montant in allocations if montant > 0) / len(allocations)
    return cout, aides, (adultes * prime - cout) / donnees.DEPENSE_TOTALE


def repere_neerlandais() -> float:
    """Ce que coûterait le zorgtoeslag néerlandais rapporté à la population française.

    Ce n'est pas une prévision : c'est le seul instrument comparable qui
    existe et dont le coût soit publié. Un chiffrage qui s'en écarterait d'un
    ordre de grandeur serait à refaire.
    """
    par_habitant = donnees.ZORGTOESLAG_COUT / donnees.POPULATION_PAYS_BAS
    return par_habitant * donnees.POPULATION


def cout_actuel_couverture() -> float:
    """Ce que l'État consacre DÉJÀ à la couverture complémentaire.

    Une dépense nouvelle qui en remplace une ancienne ne coûte que l'écart. Le
    taire reviendrait à se charger soi-même.
    """
    return donnees.DEPENSE_PUBLIQUE_COMPLEMENTAIRE


# -- les chiffres que ce calcul produit --------------------------------------
#
# Ils entrent dans les pages comme les autres — par leur clé, avec leur source
# et leur étiquette — à ceci près que leur source est ce fichier, et leur
# étiquette « estimé ». Un chiffre calculé qui se présenterait comme un chiffre
# publié serait un faux ; un chiffre calculé qu'on tairait serait un aveu.

PLAFOND_RECALIBRE = 0.10
"""Plafond d'allocation du scénario recalibré, en part du revenu.

Il n'est pas dans ``PARAMETRES_SIMULATEUR`` parce que le programme ne l'a pas
adopté : c'est une proposition que le chiffrage rend possible d'examiner, et
elle attend une décision.
"""


def _milliards(montant: float) -> str:
    return f"≈ {montant / 1e9:.0f} Md€"


def chiffres_calcules() -> dict[str, donnees.Chiffre]:
    """Ce que le chiffrage publie, prêt à être cité par une page."""
    courant = chiffrer("personne")
    foyer = chiffrer("foyer")
    prime_juste = prime_pour_partage(0.5)
    recalibre, aides_recalibre, part_recalibre = cout_scenario(
        prime_juste, PLAFOND_RECALIBRE)
    source = ("Calcul de ce dépôt : src/sante/allocation.py, entrées dans "
              "src/sante/donnees.py")

    def chiffre(cle: str, valeur: str, libelle: str, precision: str):
        return donnees.Chiffre(cle=cle, valeur=valeur, libelle=libelle,
                               annee="2026", source=source, fiabilite="estime",
                               precision=precision)

    return {c.cle: c for c in (
        chiffre(
            "allocation_cout", _milliards(courant.cout),
            "de coût annuel de l'allocation santé, telle qu'elle est "
            "paramétrée",
            "Somme, sur les dix déciles de niveau de vie publiés par l'INSEE, "
            f"de l'écart entre la prime ({prime_pleine():.0f} €) et le "
            "plafond de 5 % du revenu, multipliée par les 54 millions "
            "d'adultes redevables. Assise sur le foyer plutôt que sur la "
            f"personne, elle coûterait {foyer.cout / 1e9:.0f} Md€ : un couple "
            "doit deux primes pour une fois et demie le revenu d'un "
            "célibataire, et l'assiette de foyer est donc la plus généreuse "
            "des deux — le contraire de l'intuition.",
        ),
        chiffre(
            "allocation_net",
            _milliards(courant.cout - cout_actuel_couverture()),
            "de coût NET, une fois défalqué ce que l'État dépense déjà",
            "L'allocation ne s'ajoute pas aux aides existantes : elle les "
            "remplace. La Cour des comptes chiffre à une dizaine de milliards "
            "les exonérations sociales et fiscales et la complémentaire santé "
            "solidaire consacrées à la couverture complémentaire. Le coût "
            "net est l'écart, et c'est lui qu'il faut défendre.",
        ),
        chiffre(
            "allocation_aides",
            f"{courant.adultes_aides * 100:.0f}\u202f%",
            "des adultes toucheraient l'allocation",
            "Huit déciles de niveau de vie sur dix passent sous le plafond de "
            "5 % : ce n'est pas un filet, c'est un régime quasi universel. "
            "C'est la première chose qu'un contradicteur relèvera, et elle "
            "est exacte.",
        ),
        chiffre(
            "prime_encaissement_max", _milliards(encaissement_maximal()),
            "le maximum que les primes puissent rapporter, à ce plafond",
            "Au-delà d'un certain montant de prime, tout le monde est au "
            "plafond : chaque euro ajouté est repris par l'allocation, et "
            "l'assureur n'encaisse rien de plus. Les primes sont donc bornées "
            f"à {encaissement_maximal() / donnees.DEPENSE_TOTALE:.0%} de la "
            "dépense de santé, quelle que soit leur hauteur. Un partage "
            "moitié-moitié entre prime et contribution n'est pas mal calibré "
            "à ce plafond : il est impossible.",
        ),
        chiffre(
            "allocation_repere", _milliards(repere_neerlandais()),
            "ce que coûterait le dispositif néerlandais à notre échelle",
            "Le zorgtoeslag coûte environ 6,5 Md€ par an pour 18 millions "
            "d'habitants, soit 360 € par habitant. Rapporté à la population "
            "française, cela donne ce montant. Ce n'est pas une prévision : "
            "c'est le seul instrument comparable dont le coût soit publié, et "
            "il sert à savoir si notre calcul est du bon ordre. Il l'est.",
        ),
        chiffre(
            "allocation_recalibree", _milliards(recalibre),
            "de coût annuel si l'allocation redevenait un filet",
            f"Avec une prime de {prime_juste:.0f} € — la moitié de la dépense "
            "rapportée aux adultes qui la paient, et non aux habitants — et "
            f"un plafond porté à {PLAFOND_RECALIBRE:.0%} du revenu, "
            f"l'allocation ne toucherait plus que {aides_recalibre:.0%} des "
            "adultes, les primes porteraient "
            f"{part_recalibre:.0%} du financement, et le coût tomberait "
            "sous celui des aides actuelles. C'est une proposition, pas une "
            "mesure : le programme ne l'a pas adoptée.",
        ),
    )}


def valeur_calculee(cle: str) -> str:
    """Le chiffre calculé de clé donnée, pour l'écrire au fil d'une phrase."""
    calcules = chiffres_calcules()
    if cle not in calcules:
        raise KeyError(f"chiffre calculé inconnu : {cle}")
    return calcules[cle].valeur
