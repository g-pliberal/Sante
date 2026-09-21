"""Le texte du site, page par page.

Chaque fonction rend le CORPS d'une page — le gabarit pose autour d'elle le
bandeau, le pied et la coquille HTML. Les chiffres ne sont pas écrits ici : ils
sont appelés par leur clé dans ``donnees.py``, qui les porte avec leur source et
leur millésime.

L'ordre des pages est celui des questions qu'un électeur pose : qu'est-ce qui ne
va pas, que font les autres, que proposez-vous, qu'est-ce que ça me fait, et
qu'est-ce que vous répondez à mes objections.
"""

from __future__ import annotations

from . import allocation, donnees, gabarit as g
from .allocation import valeur_calculee as vc
from .donnees import valeur as v


# -- accueil : le programme --------------------------------------------------


def programme() -> str:
    tete = g.affiche(
        "Notre programme pour la santé",
        "Parmi les plus chères d'Europe, et "
        + g.cle_texte(v("delai_ophtalmo"))
        + " pour un ophtalmologue.",
        "La France consacre à la santé près de trois points de PIB de plus que "
        "la moyenne des pays riches, et le délai médian pour un rendez-vous "
        "d'ophtalmologie y est de cinquante-deux jours — deux jours chez le "
        "généraliste, et jusqu'à quatre mois dans certaines régions. "
        + g.cle_texte("Le problème n'est pas l'argent.")
        + " C'est que personne, dans ce système, n'a le pouvoir de choisir : ni "
        "le patient, ni le médecin, ni même le directeur d'hôpital.",
    )

    reperes = g.fiches(["dcs_pib", "ocde_moyenne", "deficit_maladie",
                        "sans_medecin"], reperes=True)

    cartes = g.engagements([
        (
            "1 contrat",
            "au lieu de deux assureurs " + g.cle_texte("sur la même facture")
            + ".",
            "La Sécurité sociale rembourse 70 % d'une consultation, la "
            "complémentaire le reste : deux organismes, deux systèmes "
            "d'information, deux services de gestion pour un seul soin. Nous "
            "les fusionnons en un contrat unique, couvrant l'intégralité du "
            "panier de soins. Les frais de gestion des seules complémentaires "
            f"pèsent {v('frais_gestion_oc')} par an.",
        ),
        (
            "Votre choix",
            "de l'assureur, " + g.cle_texte("comme en Allemagne")
            + " et aux Pays-Bas.",
            "L'assurance maladie de base cesse d'être un monopole. Plusieurs "
            "caisses — publiques, mutualistes, privées — offrent le même "
            "panier obligatoire, sous une règle d'airain : aucune ne peut "
            "refuser un assuré ni moduler sa prime selon son état de santé. "
            "Une " + g.terme("péréquation des risques") + " leur verse ce que "
            "coûtent réellement leurs malades.",
        ),
        (
            "100 %",
            "du gros risque couvert, " + g.cle_texte("sans condition") + ".",
            "Un bouclier sanitaire remplace et élargit l'"
            + g.terme("ALD") + " : au-delà d'un plafond annuel de reste à "
            "charge, proportionnel au revenu, tout est pris en charge. Nul ne "
            "renonce à un traitement lourd pour des raisons d'argent — c'est "
            "la première obligation d'un système d'assurance, et le reste en "
            "découle.",
        ),
        (
            "0 quota",
            "à l'entrée des études, " + g.cle_texte("ni à l'installation") + ".",
            "Le " + g.terme("numerus clausus") + " a plafonné les promotions "
            f"à {v('numerus')} au milieu des années 1990 ; les médecins qui "
            "manquent aujourd'hui sont ceux qu'on a refusé de former il y a "
            "trente ans. Nous ouvrons les capacités de formation, supprimons "
            "les quotas d'installation, et rendons publics les prix comme les "
            "résultats.",
        ),
    ])

    etapes = g.gestes([
        "<strong>Vous choisissez votre assureur santé</strong>, une fois par "
        "an, parmi tous ceux qui offrent le panier obligatoire. Rester ne "
        "demande rien ; partir prend dix minutes.",
        "<strong>Vous payez deux choses, et vous les voyez toutes les "
        "deux</strong> : une contribution assise sur votre revenu, qui "
        "remplace la cotisation maladie de votre employeur et la part de "
        + g.terme("CSG") + " affectée à la santé et alimente la "
        + g.terme("péréquation des risques") + " ; et une prime versée à "
        "l'assureur que vous avez choisi, qui remplace votre complémentaire. "
        "La loi fixe un plancher — la moitié au moins assise sur le revenu — "
        "et vise le partage néerlandais, moitié-moitié : une prime seule "
        "serait la même pour un SMIC et pour un très haut revenu, et ce n'est "
        "pas ce que nous proposons.",
        "<strong>Les petits soins passent par une franchise annuelle</strong>, "
        "plafonnée selon votre revenu ; au-delà, l'assureur paie tout. Les "
        "soins lourds, eux, sont couverts dès le premier euro.",
    ])

    comparatif = g.tableau(
        ["", "Aujourd'hui", "Avec la réforme"],
        [
            ["Qui vous assure", "Un organisme imposé par votre statut",
             "Celui que vous choisissez"],
            ["Combien vous payez", "Réparti entre cotisations, CSG et mutuelle",
             "Une contribution sur le revenu, une prime : deux lignes, "
             "écrites"],
            ["Qui rembourse", "Deux organismes sur la même facture",
             "Un seul"],
            ["Si vous êtes gravement malade",
             "100 % du tarif Sécu, si vous êtes sur la liste ALD",
             "Tout, au-delà du plafond de reste à charge"],
            ["Si votre assureur vous déplaît", "Rien à faire",
             "Vous partez ailleurs"],
        ],
        ["", "", ""],
        "Ce que la réforme change, ligne à ligne",
    )

    changements = g.points([
        ("Le prix redevient une information",
         "Aujourd'hui, ni le patient ni le médecin ne savent ce que coûte "
         "l'acte qu'ils décident. Un système où personne ne connaît le prix "
         "n'a aucun moyen de repérer ce qui est cher pour rien."),
        ("L'assureur a intérêt à vous garder en bonne santé",
         "Un assureur que l'on peut quitter, et qui reçoit pour chaque assuré "
         "ce que son état de santé coûte réellement, gagne à prévenir plutôt "
         "qu'à rembourser. Un monopole n'a cet intérêt qu'en théorie."),
        ("Le médecin cesse d'être un fonctionnaire de fait",
         "Tarifs fixés par convention nationale, lieu d'exercice sous "
         "contrainte, acte codifié : l'exercice libéral n'a plus de libéral "
         "que le nom. Nous rendons au praticien le droit de s'installer, de "
         "fixer son prix et de le publier."),
        ("La facture cesse d'être envoyée aux suivants",
         f"La dette sociale — de l'ordre de {v('dette_sociale')} à rembourser "
         "— finance des soins consommés il y a dix ou vingt ans. Une "
         "génération se soigne, la suivante paie : ce n'est pas de la "
         "solidarité, c'est un transfert non voté."),
    ])

    appel = g.appel(
        "Vérifiez plutôt que de nous croire.",
        "Tous les chiffres de ce site sont datés, sourcés et notés selon leur "
        "fiabilité. Le simulateur calcule dans votre navigateur ce que la "
        "santé prélève réellement sur votre travail — rien n'est envoyé nulle "
        "part.",
        [("Ce que vous payez vraiment", "simulateur.html", True),
         ("Ce qui ne va pas aujourd'hui", "diagnostic.html", False),
         ("D'où viennent nos chiffres", "donnees.html", False)],
    )

    pas_propose = g.depliant(
        "Ce que nous ne proposons pas",
        """
<p>Une proposition libérale sur la santé est immédiatement traduite par ses
adversaires en « système américain ». Disons donc en toutes lettres ce que ce
programme ne contient pas.</p>
<ul class="serree">
  <li><strong>Pas de fin de l'obligation d'assurance.</strong> S'assurer reste
  obligatoire, et l'assureur reste obligé d'accepter tout le monde au même
  prix. Un marché de l'assurance santé sans ces deux règles trie les malades :
  c'est le défaut américain, et il est évitable.</li>
  <li><strong>Pas de reste à charge sur le gros risque.</strong> Le bouclier
  sanitaire couvre intégralement ce qui dépasse un plafond proportionnel au
  revenu. Aucune maladie grave ne doit coûter un patrimoine.</li>
  <li><strong>Pas de privatisation des hôpitaux publics.</strong> Nous leur
  donnons l'autonomie de gestion qu'ont les hôpitaux allemands ou suisses —
  recruter, investir, s'organiser — et non un actionnaire.</li>
  <li><strong>Pas de baisse du niveau de couverture.</strong> Le panier de
  soins obligatoire est défini par la loi, et ce programme ne propose pas de le
  réduire. Il propose de le payer autrement.</li>
</ul>
<p class="discret">Ce qui reste, après ces quatre exclusions, est exactement ce
que pratiquent les Pays-Bas, l'Allemagne et la Suisse — trois pays qui couvrent
toute leur population et n'ont jamais connu le débat français sur l'accès aux
soins.</p>""",
        "non-propose",
    )

    garanties = g.depliant(
        "Les garanties, écrites dans la loi",
        """
<p>Une réforme de l'assurance maladie ne vaut que par ce qu'elle interdit à
ceux qui l'appliqueront. Sept règles, dans la loi et non dans un décret :</p>
<ol class="gestes">
  <li><span class="rang">1</span><span><strong>Obligation d'accepter.</strong>
  Aucun assureur ne peut refuser une demande d'affiliation au panier
  obligatoire, quel que soit l'état de santé du demandeur.</span></li>
  <li><span class="rang">2</span><span><strong>Prime unique.</strong> À l'intérieur
  d'un même contrat de base, la prime ne dépend ni de l'état de santé, ni du
  sexe, ni des antécédents.</span></li>
  <li><span class="rang">3</span><span><strong>Péréquation obligatoire.</strong>
  Un fonds public verse à chaque assureur ce que coûtent ses assurés selon
  leur âge et leurs pathologies, de sorte qu'assurer un malade ne soit jamais
  une mauvaise affaire.</span></li>
  <li><span class="rang">4</span><span><strong>Bouclier sanitaire.</strong>
  Le reste à charge annuel est plafonné en part du revenu ; au-delà, la prise
  en charge est intégrale et automatique.</span></li>
  <li><span class="rang">5</span><span><strong>Aide au paiement.</strong> Une
  allocation santé prend en charge tout ou partie de la prime des ménages
  modestes, comme le fait la Suisse pour un quart de sa population.</span></li>
  <li><span class="rang">6</span><span><strong>Moitié-moitié.</strong> La
  moitié au moins du financement reste assise sur le revenu. La prime versée à
  l'assureur ne peut pas porter l'autre moitié à elle seule : c'est la règle
  néerlandaise, et elle est ce qui sépare une assurance solidaire d'une
  capitation.</span></li>
  <li><span class="rang">7</span><span><strong>Aucune prime avant 18
  ans.</strong> Les mineurs sont assurés sans prime, l'État versant la leur au
  fonds de péréquation. Une famille ne paie pas autant de primes qu'elle
  compte de têtes.</span></li>
</ol>""",
        "garanties",
    )

    transition = g.depliant(
        "Comment on y va, en cinq ans",
        """
<p>Aucun système de santé ne change du jour au lendemain, et personne ne doit
se retrouver sans couverture pendant la transition. Le calendrier est donc
lent, et chaque étape est réversible tant que la suivante n'a pas eu lieu.</p>
<ul class="serree">
  <li><strong>Année 1 — la transparence.</strong> Publication obligatoire des
  prix pratiqués, des délais d'attente et des résultats par établissement.
  Elle ne coûte rien, ne demande aucune loi organique, et change déjà les
  comportements.</li>
  <li><strong>Année 2 — le guichet unique.</strong> Fusion du remboursement de
  base et complémentaire : un seul décompte, un seul interlocuteur, un seul
  service de gestion. Les organismes existants deviennent les premiers
  assureurs du nouveau régime.</li>
  <li><strong>Année 3 — le bouclier.</strong> Le plafond de reste à charge
  proportionnel au revenu remplace le régime ALD, qu'il englobe. C'est l'étape
  la plus délicate du calendrier, et il faut la nommer : un patient en ALD est
  aujourd'hui remboursé à 100 % du tarif pour les soins liés à son affection,
  là où un bouclier fait payer jusqu'à son plafond. Le calibrage de ce plafond
  pour les affections longues est donc une condition de la réforme, écrite
  dans la loi et non dans un décret : aucun malade chronique ne doit sortir
  perdant de l'échange.</li>
  <li><strong>Année 4 — le choix.</strong> Ouverture effective de la
  concurrence : chacun peut changer d'assureur au 1ᵉʳ janvier. La
  péréquation des risques est en service depuis un an, à blanc.</li>
  <li><strong>Année 5 — l'offre.</strong> Liberté d'installation, ouverture
  des capacités de formation, autonomie de gestion des hôpitaux publics.
  C'est la mesure la plus lente à produire ses effets : elle doit donc être
  votée la première, même si elle s'applique la dernière.</li>
</ul>""",
        "transition",
    )

    diagnostic_court = g.depliant(
        "Le diagnostic, en cinq lignes",
        f"""
<ul class="serree">
  <li>La France dépense {v('dcs_pib')} pour sa santé, contre {v('ocde_moyenne')}
  en moyenne dans l'OCDE.</li>
  <li>La branche maladie est en déficit d'environ {v('deficit_maladie')} par
  an, sans qu'aucune loi n'ait prévu son retour à l'équilibre.</li>
  <li>Environ {v('sans_medecin')} de personnes n'ont pas de médecin traitant,
  et près d'un Français sur trois vit dans une zone sous-dense.</li>
  <li>Le reste à charge des ménages est le plus faible de l'OCDE
  ({v('reste_a_charge')}) : le rationnement ne passe pas par l'argent, il passe
  par l'attente.</li>
  <li>Deux assureurs interviennent sur la même facture, et le second coûte à
  lui seul {v('frais_gestion_oc')} de frais de gestion par an.</li>
</ul>
<p class="actions"><a href="diagnostic.html">Le diagnostic complet</a></p>""",
        "diagnostic-court",
    )

    return f"""
{tete}

{reperes}

{cartes}

<div class="paire">
  <div>
    <p class="surtitre">La réforme</p>
    <h2 style="margin-top:0">Comment ça marche, en trois gestes</h2>
    {etapes}
    <p class="discret">Rien de tout cela n'est une expérience : c'est le
    fonctionnement ordinaire de l'assurance maladie aux Pays-Bas depuis 2006 et
    en Suisse depuis 1996. <a href="comparaisons.html">Voir comment</a>.</p>
  </div>
  <div class="encadre">
    <h2 class="serif" style="margin-top:0">Ce qui change pour vous</h2>
    {comparatif}
  </div>
</div>

<h2>Ce que cela change</h2>
{changements}

{appel}

<h2>Pour aller plus loin</h2>

{diagnostic_court}
{pas_propose}
{garanties}
{transition}
"""


# -- le système actuel -------------------------------------------------------


def diagnostic() -> str:
    tete = g.affiche(
        "Le système actuel",
        "Beaucoup d'argent, " + g.cle_texte("peu de choix") + ", et une file "
        "d'attente.",
        "Le système de santé français a une qualité rare : il laisse très peu "
        "de dépenses à la charge des malades. Il a aussi trois défauts qui "
        "s'aggravent — il coûte plus cher que partout ailleurs en Europe, il "
        "ne trouve plus de médecin pour six millions de personnes, et il "
        "finance les soins d'hier avec la dette de demain.",
    )

    marche = g.cle(
        "Comment ça marche aujourd'hui, exactement ?",
        "Un monopole public rembourse environ 80 % de la dépense, une "
        "complémentaire privée obligatoire rembourse le reste, et le Parlement "
        "vote chaque année un objectif de dépense qu'il n'a aucun moyen de "
        "faire respecter.",
        f"""
<ul class="serree">
  <li><strong>Vous ne choisissez pas votre assureur de base.</strong> Votre
  caisse dépend de votre statut professionnel et de votre lieu de résidence.
  Elle rembourse {v('part_amo')} de la dépense de soins.</li>
  <li><strong>Vous payez sans le voir.</strong> La cotisation maladie de votre
  employeur ({v('cotisation_employeur')} du salaire brut) et la
  {g.terme('CSG')} ({v('csg')}) sont prélevées avant que votre salaire n'existe.
  Aucune fiche de paie ne totalise ce que la santé vous coûte.</li>
  <li><strong>Une seconde assurance rembourse le solde.</strong> La
  complémentaire santé, obligatoire en entreprise depuis 2016, couvre le
  {g.terme('ticket modérateur')} : {v('part_oc')} de la dépense, pour
  {v('frais_gestion_oc')} de frais de gestion par an.</li>
  <li><strong>Le Parlement vote un objectif, pas un budget.</strong>
  L'{g.terme('ONDAM')} s'élève à {v('ondam')} pour 2025. Son dépassement
  n'emporte aucune conséquence automatique, et il a été dépassé la plupart des
  années depuis sa création.</li>
  <li><strong>Les prix sont administrés.</strong> Le tarif d'une consultation,
  d'un acte, d'un séjour hospitalier est fixé par convention nationale ou par
  arrêté. Ni le patient ni le médecin ne négocient quoi que ce soit.</li>
</ul>""",
        identifiant="fonctionnement",
    )

    cout = g.cle(
        "Combien ça coûte, et à qui ?",
        f"Environ {v('csbm')} de soins consommés en un an, financés à "
        f"{v('part_amo')} par la Sécurité sociale, {v('part_oc')} par les "
        f"complémentaires, et {v('reste_a_charge')} par les ménages.",
        g.fiches(["csbm", "dcs_pib", "prelevements"])
        + """
<p>La dépense n'est pas anormale en elle-même : un pays riche et vieillissant
dépense beaucoup pour sa santé, et c'est légitime. Ce qui l'est moins, c'est
l'écart avec des pays qui obtiennent des résultats comparables — près de trois
points de PIB, soit de l'ordre de quatre-vingts milliards d'euros par an. Cet
argent est prélevé sur le travail : la France a le taux de prélèvements
obligatoires le plus élevé de l'Union européenne, et la santé en est, avec les
retraites, le premier poste.</p>""",
        identifiant="cout",
    )

    maux = g.cle(
        "Qu'est-ce qui ne marche pas ?",
        "Six défauts, et ils se tiennent : ils découlent tous du fait que "
        "personne n'a, dans ce système, à la fois l'information et le pouvoir "
        "de décider.",
        """
<h4>1. Personne ne connaît le prix</h4>
<p>Le patient ne voit pas ce que coûte son soin ; le médecin non plus, le plus
souvent, pour ce qu'il prescrit. Un système où le prix n'apparaît nulle part
n'a aucun moyen de distinguer ce qui est cher et utile de ce qui est cher pour
rien. Les seules économies possibles y sont donc aveugles : une baisse de
tarif, un déremboursement uniforme, un gel de l'enveloppe.</p>

<h4>2. Deux assureurs sur la même facture</h4>
<p>La Sécurité sociale rembourse une part, la complémentaire l'autre. Deux
organismes lisent la même feuille de soins, tiennent deux systèmes
d'information, emploient deux services de gestion et envoient deux décomptes.
La complémentaire est, de plus, taxée : une taxe pèse sur une assurance rendue
obligatoire par la loi.</p>

<h4>3. La pénurie a été organisée</h4>
<p>Le nombre de médecins formés a été plafonné pendant cinquante ans par l'État
lui-même, au motif que l'offre de soins crée la demande. Un médecin se formant
en dix ans, la pénurie constatée aujourd'hui a été décidée dans les années
1990. S'y ajoutent des règles d'installation, des conventions tarifaires qui
rendent certains exercices non viables, et une charge administrative qui prend
au praticien un jour de travail par semaine.</p>

<h4>4. L'hôpital est piloté par circulaire</h4>
<p>Un directeur d'hôpital public ne fixe ni les tarifs de ses séjours, ni les
salaires de ses équipes, ni, le plus souvent, ses investissements. Il applique.
La tarification à l'activité l'a rendu comptable de son volume d'actes sans lui
donner la maîtrise de ses coûts : la pire combinaison possible, celle qui
produit à la fois la course au volume et l'impuissance budgétaire.</p>

<h4>5. Le déficit est devenu structurel</h4>
<p>La branche maladie est en déficit chaque année depuis plus de vingt ans, à
deux exceptions près. Ce déficit est repris par la dette sociale, amortie par
un prélèvement sur les revenus d'aujourd'hui pour des soins consommés il y a
dix ou vingt ans. Aucune loi ne prévoit de retour durable à l'équilibre.</p>

<h4>6. Le rationnement passe par l'attente</h4>
<p>C'est le point le plus important, et le moins dit. Dans un système où le
prix ne joue aucun rôle, la demande dépasse toujours l'offre, et il faut bien
que quelque chose la contienne : c'est le délai. Six mois pour un
ophtalmologue, des mois pour un spécialiste, des heures aux urgences faute de
médecine de ville disponible. Le reste à charge le plus faible de l'OCDE
coexiste ainsi avec un renoncement aux soins massif — non par manque d'argent,
mais par manque de rendez-vous.</p>""",
        identifiant="maux",
    )

    pression = g.cle(
        "Est-ce que ça peut durer ?",
        "Non, et la raison est démographique : la dépense croît avec l'âge de "
        "la population, tandis que la base qui la finance — le travail — ne "
        "croît plus.",
        f"""
<p>Les {v('ald')} de personnes en {g.terme('ALD')} concentrent environ les deux
tiers des remboursements, et leur nombre augmente de 3 à 4 % par an sous le
double effet du vieillissement et du progrès thérapeutique. C'est une bonne
nouvelle sanitaire et une équation budgétaire impossible : la dépense suit une
population qui vieillit, la recette suit une masse salariale qui stagne.</p>
<p>Il n'existe que quatre façons de solder cet écart : augmenter les
prélèvements sur le travail, rationner davantage par l'attente, rembourser
moins, ou rendre le système plus efficace. Les trois premières ont été essayées
sans relâche depuis trente ans. Ce site propose la quatrième.</p>""",
        identifiant="pression",
    )

    garder = g.cle(
        "Qu'est-ce qui marche, et qu'il ne faut pas casser ?",
        "Trois choses, et aucune réforme ne doit y toucher : la couverture "
        "universelle, le reste à charge faible sur le gros risque, et la "
        "qualité des soins hospitaliers lourds.",
        f"""
<ul class="serree">
  <li><strong>Tout le monde est couvert.</strong> La protection universelle
  maladie couvre toute personne résidant régulièrement en France. C'est un
  acquis, et il n'est pas négociable.</li>
  <li><strong>Le {g.terme('reste à charge')} est le plus faible de l'OCDE</strong>
  ({v('reste_a_charge')} de la dépense). Une réforme qui l'augmenterait
  significativement pour les maladies graves serait un échec, quel que soit son
  effet budgétaire.</li>
  <li><strong>L'espérance de vie est parmi les meilleures d'Europe</strong>
  ({v('esperance_vie')}). C'est l'étalon auquel toute réforme doit se juger,
  avant tout autre.</li>
  <li><strong>L'hôpital public sait traiter l'urgence vitale et le soin
  complexe.</strong> Ce qu'il fait mal, il le fait mal par contrainte de
  gestion, non par défaut de compétence.</li>
</ul>
<p>Un programme sérieux part de là. Il ne s'agit pas de remplacer un système
qui échoue par un système inconnu, mais de corriger trois défauts précis dans
un système qui réussit sur l'essentiel et se dégrade sur le reste.</p>""",
        identifiant="acquis",
    )

    corps = marche + cout + maux + pression + garder
    return f"""
{tete}
{g.plan(corps)}
{corps}

{g.appel(
    "Voyez ce que ces défauts vous coûtent.",
    "Le simulateur additionne, sur votre salaire, tout ce qui est prélevé pour "
    "la santé — cotisation employeur, part de CSG, complémentaire, "
    "participations. Le total surprend presque toujours.",
    [("Ce que vous payez vraiment", "simulateur.html", True),
     ("Ce que font les autres pays", "comparaisons.html", False)],
)}
"""


# -- comparaisons internationales --------------------------------------------


def comparaisons() -> str:
    tete = g.affiche(
        "Ailleurs",
        "Quatre pays couvrent " + g.cle_texte("tout le monde") + " sans "
        "monopole public.",
        "Le débat français oppose le modèle actuel au « système américain ». "
        "C'est une fausse alternative : entre les deux, quatre pays au moins "
        "assurent une couverture universelle avec des assureurs en "
        "concurrence, sans que personne n'y soit refusé pour son état de "
        "santé — et plusieurs dépensent moins que nous.",
    )

    lignes = [
        [pays.nom, pays.depense, pays.publique, pays.modele.split(".")[0] + "."]
        for pays in donnees.PAYS
    ]
    lignes.insert(0, [
        "<strong>France</strong>", f"<strong>{v('dcs_pib')}</strong>",
        f"<strong>{v('part_publique_france')}</strong>",
        "<strong>Monopole public pour la base, assurance privée obligatoire "
        "pour le complément</strong>",
    ])
    table = g.tableau(
        ["Pays", "Dépense de santé", "Part publique", "Mécanisme"],
        lignes,
        ["", "nombre", "nombre", "long texte"],
        "Quatre systèmes universels sans monopole, et le nôtre",
    )

    fiches_pays = "".join(
        g.cle(
            f"{pays.nom} — {pays.drapeau}",
            pays.modele,
            "<ul class=\"serree\">"
            + "".join(f"<li>{detail}</li>" for detail in pays.detail)
            + "</ul>"
            + g.note("<strong>Ce que ça prouve.</strong> " + pays.lecon,
                     "resume")
            + g.note("<strong>Ce que valent ces chiffres.</strong> "
                     + pays.reserve, "avertissement"),
            source=f"{pays.annee} · {pays.source} · "
                   + g.etiquette_fiabilite(pays.fiabilite),
            identifiant=pays.nom.lower().replace("-", "").replace(" ", ""),
        )
        for pays in donnees.PAYS
    )

    limites = g.depliant(
        "Ce que ces exemples ne prouvent pas",
        f"""
<p>Une comparaison internationale est un argument faible si l'on en tire plus
qu'elle ne contient. Quatre réserves, et elles sont sérieuses :</p>
<ul class="serree">
  <li><strong>Les populations diffèrent.</strong> Singapour est une cité-État
  jeune ; la France est un pays vieillissant de {v('population')}
  d'habitants. La
  comparaison des dépenses en part de PIB ne corrige pas la structure d'âge.</li>
  <li><strong>Les périmètres comptables diffèrent.</strong> Ce qui est compté
  comme dépense de santé — soins de longue durée, dépendance, indemnités
  journalières — varie d'un pays à l'autre, malgré les efforts
  d'harmonisation de l'OCDE.</li>
  <li><strong>Aucun de ces pays n'est parfait.</strong> La Suisse laisse un
  reste à charge élevé. Les Pays-Bas ont connu une hausse des primes et un
  débat sur la concentration des assureurs. L'Allemagne peine à contenir sa
  dépense, la plus élevée d'Europe.</li>
  <li><strong>Une réforme ne se transplante pas.</strong> Ce qu'on peut
  reprendre d'un système étranger, ce sont des mécanismes — la péréquation des
  risques, la franchise choisie, la liberté de changer d'assureur — et non son
  organisation entière.</li>
</ul>
<p class="discret">Ce que ces quatre pays établissent, en revanche, est simple
et suffit à l'argument : la concurrence entre assureurs n'entraîne ni
sélection des malades, ni perte de couverture, ni explosion du reste à charge,
dès lors que la loi impose d'accepter tout le monde au même prix et organise
la péréquation des risques.</p>""",
        "limites-comparaison",
    )

    corps = fiches_pays
    avertissement_table = g.note(
        "<strong>Ces cinq lignes sont à vérifier avant toute reprise "
        "publique.</strong> Les parts de PIB sont recopiées de seconde main, "
        "et les périmètres comptables nationaux ne coïncident pas. Elles "
        "doivent être relues dans <em>une seule et même</em> édition du "
        "Système de comptes de la santé : deux chiffres vrais pris dans deux "
        "éditions différentes font un tableau faux, et c'est la pièce la plus "
        "facile à retourner contre qui la publie. Le classement des pays "
        "selon leur dépense — la Suisse notamment — en dépend.",
        "avertissement")

    return f"""
{tete}

{table}

{avertissement_table}

{g.plan(corps, "Les quatre systèmes")}

{corps}

{limites}

{g.appel(
    "Ce que nous en retenons, mesure par mesure.",
    "La réforme proposée reprend quatre mécanismes éprouvés : la péréquation "
    "des risques néerlandaise, la franchise choisie suisse, la liberté de "
    "changer de caisse allemande et la transparence des prix singapourienne.",
    [("La réforme en détail", "reforme.html", True),
     ("Nos sources", "donnees.html", False)],
)}
"""


# -- la réforme --------------------------------------------------------------


def reforme() -> str:
    tete = g.affiche(
        "La réforme",
        "Six mesures, " + g.cle_texte("et rien d'autre") + ".",
        "Un programme de santé se juge sur sa précision. Voici les six mesures "
        "que nous proposons, ce qu'elles changent, ce qu'elles coûtent, et "
        "l'objection la plus sérieuse qu'on leur oppose — écrite par nous, "
        "avant qu'on nous l'oppose.",
    )

    def mesure(numero: str, titre: str, quoi: str, comment: str,
               pour_vous: str, objection: str, reponse: str,
               identifiant: str) -> str:
        # L'objection est écrite PAR NOUS, avant qu'on nous l'oppose : une
        # mesure dont on n'a pas su nommer le défaut n'a pas été pensée.
        contradiction = g.note(
            "<strong>L'objection la plus sérieuse.</strong> "
            + objection
            + "<br><strong>Notre réponse.</strong> "
            + reponse,
            "vigilance",
        )
        return g.cle(
            f"{numero}. {titre}",
            quoi,
            f"""
<h4>Comment</h4>
{comment}
<h4>Ce que ça change pour vous</h4>
<p>{pour_vous}</p>
{contradiction}""",
            identifiant=identifiant,
        )

    mesures = "".join([
        mesure(
            "1", "Un seul assureur par facture",
            "Fusion de l'assurance maladie de base et de la complémentaire "
            "santé en un contrat unique couvrant l'intégralité du panier de "
            "soins.",
            f"""
<ul class="serree">
  <li>Le panier de soins obligatoire est défini par la loi, au niveau de
  couverture actuel base + complémentaire responsable.</li>
  <li>Un seul organisme rembourse, un seul décompte, un seul service de
  gestion, un seul interlocuteur en cas de litige.</li>
  <li>La taxe de solidarité additionnelle ({v('tsa')} sur votre cotisation de
  complémentaire) disparaît avec l'étage qu'elle taxait. Elle rapporte
  aujourd'hui {v('rendement_tsa')} et finance la complémentaire santé
  solidaire : cette recette doit être reprise à l'euro près dans le nouveau
  régime, faute de quoi la réforme déplacerait un trou au lieu de le
  combler.</li>
  <li>Les mutuelles et institutions de prévoyance existantes deviennent, si
  elles le souhaitent, les premiers assureurs du nouveau régime : elles en ont
  les réseaux, les systèmes et les adhérents.</li>
</ul>""",
            "Vous ne remplissez plus de dossier entre deux organismes et vous "
            "ne recevez plus deux décomptes pour une consultation. Ce que la "
            "fusion économise n'est pas la totalité des "
            f"{v('frais_gestion_oc')} de gestion du second étage — un assureur "
            "unique garde des frais, et le premier étage en a déjà pour "
            f"{v('frais_gestion_amo')} — mais le DOUBLON : deux systèmes "
            "d'information, deux services de gestion et deux décomptes sur "
            "chaque facture. Nous ne savons pas dire au milliard près ce que "
            "pèse ce doublon, et nous ne l'inventons pas.",
            "Les complémentaires emploient des dizaines de milliers de "
            "personnes, dont l'emploi dépend directement de ce second étage.",
            "L'emploi ne disparaît pas : la gestion du risque, le service aux "
            "assurés et les réseaux de soins restent nécessaires, et ces "
            "organismes deviennent des assureurs de plein exercice au lieu "
            "d'être des payeurs de solde. La transition est étalée sur cinq "
            "ans pour cette raison.",
            "guichet-unique",
        ),
        mesure(
            "2", "Le choix de son assureur",
            "Fin du monopole de l'assurance maladie de base : plusieurs "
            "caisses offrent le même panier obligatoire, et chacun choisit la "
            "sienne.",
            f"""
<ul class="serree">
  <li>Toute caisse agréée — publique, mutualiste ou privée — peut offrir le
  panier obligatoire, aux mêmes conditions d'agrément.</li>
  <li><strong>Obligation d'accepter</strong> tout demandeur, et
  <strong>prime unique</strong> à l'intérieur d'un contrat : ni l'âge, ni le
  sexe, ni l'état de santé ne modulent ce que vous payez.</li>
  <li>Une {g.terme('péréquation des risques')} verse à chaque caisse ce que
  coûtent réellement ses assurés, calculée sur l'âge et les pathologies.
  C'est le mécanisme central : sans lui, la concurrence porte sur la sélection
  des malades ; avec lui, elle ne peut porter que sur le service et
  l'efficacité.</li>
  <li>Changement possible au 1ᵉʳ janvier, sans motif, sans frais, sans
  délai de carence.</li>
  <li><strong>Le financement reste à moitié assis sur le revenu.</strong> La
  prime versée à l'assureur ne porte que la moitié du coût ; l'autre moitié
  vient d'une contribution proportionnelle au revenu, qui remplace la
  cotisation employeur et la part de CSG et alimente la péréquation. C'est le
  partage que la loi néerlandaise impose depuis 2006, et c'est lui qui
  distingue cette réforme d'une capitation.</li>
  <li>Aucune prime n'est due avant 18 ans : l'État verse celle des mineurs au
  fonds.</li>
</ul>""",
            "Si votre caisse vous rembourse mal, vous fait attendre, ou "
            "refuse un traitement que sa concurrente accepte, vous partez. "
            "C'est le seul mécanisme de pression dont dispose un assuré, et "
            "c'est celui qu'un monopole lui retire.",
            "La concurrence entre assureurs de santé peut dégénérer en "
            "sélection des risques, ce qui rendrait les malades inassurables.",
            "C'est exact en l'absence de péréquation — et c'est la raison pour "
            "laquelle elle figure dans la loi, et non dans un décret "
            "d'application. Les Pays-Bas assurent ainsi toute leur population "
            "depuis 2006 sans qu'aucun assuré ne puisse être refusé.",
            "choix-assureur",
        ),
        mesure(
            "3", "Le bouclier sanitaire",
            "Un plafond annuel de reste à charge, proportionnel au revenu, "
            "au-delà duquel tout est pris en charge — quelle que soit la "
            "maladie.",
            f"""
<ul class="serree">
  <li>Le plafond est une part du revenu fiscal du foyer, et non un montant
  forfaitaire : un même euro de reste à charge ne pèse pas de la même façon
  sur un SMIC et sur un revenu élevé.</li>
  <li>Au-delà, la prise en charge est intégrale et <strong>automatique</strong> :
  aucun dossier, aucune demande, aucune liste.</li>
  <li>Le bouclier remplace le régime {g.terme('ALD')} en l'élargissant : les malades
  graves qui ne figurent sur aucune liste — et ils sont nombreux — sont
  couverts comme les autres, sans dossier, sans admission et sans attente.
  <strong>En contrepartie, il faut dire ce qu'un bouclier change pour ceux qui
  y sont déjà</strong> : l'ALD rembourse aujourd'hui dès le premier euro les
  soins liés à l'affection, là où un plafond se paie avant d'être atteint. Le
  plafond applicable aux {v('ald')} de personnes en ALD doit donc être fixé de
  sorte qu'aucune ne soit perdante — c'est une clause de la loi, pas un
  paramètre de décret.</li>
  <li>Les participations forfaitaires actuelles ({v('participation')}), qui
  pèsent autant sur un petit revenu que sur un grand, sont supprimées et
  remplacées par ce mécanisme.</li>
</ul>""",
            "Vous savez, au début de l'année, le maximum que votre santé peut "
            "vous coûter. C'est une information qu'aucun assuré français ne "
            "possède aujourd'hui, puisqu'elle dépend d'une liste "
            "administrative et du contrat de complémentaire dont il dispose.",
            "Un plafond proportionnel au revenu peut aboutir, pour les hauts "
            "revenus, à un reste à charge de plusieurs milliers d'euros.",
            "Oui, et c'est assumé : l'assurance doit couvrir ce qu'un ménage "
            "ne peut pas absorber, pas ce qu'il peut payer. La proportionnalité "
            "garantit que cette limite est la même pour tous, rapportée à ce "
            "qu'on gagne.",
            "bouclier",
        ),
        mesure(
            "4", "Une franchise plutôt qu'un forfait",
            "Le petit risque passe par une franchise annuelle modulable, "
            "choisie par l'assuré dans une fourchette légale, contre une prime "
            "plus basse.",
            """
<ul class="serree">
  <li>Comme en Suisse : plus la franchise choisie est élevée, plus la prime
  baisse. L'assuré arbitre lui-même entre certitude et coût.</li>
  <li>La médecine générale, la prévention, le suivi de grossesse et les soins
  pédiatriques en sont exclus : rien ne doit décourager le premier recours,
  qui est précisément ce qui évite les dépenses lourdes.</li>
  <li>La franchise ne s'applique jamais au-delà du plafond du bouclier : les
  deux mécanismes se rejoignent, et le second annule le premier.</li>
  <li>L'allocation santé couvre la franchise des ménages modestes, comme elle
  couvre leur prime.</li>
</ul>""",
            "Vous payez moins chaque mois si vous acceptez de payer les petits "
            "soins vous-même, et vous ne payez rien de plus si vous tombez "
            "gravement malade. Aujourd'hui, l'arbitrage n'existe pas : tout le "
            "monde paie la même chose pour la même couverture.",
            "Une franchise conduit certains à renoncer à des soins utiles, et "
            "un soin évité aujourd'hui coûte plus cher demain.",
            "C'est le risque réel de cette mesure, et il justifie l'exclusion "
            "de la médecine générale et de la prévention du champ de la "
            "franchise. Un renoncement se produit sur la consultation, pas sur "
            "l'hospitalisation : c'est donc la consultation qu'il faut laisser "
            "gratuite.",
            "franchise",
        ),
        mesure(
            "5", "Plus de médecins, libres de s'installer",
            "Suppression des quotas résiduels à l'entrée des études, ouverture "
            "des capacités de formation, et fin des restrictions à "
            "l'installation.",
            f"""
<ul class="serree">
  <li>Le {g.terme('numerus clausus')} a été remplacé en 2021 par un « numerus
  apertus » qui reste un plafond décidé par l'administration. Nous alignons le
  nombre de places sur les capacités réelles de formation, universités et
  terrains de stage.</li>
  <li>Reconnaissance accélérée des diplômes européens, et voie de
  qualification pour les praticiens à diplôme étranger déjà en exercice dans
  les hôpitaux français.</li>
  <li>Aucune autorisation administrative pour s'installer : la contrainte
  d'installation, régulièrement proposée, produirait l'effet inverse de celui
  qu'elle vise — elle dissuade de devenir médecin libéral.</li>
  <li>Délégation d'actes aux infirmiers en pratique avancée, aux pharmaciens
  et aux sages-femmes, sur la base de la compétence et non du statut.</li>
  <li>Liberté tarifaire, contre transparence obligatoire : le prix est
  affiché, comparable, et connu avant le soin.</li>
</ul>""",
            f"Aujourd'hui, {v('sans_medecin')} de personnes n'ont pas de "
            "médecin traitant et près d'un tiers de la population vit dans une "
            "zone sous-dense. Aucune mesure de répartition ne peut créer des "
            "médecins qui n'ont pas été formés : seule l'ouverture le peut, et "
            "elle met dix ans à produire ses effets. C'est pourquoi elle doit "
            "être votée en premier.",
            "La liberté tarifaire ferait exploser les dépassements "
            "d'honoraires, donc le reste à charge.",
            "Elle est indissociable de la transparence des prix et du bouclier "
            "sanitaire : un prix affiché et comparable se discipline par la "
            "concurrence, et ce qui dépasse le plafond de reste à charge est "
            "pris en charge intégralement. Le dépassement d'honoraires "
            "d'aujourd'hui prospère précisément parce que le tarif opposable "
            "est irréaliste et que le prix réel n'est affiché nulle part.",
            "offre-de-soins",
        ),
        mesure(
            "6", "Des prix et des résultats publics",
            "Publication obligatoire des prix pratiqués, des délais d'attente "
            "et des résultats de soins, établissement par établissement.",
            """
<ul class="serree">
  <li>Prix affichés pour tous les actes, en ville comme à l'hôpital, avant le
  soin, dans un format comparable et réutilisable.</li>
  <li>Délais d'attente moyens par spécialité et par établissement, publiés
  mensuellement.</li>
  <li>Indicateurs de résultats — taux de complications, de réadmission, de
  mortalité ajustée — publiés par établissement et par intervention, comme le
  font le Royaume-Uni et les pays scandinaves.</li>
  <li>Autonomie de gestion des hôpitaux publics : recrutement, rémunération,
  investissement, organisation. Un directeur responsable de ses résultats doit
  disposer des leviers correspondants.</li>
  <li>Données de remboursement ouvertes à la recherche et à l'évaluation
  indépendante, sous contrôle du secret médical.</li>
</ul>""",
            "Vous pouvez savoir, avant d'être opéré, combien d'interventions "
            "de ce type l'établissement pratique par an et avec quels "
            "résultats. Cette information existe déjà dans les bases de "
            "l'assurance maladie : elle n'est simplement pas publiée.",
            "Publier des résultats bruts conduirait les établissements à "
            "refuser les cas difficiles pour protéger leurs statistiques.",
            "C'est un effet documenté, et il se corrige par l'ajustement au "
            "risque des indicateurs — pratique standard là où ces publications "
            "existent depuis vingt ans. L'alternative — ne rien publier — "
            "laisse le patient choisir son chirurgien au hasard.",
            "transparence",
        ),
    ])

    # Le barème du plafond d'allocation, engendré par le chiffrage lui-même :
    # un arbitrage qu'on publie en nombres se discute ; le même en adjectifs
    # se subit.
    lignes_bareme = []
    for ligne in allocation.bareme_plafond():
        accent = (lambda texte: f"<strong>{texte}</strong>"
                  ) if ligne["retenu"] else str
        lignes_bareme.append([accent(str(ligne[colonne]))
                              for colonne in ("plafond", "cout", "aides",
                                              "part")])
    bareme = g.tableau(
        ["Plafond de l'allocation", "Ce qu'elle coûte",
         "Adultes protégés", "Part des primes dans le financement"],
        lignes_bareme,
        ["nombre", "nombre", "nombre", "nombre"],
        "Ce que chaque réglage du plafond coûte, et ce qu'il protège",
    )

    financement = g.depliant(
        "Qui paie, et combien",
        f"""
<p>Une réforme de l'assurance maladie ne diminue pas la dépense de soins du
jour au lendemain : elle change qui décide, et donc la manière dont la dépense
évolue. Disons d'abord par quels tuyaux l'argent passe, puis ce qu'on peut
affirmer et ce qu'on ne peut pas.</p>
<h4>Les deux étages, et leur partage</h4>
<p>Le financement repose sur deux prélèvements, et le partage entre eux est le
choix politique de cette réforme — pas un réglage technique.</p>
<ul class="serree">
  <li><strong>Une contribution assise sur le revenu</strong> remplace la
  cotisation maladie de l'employeur ({v('cotisation_employeur')} du brut) et la
  part de {g.terme('CSG')} affectée à la santé. Elle ne va pas à votre
  assureur : elle alimente le fonds de {g.terme('péréquation des risques')},
  qui verse ensuite à chaque caisse ce que coûtent réellement ses assurés.
  C'est elle qui porte la progressivité, et c'est elle qui rend la sélection
  des malades sans intérêt.</li>
  <li><strong>Une prime versée à l'assureur choisi</strong> remplace la
  cotisation de complémentaire. Elle est égale pour tous à l'intérieur d'un
  contrat, plafonnée en part du revenu par l'allocation santé, nulle avant 18
  ans. C'est la seule part du financement que vous pouvez emporter ailleurs,
  et c'est donc elle qui porte la concurrence.</li>
  <li><strong>La loi fixe un plancher et une cible.</strong> Le plancher : la
  moitié au moins des ressources reste assise sur le revenu. La cible : le
  partage néerlandais, moitié-moitié — {v('contribution_pays_bas')} de
  contribution employeur d'un côté, {v('prime_pays_bas')} de prime de
  l'autre. Le chiffrage ci-dessous dit où en est le paramétrage publié : les
  primes y portent {vc('part_prime_financement')} de la dépense. Une prime
  qui porterait SEULE le financement serait, à l'inverse, la même pour un
  SMIC et pour un très haut revenu : ce n'est pas une assurance solidaire,
  c'est une capitation, et ce n'est pas davantage ce que ce programme
  propose.</li>
</ul>
<p>Un déplacement de cette ampleur fait des gagnants et des perdants, et il
serait malhonnête de ne montrer que les premiers. Trois effets, et nous les
écrivons avant qu'on nous les oppose : la cotisation employeur passe
aujourd'hui de 7 % à 13 % du salaire ENTIER au-delà de 2,5 SMIC, ce qu'une
contribution proportionnelle ne reproduit pas — <strong>les hauts revenus
contribueraient moins</strong> ; une pension ne supporte aujourd'hui aucune
cotisation maladie, alors que la dépense de santé se concentre sur les âges
élevés — <strong>les retraités contribueraient davantage</strong> ; et
l'allocation, resserrée pour que la réforme soit finançable, s'éteint au-dessus
de {vc('seuil_allocation')} bruts par mois — <strong>les salaires modestes et
moyens versent un peu plus</strong>, l'écart s'inversant autour de trois mille
euros bruts par mois. Les deux derniers n'ont pas de réponse qui les annule.
<a href="simulateur.html">Le simulateur le dit pour votre cas</a>, dans les
deux sens, et <a href="objections.html#objection-4">l'objection est écrite</a>.
</p>
<h4>Ce que coûte l'allocation santé</h4>
<p>C'est la seule dépense que cette réforme crée, et un programme qui refuse
de chiffrer ses économies ne peut pas refuser de chiffrer une dépense qu'il
crée. Le calcul ne demande aucun modèle : l'allocation vaut l'écart entre la
prime et le plafond, et il suffit de le sommer sur la distribution des revenus
que l'INSEE publie. Sa méthode est dans le dépôt, ses entrées sont sourcées,
et <code>python3 scripts/cout_allocation.py</code> le refait.</p>
<ul class="serree">
  <li><strong>{vc('allocation_cout')} par an</strong>, et
  <strong>{vc('allocation_net')} net</strong> une fois défalqués les
  {v('aides_complementaire')} d'exonérations et de complémentaire santé
  solidaire que l'État consacre déjà à la couverture complémentaire. Le
  zorgtoeslag néerlandais, qui coûte {v('zorgtoeslag')} pour dix-huit millions
  d'habitants, vaudrait {vc('allocation_repere')} à notre échelle : la nôtre
  est plus serrée, et c'est un choix.</li>
  <li><strong>{vc('allocation_aides')} des adultes la toucheraient</strong>,
  et elle s'éteint au-dessus : c'est un filet, et c'est ce qu'elle doit
  être.</li>
  <li><strong>Les primes portent {vc('part_prime_financement')} du
  financement</strong>, allocation déduite. C'est le nombre à surveiller : la
  prime est le seul étage qu'un assuré peut emporter ailleurs, et chaque euro
  que l'allocation en paie est un euro de moins sur lequel la concurrence a
  prise.</li>
</ul>
<p><strong>Ce que ce calcul nous a fait corriger.</strong> Ce n'est pas le
chiffrage d'un réglage déjà décidé : c'est lui qui a décidé du réglage, et
nous le disons parce que c'est la seule façon de rendre un chiffrage
croyable.</p>
<ul class="serree">
  <li><strong>La prime était calée sur le mauvais dénominateur.</strong> Elle
  valait la moitié du coût moyen par HABITANT, alors que seuls les adultes la
  paient : {v('mineurs')} de mineurs n'en versant aucune, la même moitié doit
  être portée par cinquante-quatre millions d'adultes et non par
  soixante-huit. La prime n'est plus écrite, elle est déduite — personne ne
  peut donc refaire l'erreur.</li>
  <li><strong>Le plafond de l'allocation rendait la loi inapplicable.</strong>
  À 5 % du revenu, l'allocation touchait quatre adultes sur cinq et bornait ce
  que les primes peuvent rapporter au tiers de la dépense : le partage
  moitié-moitié inscrit dans les garanties n'était pas mal calibré, il était
  arithmétiquement impossible. Porté à 8 %, il laisse les primes atteindre
  {vc('prime_encaissement_max')} — au-delà de la moitié de la dépense — et la
  garantie redevient tenable. Le plafond minimal qui la rend possible est de
  {vc('plafond_minimal')} : nous sommes donc au réglage le plus protecteur que
  l'arithmétique autorise.</li>
</ul>
<p>Ce plafond est le seul bouton de réglage de la réforme, et il arbitre entre
deux choses qui vont en sens contraire : plus il est haut, moins l'allocation
coûte et plus la concurrence a de prise, mais moins de monde est protégé.
Voici le barème, pour que l'arbitrage se discute sur des nombres.</p>
{bareme}
<p class="discret">Le réglage retenu est en gras. Les autres ne sont pas moins
défendables : au-dessus il coûte moins et protège moins, en dessous il
protège davantage — mais sous {vc('plafond_minimal')} les primes ne peuvent
plus porter la moitié du financement, et la sixième garantie devient
intenable. C'est un
choix politique que ce tableau rend discutable au lieu de le cacher.</p>
<h4>Ce qu'on peut affirmer</h4>
<ul class="serree">
  <li>La fusion des deux étages supprime un doublon de gestion : deux systèmes
  d'information et deux services sur chaque facture, pour
  {v('frais_gestion_oc')} de frais au second étage et {v('frais_gestion_amo')}
  au premier. Ce que le doublon coûte à lui seul, personne ne le sait au
  milliard près — nous ne l'avançons donc pas.</li>
  <li>La {v('tsa')} de taxe qui pèse aujourd'hui sur les cotisations de
  complémentaire disparaît avec l'étage qu'elle taxait. Sa recette —
  {v('rendement_tsa')}, qui finance la complémentaire santé solidaire — doit
  être reprise dans le nouveau régime : elle l'est par la contribution assise
  sur le revenu, dont l'allocation santé prend le relais.</li>
  <li>À couverture égale, le prélèvement total est destiné à rester constant
  la première année <em>à l'échelle du pays</em> : la réforme redistribue le
  paiement, elle ne le réduit pas d'emblée. À l'échelle d'un assuré, en
  revanche, il change — c'est le propre d'un changement d'assiette, et le
  simulateur ne le cache pas.</li>
  <li>Les mesures d'offre (formation, installation, délégation d'actes) ne
  produisent pas d'économie à court terme. Elles produisent de l'accès aux
  soins, ce qui est leur seul objet.</li>
</ul>
<h4>Ce qu'on ne peut pas affirmer</h4>
<p>Que la réforme économiserait un montant précis. Un tel chiffrage exigerait
un modèle de la dépense de santé, de son élasticité au reste à charge et de la
réaction des offreurs — modèle que ce dépôt ne contient pas, et dont les
estimations disponibles dans la littérature varient trop pour qu'on en tire un
chiffre de tract. <strong>Nous ne l'avançons donc pas.</strong></p>
<p class="discret">Le simulateur de ce site ne chiffre pas non plus l'économie
collective : il montre ce que vous payez aujourd'hui, et ce que vous paieriez
sous des hypothèses explicites et modifiables.
<a href="simulateur.html">Le voir</a> — <a href="donnees.html#simulateur">lire
ses hypothèses</a>.</p>""",
        "financement",
    )

    corps = mesures
    return f"""
{tete}
{g.plan(corps, "Les six mesures")}
{corps}
{financement}

{g.appel(
    "Les objections, une par une.",
    f"Nous avons écrit les {nombre_objections()} objections les plus sérieuses "
    "à ce programme, et nos réponses. Celles auxquelles nous n'avons pas de "
    "bonne réponse y figurent aussi.",
    [("Lire les objections", "objections.html", True),
     ("Ce que vous payez aujourd'hui", "simulateur.html", False)],
)}
"""


# -- le simulateur -----------------------------------------------------------


def simulateur() -> str:
    tete = g.affiche(
        "Ce que vous payez",
        "Votre santé vous coûte " + g.cle_texte("bien plus") + " que votre "
        "mutuelle.",
        "Cotisation maladie de l'employeur, part de la CSG, cotisation de "
        "complémentaire, participations forfaitaires : quatre prélèvements, "
        "dont trois n'apparaissent nulle part en clair. Ce simulateur les "
        "additionne, puis les met en regard des deux étages du système "
        "proposé. Tout se calcule dans votre navigateur : "
        + g.cle_texte("rien n'est envoyé nulle part") + ".",
    )

    formulaire = """
<form class="creme simulateur-court" id="formulaire" method="get" action="#resultat">
  <div class="tete">
    <h2 class="serif">Et vous, ça fait combien&nbsp;?</h2>
    <span class="etiquette">Le simulateur</span>
  </div>
  <div class="grille">
    <div>
      <label for="statut">Situation<span class="aide">celle qui finance votre
      couverture</span></label>
      <select id="statut" name="statut">
        <option value="salarie" selected>Salarié du privé</option>
        <option value="independant">Indépendant</option>
        <option value="retraite">Retraité</option>
      </select>
    </div>
    <div>
      <label for="revenu">Revenu brut mensuel<span class="aide">salaire brut,
      ou pension brute</span></label>
      <input id="revenu" name="revenu" type="number" inputmode="numeric"
             min="0" max="100000" step="10" value="2500">
    </div>
    <div>
      <label for="mutuelle">Complémentaire, par mois<span class="aide">ce que
      vous payez vous-même</span></label>
      <input id="mutuelle" name="mutuelle" type="number" inputmode="numeric"
             min="0" max="1000" step="1" value="35">
    </div>
    <div>
      <label for="enfants">Enfants à charge<span class="aide">ils ne paient
      aucune prime</span></label>
      <input id="enfants" name="enfants" type="number" inputmode="numeric"
             min="0" max="12" step="1" value="0">
    </div>
    <div>
      <label for="franchise">Franchise annuelle souhaitée<span class="aide">dans
      le système proposé</span></label>
      <select id="franchise" name="franchise">
        <option value="0">Aucune franchise</option>
        <option value="300" selected>300 € par an</option>
        <option value="600">600 € par an</option>
        <option value="1200">1 200 € par an</option>
      </select>
    </div>
    <div class="action"><button type="submit">Calculer →</button></div>
  </div>
  <p class="discret" style="margin:0.9rem 0 0">Deux totaux côte à côte, calculés
  séparément : ce que le système actuel prélève sur votre travail pour la
  santé, et ce que la réforme proposée prélèverait sous des hypothèses écrites
  noir sur blanc. L'écart entre les deux est un résultat, pas une promesse.</p>
</form>"""

    resultat = """
<div id="resultat" tabindex="-1">
  <noscript>
    <div class="erreur">Ce simulateur a besoin de JavaScript : le calcul se
    fait dans votre navigateur, il n'y a pas de serveur pour le faire à sa
    place. Les hypothèses et la formule sont lisibles sur la page
    <a href="donnees.html#simulateur">Données et sources</a>.</div>
  </noscript>
</div>"""

    methode = g.depliant(
        "Comment ce calcul est fait",
        f"""
<p>Le simulateur n'a aucun secret : il applique quatre taux publics à votre
revenu, et compare le total à une hypothèse de prime. Voici la formule, dans
l'ordre où elle s'applique.</p>
<h4>Ce que le système actuel prélève</h4>
<ul class="serree">
  <li><strong>Cotisation maladie de l'employeur</strong> :
  {v('cotisation_employeur')} du salaire brut — 7 % jusqu'à 2,5 SMIC annuels,
  13 % sur la totalité au-delà. Elle ne figure pas dans votre salaire net,
  mais elle fait partie de ce que votre travail rapporte.</li>
  <li><strong>Part de la {g.terme('CSG')} affectée à la maladie</strong> :
  {v('csg')} appliqués à 98,25 % du brut, dont une fraction revient à la
  branche maladie. Cette fraction est fixée chaque année par la loi de
  financement ; la valeur retenue ici est un ordre de grandeur, et elle est
  écrite dans <a href="donnees.html#simulateur">les hypothèses</a>.</li>
  <li><strong>Complémentaire santé</strong> : ce que vous versez, plus la part
  payée par votre employeur — au moins 50 % en contrat collectif, et c'est une
  part de votre rémunération, pas un cadeau.</li>
  <li><strong>Participations forfaitaires et franchises médicales</strong> :
  {v('participation')} par consultation et par boîte, plafonnées à 50 € par an
  chacune.</li>
</ul>
<h4>Ce que le système proposé prélèverait</h4>
<p>Deux étages, et le partage entre eux est le choix politique de cette
réforme. La cible est le partage néerlandais, moitié-moitié ; les primes
portent {vc('part_prime_financement')} du financement une fois l'allocation
déduite, et <a href="reforme.html#financement">le chiffrage dit comment on y
est arrivé</a>.</p>
<ul class="serree">
  <li><strong>Une contribution assise sur votre revenu</strong>, qui remplace
  la cotisation maladie de l'employeur et la part de CSG affectée à la santé,
  et qui alimente le fonds de péréquation — pas votre assureur. Le taux retenu
  est une <strong>hypothèse de travail</strong> : son calibrage réel exige un
  modèle budgétaire que ce site ne contient pas, et la page Données le dit.</li>
  <li><strong>Une prime versée à l'assureur que vous choisissez</strong>, égale
  pour tous à l'intérieur d'un contrat. C'est elle, et elle seule, que vous
  emportez ailleurs si votre caisse vous déplaît.</li>
  <li><strong>L'allocation santé</strong>, qui plafonne cette prime à une part
  de votre revenu et se verse directement à l'assureur.</li>
  <li><strong>La franchise que vous choisissez</strong>, dans la limite de
  votre dépense réelle de petit risque. Le simulateur retient une dépense
  moyenne ; la vôtre peut être nulle comme elle peut la dépasser.</li>
  <li><strong>Rien pour vos enfants</strong> : aucune prime n'est due avant 18
  ans, l'État verse la leur au fonds.</li>
  <li><strong>Rien au-delà du bouclier</strong> : le reste à charge est
  plafonné en part du revenu, ce que le calcul applique.</li>
</ul>
<p>Les deux colonnes sont calculées séparément. L'écart entre elles est donc un
résultat, pas une construction — et il n'est pas le même pour tout le monde :
déplacer le financement d'un prélèvement assis sur le travail vers une prime
égale pour tous fait des gagnants et des perdants. Le simulateur le dit pour
votre cas, dans les deux sens.</p>
{g.note(
    "Ce simulateur illustre des ORDRES DE GRANDEUR. Il ne prédit ni votre "
    "prime future, ni votre dépense de santé, et il ne chiffre pas la réforme "
    "à l'échelle du pays — voir <a href='reforme.html#financement'>ce que nous "
    "pouvons affirmer et ce que nous ne pouvons pas</a>. Chacune de ses "
    "hypothèses est écrite, datée et discutable sur la page "
    "<a href='donnees.html#simulateur'>Données et sources</a>.",
    "avertissement")}""",
        "methode-simulateur",
    )

    return f"""
{tete}

{formulaire}

{resultat}

{methode}

{g.appel(
    "Le total vous surprend ? C'est le sujet.",
    "Un prélèvement qu'on ne voit pas n'est jamais discuté. Rendre le prix de "
    "la santé visible est la première mesure de ce programme, et la seule qui "
    "ne coûte rien.",
    [("La réforme en six mesures", "reforme.html", True),
     ("Pourquoi ça coûte autant", "diagnostic.html", False)],
)}
"""


# -- objections --------------------------------------------------------------

# Les objections, et leur nombre.
#
# Elles sont hors de la fonction parce que leur NOMBRE est écrit dans le
# titre de la page, dans son chapeau, dans son sommaire, dans l'appel de la
# page Réforme et dans la description que lisent les moteurs de recherche.
# Un nombre recopié à cinq endroits finit par mentir : celui-ci est déduit.
OBJECTIONS: list[tuple[str, str, str]] = [
        ("C'est la privatisation de la Sécurité sociale.",
         "C'est la fin de son monopole sur l'assurance, pas la fin de son "
         "rôle.",
         """
<p>La Sécurité sociale garde, dans ce programme, trois fonctions dont aucune
n'est marchande : elle définit le panier de soins obligatoire, elle gère la
péréquation des risques entre assureurs, et elle finance l'allocation santé
des ménages modestes. Ce qu'elle perd, c'est l'exclusivité de la gestion du
remboursement — celle que l'Allemagne n'a jamais eue et que les Pays-Bas ont
abandonnée en 2006, sans que la couverture y recule.</p>
<p>Il faut ajouter une remarque désagréable : le monopole de l'assurance
maladie de base coexiste déjà, en France, avec un second étage entièrement
privé, obligatoire en entreprise, et qui paie {part} de la dépense. Le débat
sur le principe est donc clos depuis longtemps ; ce qui reste à discuter est
l'efficacité de l'empilement.</p>"""),
        ("Les assureurs vont sélectionner les bons risques.",
         "Ils y gagneraient, en effet — et c'est pourquoi la péréquation des "
         "risques figure dans la loi, avant l'ouverture de la concurrence.",
         """
<p>Un assureur libre de choisir ses clients choisit les bien portants : c'est
mécanique, et aucune bonne volonté n'y change rien. Le programme y répond par
trois règles cumulatives — obligation d'accepter tout demandeur, prime unique
indépendante de l'état de santé, et versement à chaque assureur de ce que
coûtent réellement ses assurés selon leur âge et leurs pathologies.</p>
<p>Ce dernier mécanisme est le cœur du dispositif : il rend l'assuré malade
aussi rentable que l'assuré sain, et déplace donc la concurrence de la
sélection vers le service. Il fonctionne aux Pays-Bas depuis 2006 et en
Allemagne depuis 1996. Il doit être en service, à blanc, un an avant
l'ouverture — c'est l'ordre du calendrier proposé, et il n'est pas
négociable.</p>"""),
        ("Les plus pauvres ne pourront pas payer la prime.",
         "Ils ne la paieront pas : une allocation santé la couvre, comme la "
         "Suisse le fait pour un quart de sa population.",
         """
<p>Rendre le prix visible ne signifie pas le faire porter à ceux qui ne peuvent
pas le payer. L'allocation santé couvre tout ou partie de la prime et de la
franchise des ménages modestes, selon leur revenu fiscal, et elle est versée
directement à l'assureur : l'assuré n'a aucune avance à faire.</p>
<p>Le mécanisme est plus lisible que l'actuel, qui superpose la complémentaire
santé solidaire, des exonérations de ticket modérateur, des plafonds et des
listes. Une aide dont le montant décroît avec le revenu, sans seuil brutal,
supprime les effets de seuil que le système actuel multiplie.</p>"""),
        ("Votre prime est une capitation : le même montant pour un SMIC et "
         "pour un très haut revenu.",
         "Elle en serait une si elle portait tout le financement. Elle en "
         "porte la moitié, et la loi l'y oblige.",
         """
<p>L'objection vise juste sur un point : une prime égale pour tous EST un
montant égal pour tous, et c'est même à cela qu'elle sert — un prix qu'on peut
comparer, et qu'on emporte ailleurs si l'assureur déçoit. Un prix qui varierait
avec le revenu ne serait plus un prix, et la concurrence n'aurait plus de
prise.</p>
<p>Ce qui rend ce prix acceptable, c'est qu'il ne porte pas seul le
financement. Trois règles l'encadrent, et elles sont dans la loi : la moitié au
moins des ressources reste assise sur le revenu, par une contribution qui
remplace la cotisation employeur et la part de {csg} ; l'allocation santé
plafonne la prime à une part du revenu ; et aucune prime n'est due avant 18
ans. C'est le partage néerlandais — {contribpb} de contribution employeur
d'un côté, {primepb} de prime de l'autre — et il n'a rien d'un détail : il est
la différence entre une assurance solidaire et une capitation. Notre premier
paramétrage n'atteignait d'ailleurs pas cette cible — les primes n'y portaient
que le quart du financement — et c'est
<a href="reforme.html#financement">notre propre chiffrage qui l'a trouvé</a>,
avant qu'on nous le trouve.</p>
<p><strong>Ce que nous ne prétendons pas</strong> : que l'opération soit neutre
pour chacun. Déplacer une partie du financement d'un prélèvement assis sur le
travail vers une prime égale pour tous change qui paie quoi, et dans deux
directions qu'il faut nommer toutes les deux.</p>
<ul class="serree">
  <li>La cotisation maladie d'aujourd'hui passe de 7 % à 13 % du salaire
  ENTIER au-delà de 2,5 SMIC. Une contribution proportionnelle ne reproduit
  pas ce saut : <strong>les hauts revenus contribueraient moins
  qu'aujourd'hui</strong>.</li>
  <li>Une pension ne supporte aucune cotisation maladie et une {csg} au taux
  réduit, alors que la dépense de santé se concentre sur les âges élevés. Une
  contribution assise sur tous les revenus et une prime due par tous les
  adultes prélèveraient <strong>davantage sur les retraités</strong>.</li>
  <li>Et le resserrement de l'allocation, que notre chiffrage a imposé pour
  que la réforme soit finançable, a un prix : elle s'éteint au-dessus de
  {seuilalloc} bruts par mois. <strong>Les salaires modestes et moyens versent
  donc un peu plus qu'aujourd'hui</strong>, l'écart s'inversant autour de
  trois mille euros bruts par mois. Ce plafond est le seul bouton de réglage
  de cette réforme, et il est déjà au cran le plus protecteur que
  l'arithmétique autorise :
  <a href="reforme.html#financement">le chiffrage donne le barème</a>.</li>
</ul>
<p>Les deux derniers points sont les effets les plus impopulaires de cette
réforme, et nous n'avons pas de réponse qui les annule — seulement le constat
que le financement actuel fait porter aux actifs la part que les pensions ne
portent pas, et que ce transfert n'a jamais été voté comme tel. C'est le point le plus discutable
de ce programme, et il se discute sur pièces plutôt qu'en principe :
<a href="simulateur.html">le simulateur affiche l'écart pour votre cas</a>,
dans les deux sens, et le taux de la contribution est une hypothèse écrite —
rien n'interdit de le moduler si la charge doit être répartie autrement.</p>"""),
        ("Qui paie pour les enfants ? Une famille de quatre paierait quatre "
         "primes.",
         "Personne ne paie de prime avant 18 ans. C'est une des garanties "
         "inscrites dans la loi, et c'est la règle néerlandaise.",
         """
<p>L'objection est juste contre une prime par tête appliquée sans règle : au
coût moyen des soins par habitant, une famille de quatre paierait quatre fois
ce montant, et le système serait intenable pour exactement les ménages qu'il
prétend protéger. Il faut donc une règle, et elle doit être écrite.</p>
<p>Elle l'est : <strong>aucune prime n'est due avant 18 ans</strong>. L'État
verse celle des mineurs au fonds de péréquation, qui reverse à leur assureur ce
que leurs soins coûtent réellement — nettement moins que la moyenne, puisque la
dépense de santé se concentre sur les âges élevés. Une famille paie autant de
primes qu'elle compte d'adultes, et l'allocation santé plafonne chacune d'elles
en part du revenu du foyer. C'est ce que font les Pays-Bas depuis 2006.</p>
<p><strong>Ce que cela laisse ouvert</strong> : le cas de l'adulte sans revenu
propre — étudiant, conjoint sans activité, personne au chômage de longue durée.
L'allocation santé couvre alors l'intégralité de la prime, mais la frontière
exacte — foyer fiscal ou personne, et à quel âge la prime commence — relève de
la loi et n'est pas tranchée ici. Nous préférons le dire que laisser croire que
tout est réglé.</p>"""),
        ("La concurrence coûtera plus cher : il faudra payer le marketing "
         "des assureurs.",
         "C'est un coût réel, et il doit être mis en face du coût du doublon "
         "actuel.",
         f"""
<p>Un marché d'assureurs dépense en acquisition de clients ce qu'un monopole ne
dépense pas : c'est exact, et les Pays-Bas comme la Suisse en font
l'expérience. Mais le système français entretient déjà un doublon complet —
deux organismes, deux systèmes d'information, deux gestions sur chaque
facture — dont le seul étage complémentaire coûte {{frais}} par an, auxquels
s'ajoutent {{fraisamo}} pour le premier étage et la taxe qui pèse sur les
cotisations du second. Additionnés, ces frais placent la France au deuxième
rang de l'OCDE pour le coût de gestion de son système de santé, derrière les
États-Unis.</p>
<p>La comparaison honnête n'est donc pas « monopole sobre contre marché
dispendieux », mais « doublon administratif contre concurrence avec frais
commerciaux ». Nous pensons que le second coûte moins ; nous ne prétendons pas
pouvoir le chiffrer au milliard près, et
<a href="reforme.html#financement">nous le disons aussi</a>.</p>"""),
        ("La France a le meilleur système de santé du monde.",
         "Ce classement date de l'an 2000, sa méthode a été abandonnée, et "
         "l'OMS n'en a jamais publié d'autre.",
         """
<p>Le classement de l'Organisation mondiale de la santé qui plaçait la France
au premier rang date de 2000, portait sur des données des années 1990, et
combinait des indicateurs dont la pondération a été si contestée que
l'organisation n'a jamais renouvelé l'exercice. L'invoquer aujourd'hui revient
à juger un pays sur une photographie d'il y a trente ans.</p>
<p>Les indicateurs actuels donnent une image contrastée, et il faut la prendre
entière : l'espérance de vie française reste parmi les meilleures d'Europe et
le reste à charge parmi les plus faibles au monde ; les délais d'accès, la
densité médicale et la mortalité évitable se dégradent. Un système peut être
excellent pour le soin lourd et défaillant pour l'accès — c'est exactement le
cas français.</p>"""),
        ("Avec une franchise, les gens renonceront à se soigner.",
         "C'est l'objection la plus sérieuse, et elle est en partie fondée.",
         """
<p>La littérature économique est claire sur un point : un reste à charge réduit
la consommation de soins utiles autant que celle de soins inutiles, parce que
le patient n'est pas en mesure de faire le tri. C'est le résultat central de
l'expérience RAND, et rien depuis ne l'a infirmé.</p>
<p>D'où trois garde-fous, qui sont des conséquences de cette objection et non
des concessions : la médecine générale, la prévention, le suivi de grossesse et
les soins pédiatriques sont hors du champ de la franchise ; l'allocation santé
la couvre pour les ménages modestes ; et le bouclier sanitaire l'annule dès que
le plafond de reste à charge est atteint.</p>
<p><strong>Ce que nous ne pouvons pas garantir</strong> : qu'aucun renoncement
ne se produise à la marge. Nous soutenons que le renoncement actuel — faute de
rendez-vous, faute de médecin traitant, faute de spécialiste à moins de deux
heures — est plus massif, et qu'il est simplement moins visible parce qu'il ne
figure sur aucune facture.</p>"""),
        ("L'hôpital public ne survivra pas à la concurrence.",
         "Il ne la subit pas : il la pratique déjà, avec les mains liées.",
         """
<p>Les cliniques privées assurent déjà une part importante de la chirurgie et
de l'hospitalisation en France, sous les mêmes tarifs administrés. L'hôpital
public affronte donc la concurrence depuis longtemps, mais sans pouvoir fixer
ses rémunérations, recruter librement, ni arbitrer ses investissements — il en
subit les effets sans en avoir les instruments.</p>
<p>L'autonomie de gestion n'est pas une privatisation : l'hôpital reste public,
son capital reste public, sa mission de service public reste définie par la
loi et financée. Ce qui change, c'est que son directeur et ses équipes
médicales décident au lieu d'appliquer. C'est le statut des hôpitaux publics
allemands et suisses, qui ne sont pas réputés pour leur faiblesse.</p>"""),
        ("Supprimer le numerus clausus ne donnera pas de médecins avant dix "
         "ans.",
         "C'est exact, et c'est pourquoi il fallait le faire il y a vingt ans.",
         f"""
<p>Un médecin se forme en dix à douze ans. La pénurie de {{annee}} est la
conséquence directe des arrêtés des années 1990, qui ont plafonné les
promotions à {{numerus}}. Aucune mesure prise aujourd'hui ne produira de
praticien avant le milieu des années 2030.</p>
<p>Cette objection est donc un argument pour agir maintenant, pas contre. Elle
justifie aussi les mesures à effet rapide qui l'accompagnent : reconnaissance
des diplômes européens, qualification des praticiens à diplôme étranger déjà
en exercice, délégation d'actes aux infirmiers en pratique avancée et aux
pharmaciens, et suppression des tâches administratives qui absorbent
l'équivalent d'une journée de travail hebdomadaire par praticien.</p>"""),
        ("On va vers une médecine à deux vitesses.",
         "Elle existe déjà : elle se compte en mois d'attente et en "
         "kilomètres.",
         """
<p>Aujourd'hui, l'accès rapide à un spécialiste dépend du lieu de résidence, du
réseau personnel, de la capacité à payer un dépassement d'honoraires et de la
qualité du contrat de complémentaire — lequel dépend de l'employeur. Quatre
vitesses, donc, et aucune n'est choisie par le patient.</p>
<p>La question n'est pas de savoir s'il faut une seule vitesse — personne ne
sait produire cela — mais quel mécanisme trie : l'attente et la géographie,
comme aujourd'hui, ou un prix visible avec un bouclier qui empêche qu'il
devienne une barrière. Nous soutenons le second, et nous assumons que ce soit
un choix discutable.</p>"""),
        ("Votre programme n'est pas chiffré.",
         "Il ne l'est pas, et nous refusons de le chiffrer faussement.",
         """
<p>Un chiffrage crédible d'une réforme de l'assurance maladie suppose un modèle
de la dépense de santé, de sa réaction au reste à charge et du comportement des
offreurs. Ce dépôt n'en contient pas, et les estimations disponibles dans la
littérature varient trop pour qu'on en tire un chiffre de tract.</p>
<p>Ce que nous publions à la place : tous nos chiffres avec leur source, leur
millésime et leur degré de fiabilité ; un simulateur dont chaque hypothèse est
écrite et modifiable ; et la liste explicite de ce que nous ne pouvons pas
affirmer. C'est moins spectaculaire qu'un « 30 milliards d'économies », et
c'est plus vérifiable.</p>
<p><strong>Une chose est chiffrée, en revanche, et elle devait l'être</strong> :
l'allocation santé, seule dépense que cette réforme crée. Un programme qui
refuse de chiffrer ses économies ne peut pas refuser de chiffrer une dépense
qu'il invente. Elle coûterait {allocationcout} par an, {allocationnet} net des
aides qu'elle remplace, et elle toucherait {allocationaides} des adultes. Le
calcul ne demande aucun modèle de comportement — c'est une soustraction faite
sur les déciles de revenu de l'INSEE — et il est dans le dépôt, entrées
comprises : <code>python3 scripts/cout_allocation.py</code>.
<a href="reforme.html#financement">Ce qu'il nous oblige à corriger</a> y est
écrit aussi.</p>"""),
]

_EN_LETTRES = {10: "dix", 11: "onze", 12: "douze", 13: "treize",
               14: "quatorze", 15: "quinze", 16: "seize"}


def nombre_objections() -> str:
    """Le nombre d'objections, en toutes lettres, déduit de la liste."""
    return _EN_LETTRES[len(OBJECTIONS)]


def objections() -> str:
    tete = g.affiche(
        "Objections",
        f"Les {nombre_objections()} objections, "
        + g.cle_texte("y compris les bonnes") + ".",
        "Un programme qui ne publie que les objections auxquelles il répond "
        f"bien ne mérite pas d'être lu. Les {nombre_objections()} suivantes "
        "sont celles qu'on nous oppose le plus souvent ; trois d'entre elles "
        "n'ont pas de réponse entièrement satisfaisante, et nous le disons.",
    )


    corps = "".join(
        g.cle(
            question,
            reponse,
            texte
            .replace("{part}", v("part_oc"))
            .replace("{csg}", g.terme("CSG"))
            .replace("{allocationcout}", vc("allocation_cout"))
            .replace("{allocationnet}", vc("allocation_net"))
            .replace("{allocationaides}", vc("allocation_aides"))
            .replace("{seuilalloc}", vc("seuil_allocation"))
            .replace("{contribpb}", v("contribution_pays_bas"))
            .replace("{primepb}", v("prime_pays_bas"))
            .replace("{fraisamo}", v("frais_gestion_amo"))
            .replace("{frais}", v("frais_gestion_oc"))
            .replace("{numerus}", v("numerus"))
            .replace("{annee}", "2026"),
            identifiant=f"objection-{index + 1}",
        )
        for index, (question, reponse, texte) in enumerate(OBJECTIONS)
    )

    return f"""
{tete}
{g.plan(corps, f"Les {nombre_objections()} objections")}
{corps}

{g.appel(
    "Une objection qui manque ?",
    "Ce site est un dépôt ouvert : toute objection sérieuse peut y être "
    "ajoutée, et sa réponse discutée publiquement.",
    [("Ouvrir une discussion", g.DEPOT + "/issues", True),
     ("Relire la réforme", "reforme.html", False)],
)}
"""


# -- données et sources ------------------------------------------------------


def donnees_calculees() -> str:
    """Les chiffres que ce dépôt produit lui-même, et comment il les produit.

    Ils ont leur propre section, et leur propre étiquette — « estimé » —
    parce qu'un chiffre calculé n'a pas la même garantie qu'un chiffre
    recopié d'une publication officielle. Le mélanger aux autres reviendrait à
    lui prêter une autorité qu'il n'a pas ; le cacher reviendrait à refuser de
    chiffrer une dépense qu'on crée.
    """
    chiffres = allocation.chiffres_calcules()
    table = g.tableau(
        ["Chiffre", "Ce qu'il mesure", "Comment il est obtenu", "Fiabilité"],
        [[f'<span id="{cle}">{chiffre_calcule.valeur}</span>',
          chiffre_calcule.libelle,
          "<code>src/sante/allocation.py</code>",
          g.etiquette_fiabilite(chiffre_calcule.fiabilite)]
         for cle, chiffre_calcule in chiffres.items()],
        ["nombre", "long texte", "", ""],
        "Les chiffres que ce site calcule",
    )
    details = "".join(
        g.depliant(f"{chiffre_calcule.valeur} — {chiffre_calcule.libelle}",
                   f"<p>{chiffre_calcule.precision}</p>"
                   f'<p class="discret">{chiffre_calcule.source} · '
                   f"{g.etiquette_fiabilite(chiffre_calcule.fiabilite)}</p>",
                   f"detail-{cle}")
        for cle, chiffre_calcule in chiffres.items()
    )
    limites = "".join(f"<li>{limite}</li>" for limite in allocation.LIMITES)
    return f"""
<h2 id="calculs">Les chiffres que ce site calcule</h2>
<p>Ce site ne modélise rien, et il tient à cette règle. Il fait pourtant deux
calculs, et il faut dire lesquels : celui du simulateur, et le chiffrage de
l'allocation santé. La raison est la même dans les deux cas — un programme qui
refuse de chiffrer ses économies ne peut pas refuser de chiffrer une dépense
qu'il crée. Ce qu'il refuse, c'est d'inventer ce qui exigerait un modèle de
comportement : l'élasticité de la dépense de soins au reste à charge, la
réaction des offreurs. Une somme d'arithmétique sur une distribution publiée
n'est pas de cet ordre.</p>
<p>Ces chiffres portent donc l'étiquette {g.etiquette_fiabilite('estime')},
qui n'est ni « publié » ni « ordre de grandeur » : elle dit qu'un calcul de ce
dépôt les a produits, et que <code>python3 scripts/cout_allocation.py</code>
les refait. Leurs entrées sont dans la table ci-dessus, avec leurs sources.</p>
{table}
<h3>Le détail, chiffre par chiffre</h3>
{details}
<h3>Ce que ce calcul ne sait pas faire</h3>
<ul class="serree">{limites}</ul>
{g.note(
    "Ces limites ne jouent pas toutes dans le même sens, et deux d'entre "
    "elles tirent le coût vers le bas : l'assiette fiscale est plus large que "
    "le revenu disponible, et les déciles modestes comptent plus d'enfants "
    "que d'adultes. Le chiffre publié est donc un MAJORANT, ce qui est la "
    "bonne façon de se tromper quand on chiffre sa propre dépense.",
    "avertissement")}
"""


def page_donnees() -> str:
    tete = g.affiche(
        "Données et sources",
        "Chaque chiffre, " + g.cle_texte("sa source et sa date") + ".",
        "Un chiffre sans source est une opinion. Tous ceux que ce site emploie "
        "sont ici, avec leur millésime, leur origine et leur degré de "
        "fiabilité — y compris ceux que nous vous demandons de vérifier avant "
        "de les citer.",
    )

    lignes = []
    for chiffre in donnees.CHIFFRES:
        source = (f'<a href="{chiffre.lien}">{chiffre.source}</a>'
                  if chiffre.lien else chiffre.source)
        lignes.append([
            f'<span id="{chiffre.cle}">{chiffre.valeur}</span>',
            chiffre.libelle,
            chiffre.annee,
            source,
            g.etiquette_fiabilite(chiffre.fiabilite),
        ])
    table = g.tableau(
        ["Chiffre", "Ce qu'il mesure", "Année", "Source", "Fiabilité"],
        lignes,
        ["nombre", "texte", "date", "long texte", ""],
        "Tous les chiffres cités sur ce site",
    )

    # Les chiffres que le dépôt CALCULE, et qui ne sont donc publiés nulle part
    # ailleurs. Ils ont leur table à eux : les mêler aux chiffres recopiés
    # laisserait croire qu'une source extérieure les garantit.
    calcules = donnees_calculees()

    precisions = "".join(
        g.depliant(
            f"{chiffre.valeur} — {chiffre.libelle}",
            f"<p>{chiffre.precision}</p>"
            f'<p class="discret">{chiffre.source} · {chiffre.annee} · '
            f"{g.etiquette_fiabilite(chiffre.fiabilite)}</p>",
            f"detail-{chiffre.cle}",
        )
        for chiffre in donnees.CHIFFRES if chiffre.precision
    )

    # Engendré depuis la table des paramètres, et non recopié : c'est ici que
    # la page mentait, en annonçant un taux de prime que le calcul n'employait
    # pas et en taisant la moitié de ses hypothèses.
    parametres = g.tableau(
        ["Hypothèse", "Valeur", "Ce qu'elle représente"],
        [[f"<code>{cle_param}</code>", donnees.parametre_affiche(cle_param),
          description]
         for cle_param, (_, description)
         in donnees.DESCRIPTIONS_SIMULATEUR.items()],
        ["", "nombre", "long texte"],
        "Les hypothèses du simulateur, toutes",
    )

    reserves = "".join(
        f"<li><strong>{cle_param}</strong> — {texte}</li>"
        for cle_param, texte in donnees.RESERVES_SIMULATEUR
    )

    methode = g.cle(
        "Comment ce site est fait",
        "Sept pages HTML statiques, engendrées par un script Python depuis un "
        "seul jeu de textes et de chiffres. Aucun serveur, aucune ressource "
        "tierce, aucun traceur.",
        f"""
<ul class="serree">
  <li><strong>Les chiffres n'existent qu'une fois</strong>, dans
  <code>src/sante/donnees.py</code>. Les pages les appellent par leur clé :
  un chiffre ne peut donc pas dire une chose ici et une autre là, et cette
  page-ci est engendrée par la même table.</li>
  <li><strong>Le site ne charge rien d'un tiers.</strong> Les polices, les
  pictogrammes et la feuille de style sont servis par le dépôt. Aucune requête
  vers un serveur extérieur n'emporte votre adresse IP.</li>
  <li><strong>Le simulateur calcule dans votre navigateur.</strong> Aucune
  saisie n'est transmise, enregistrée ni mesurée.</li>
  <li><strong>L'apparence est celle du site
  <a href="{g.SITE_RETRAITES}">retraitecomptenotionelle</a></strong>, dont la
  feuille de style est reprise presque à l'identique : deux volets d'un même
  programme doivent se reconnaître.</li>
  <li><strong>Tout est ouvert</strong> : <a href="{g.DEPOT}">le dépôt</a>
  contient les textes, les chiffres, le script de construction et cette
  page.</li>
</ul>""",
        identifiant="methode",
    )

    limites = g.cle(
        "Ce que ce site ne fait pas",
        "Il ne modélise rien, ne chiffre pas la réforme à l'échelle du pays, "
        "et ne remplace aucune source officielle.",
        f"""
<ul class="serree">
  <li><strong>Aucun modèle de la dépense de santé.</strong> Les chiffres cités
  sont recopiés de publications ; le seul calcul du site est celui du
  simulateur, et il applique des taux publics à un revenu saisi.</li>
  <li><strong>Aucun chiffrage global de la réforme.</strong> Voir
  <a href="reforme.html#financement">ce que nous pouvons affirmer et ce que
  nous ne pouvons pas</a>.</li>
  <li><strong>Des chiffres à vérifier.</strong> Ceux marqués
  {g.etiquette_fiabilite('verifier')} sont de seconde main. Ils doivent être
  confrontés à leur source avant toute reprise publique, et le site le dit
  partout où ils paraissent plutôt que dans une note que personne n'ouvre.</li>
  <li><strong>Aucune valeur officielle.</strong> Pour vos droits, vos
  remboursements et votre couverture, seules votre caisse et
  <a href="https://www.ameli.fr/">ameli.fr</a> font foi.</li>
</ul>""",
        identifiant="limites",
    )

    return f"""
{tete}

<h2>Tous les chiffres</h2>
{table}

<h2>Le détail, chiffre par chiffre</h2>
{precisions}

{calcules}

<h2 id="simulateur">Les hypothèses du simulateur</h2>
<p>Le simulateur applique des taux publics à un revenu saisi, puis compare le
total à une prime hypothétique. Ses paramètres sont écrits une seule fois, dans
<code>src/sante/donnees.py</code>, et déposés dans
<code>moteur/donnees.json</code> que la page lit au chargement.</p>
{parametres}
<h3>Les réserves qui comptent</h3>
<ul class="serree">{reserves}</ul>
{g.note(
    "Les hypothèses marquées « ordre de grandeur » ou « hypothèse de travail » "
    "ne sont pas des mesures. Un débat public sérieux exige qu'on les "
    "distingue des chiffres publiés, et ce site refuse de les présenter "
    "autrement.",
    "avertissement")}

{methode}
{limites}
"""
