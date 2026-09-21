# Relecture adverse

Ce document lit le programme comme le lirait quelqu'un qui veut le démolir.
Il n'est pas publié sur le site : c'est un document de travail, et il doit
rester à jour tant que le programme évolue.

La méthode est celle du site lui-même — écrire l'objection avant qu'on nous
l'oppose. Elle est appliquée ici au site entier, chiffres compris.

**Un avertissement, d'abord.** Un programme « indiscutable » n'existe pas, et
le viser est le plus sûr moyen d'être discrédité : il suffit d'un chiffre faux
pour que tout le reste soit soupçonné. Ce qui existe, c'est un programme dont
chaque affirmation tient quand on la vérifie, et dont les faiblesses sont
annoncées par nous plutôt que découvertes par d'autres. Le site avait déjà
cette discipline. Elle n'était pas tenue partout.

---

## 1. Les cinq points qui coûteraient le débat

Ceux-ci ne sont pas des erreurs de rédaction : ce sont des décisions de fond
qui n'avaient pas été prises.

**Trois l'ont été depuis** (1.1, 1.2, 1.5), et le programme porte désormais
l'architecture correspondante : financement à deux étages, moitié-moitié,
aucune prime avant 18 ans. **Une reste ouverte** (1.4), **une est chiffrée et attend
un arbitrage** (1.3), et **une troisième est apparue en chemin** — voir la
section 1.6, qui est la plus importante de ce document.

### 1.1 La prime forfaitaire ne peut pas remplacer la cotisation et la CSG

C'est le point le plus grave, et il est structurel.

La page d'accueil écrit que l'assuré paiera « une prime unique […] qui
remplace la cotisation maladie de votre employeur, la part de CSG affectée à
la santé et votre complémentaire ». Le simulateur adosse cette prime au coût
moyen des soins par habitant — 3 700 €.

Faites tourner le calcul sur les cas qu'un journaliste essaiera — voici ce que
donnait le programme **avant correction** :

| Salaire brut | Prélevé aujourd'hui | « Vos soins » sous la réforme |
| --- | --- | --- |
| 1 500 €/mois | 2 855 € | 2 100 € |
| 2 500 €/mois | 4 531 € | 3 300 € |
| 5 000 €/mois | 12 083 € | 3 820 € |
| 8 000 €/mois | 18 793 € | 3 820 € |

Lu tel quel, le programme divise par cinq la contribution santé d'un cadre
supérieur. Le simulateur le masque en appelant « solidarité » la différence et
en posant que le total ne bouge pas — mais cette constance est une hypothèse
du simulateur, pas une conséquence de la réforme. Si la prime *remplace*
réellement la cotisation et la CSG, le financement s'effondre par le haut.

**Et le modèle invoqué dit le contraire.** Aux Pays-Bas, la prime nominale ne
finance que la moitié de l'assurance de base ; l'autre moitié vient d'une
contribution assise sur le revenu, prélevée par l'employeur (6,10 % en 2026,
plafonnée à 79 409 €), et la loi fixe les taux pour que le partage reste à
50-50. Présenter le modèle néerlandais comme une prime forfaitaire, c'est en
présenter la moitié — et c'est la moitié qui porte la progressivité.

**Recommandation.** Adopter explicitement l'architecture néerlandaise :
une contribution assise sur le revenu qui alimente le fonds de péréquation,
et une prime nominale, plus petite, qui porte la concurrence. Le programme y
gagne trois choses : il devient finançable, il cesse d'être attaquable comme
une capitation, et il correspond enfin au pays qu'il cite.

**Décidé.** Le programme adopte désormais cette architecture : une
contribution assise sur le revenu qui remplace la cotisation employeur et la
part de CSG et alimente le fonds de péréquation, et une prime versée à
l'assureur choisi qui remplace la complémentaire. Le partage moitié-moitié est
la sixième garantie inscrite dans la loi. Le simulateur calcule les deux étages
séparément, et l'écart entre les deux colonnes est donc un résultat, non plus
une construction.

### 1.2 Rien n'est dit des enfants ni des familles

La prime est un montant par personne. Le programme ne dit nulle part si un
enfant en paie une. Aux Pays-Bas, les mineurs n'en paient aucune : l'État
verse la leur au fonds. Sans règle équivalente, l'arithmétique du site donne
14 800 € par an pour une famille de quatre, et personne n'aura besoin de la
calculer longtemps.

**Décidé.** *Aucune prime avant 18 ans* est la septième garantie, et
l'objection « qui paie pour les enfants ? » figure sur la page Objections. Le
simulateur prend le nombre d'enfants à charge et affiche leur ligne à zéro —
une ligne absente se lirait comme une ligne oubliée.

### 1.3 Le coût de l'allocation santé — chiffré, et ce qu'il révèle

Le passage à deux étages a beaucoup amélioré ce point : la prime n'est plus de
3 520 € mais de 1 670 €, et le plafond est descendu de 10 % à 5 % du revenu.
L'allocation se déclenche désormais sous **2 783 € brut par mois** au lieu de
2 933 €, et elle ne comble qu'un écart bien plus petit — 770 € à 1 500 € brut,
contre 1 720 € auparavant.

Elle reste néanmoins versée à une large partie des salariés, et **son coût
budgétaire n'est chiffré nulle part**. Le programme refuse — à raison — de
chiffrer ses économies. Il ne peut pas refuser de chiffrer une dépense qu'il
crée.

**Chiffré.** `src/sante/allocation.py` somme l'écart entre la prime et le
plafond sur les dix déciles de niveau de vie publiés par l'INSEE, et
`python3 scripts/cout_allocation.py` le refait. Aucun modèle de comportement
n'intervient : c'est une soustraction faite dix fois.

| | Avec les paramètres actuels |
| --- | --- |
| Coût brut, assiette individuelle | **29 Md€/an** |
| Coût brut, assiette de foyer | 43 Md€/an |
| Net des 10 Md€ déjà dépensés (Cour des comptes) | **19 Md€/an** |
| Adultes concernés | **80 %** |
| Repère : le zorgtoeslag néerlandais transposé | 25 Md€/an |

Le repère néerlandais confirme l'ordre de grandeur, ce qui est la seule chose
qu'on lui demande. Deux des limites du calcul tirent vers le bas — l'assiette
fiscale est plus large que le revenu disponible, et les déciles modestes
comptent plus d'enfants que d'adultes : **le chiffre publié est un majorant**,
ce qui est la bonne façon de se tromper quand on chiffre sa propre dépense.

**Mais le calcul a trouvé autre chose, et c'est plus grave que le coût.**

À un plafond de 5 % du revenu, les primes ne peuvent pas rapporter plus de
**84 Md€, soit le tiers de la dépense de santé — quelle que soit leur
hauteur**. Au-delà d'un certain montant, tout le monde est au plafond : chaque
euro ajouté à la prime est intégralement repris par l'allocation, et
l'assureur n'encaisse rien de plus. Le partage moitié-moitié inscrit dans les
garanties n'est donc pas mal calibré : il est **arithmétiquement impossible**.

S'y ajoute une erreur de calage plus simple : la prime vaut la moitié du coût
moyen par HABITANT, alors que seuls les adultes la paient. Quatorze millions et
demi de mineurs ne versant rien, la même moitié doit être portée par 54
millions d'adultes et non par 68 — la prime juste est de 2 311 €, pas 1 850 €.

**À décider par vous.** Le chiffrage évalue la sortie, et le site la publie
sans l'adopter :

| Prime | Plafond | Allocation | Adultes aidés | Part des primes |
| --- | --- | --- | --- | --- |
| 1 850 € | 5 % | 29 Md€ | 80 % | 28 % |
| 2 311 € | 8 % | 22 Md€ | 60 % | 41 % |
| **2 311 €** | **10 %** | **13 Md€** | **40 %** | **45 %** |
| 2 311 € | 12 % | 8 Md€ | 20 % | 47 % |

La ligne à 10 % est celle que je recommande : l'allocation redevient un filet
plutôt qu'un régime, son coût passe sous celui des aides qu'elle remplace, et
les primes portent enfin près de la moitié du financement — donc la
concurrence retrouve la prise que l'allocation lui retirait. C'est un
paramétrage, pas une refonte : deux nombres dans `PARAMETRES_SIMULATEUR`.

### 1.4 Le bouclier fait payer ce que l'ALD rembourse

Le calendrier affirmait : « Aucun patient en ALD ne perd de droits : le
plafond est, pour eux, immédiatement atteint. » C'est faux deux fois — un
plafond se paie *avant* d'être atteint, et beaucoup de patients en ALD, dont
la dépense est modeste, ne l'atteindraient pas.

Avec les paramètres du simulateur (4 % du revenu, plafonné à 1 500 €) —
inchangés par le passage à deux étages — un patient en ALD gagnant 2 500 €
brut par mois passerait d'un remboursement intégral à un reste à charge
pouvant aller jusqu'à 1 200 € par an.
« Ils font payer 1 200 € par an aux malades du cancer » est le titre, et il
serait techniquement exact.

La formulation du site a été corrigée pour nommer l'arbitrage. **Le calibrage
du plafond pour les affections longues reste à décider**, et il doit figurer
dans la loi, pas dans un décret.

### 1.5 Supprimer la complémentaire supprime 6,5 Md€ de recette

La taxe de solidarité additionnelle rapporte environ 6,5 Md€ par an et finance
la complémentaire santé solidaire — celle des ménages les plus modestes. Le
programme faisait disparaître la taxe « avec l'étage qu'elle taxait » sans
dire par quoi la recette est remplacée.

**Décidé.** La recette est reprise par la contribution assise sur le revenu,
dont l'allocation santé prend le relais pour les ménages modestes ; la page
Réforme le dit à l'endroit où l'argent est décrit.

### 1.6 Les retraités paieraient davantage — et c'est le vrai coût politique

Ce point n'était pas visible avant, parce que l'ancien simulateur construisait
le total de la réforme comme égal à celui d'aujourd'hui. Les deux colonnes
étant désormais calculées séparément, il apparaît, et il est structurel.

Une pension ne supporte aucune cotisation maladie et une CSG au taux réduit,
alors que la dépense de santé se concentre sur les âges élevés. Une
contribution assise sur tous les revenus et une prime due par tous les adultes
prélèvent donc nettement plus sur elle. Avec les paramètres actuels :

| Cas | Prélevé aujourd'hui | Sous la réforme |
| --- | --- | --- |
| Salarié, 2 500 €/mois | 4 531 € | 4 200 € |
| Salarié, 8 000 €/mois | 18 793 € | 9 650 € |
| **Retraité, 2 500 €/mois** | **2 790 €** | **4 200 €** |

Le programme dit maintenant les deux effets — les hauts revenus contribuent
moins, les retraités davantage — sur la page Réforme, dans l'objection
« capitation », et dans le simulateur lui-même, qui affiche la phrase quand
c'est le cas de l'utilisateur. Aucune réponse ne l'annule : il n'en existe
pas. Le seul argument disponible est que le financement actuel fait porter aux
actifs la part que les pensions ne portent pas, et que ce transfert n'a jamais
été voté comme tel.

**À décider par vous.** Trois voies, et elles ne se valent pas
politiquement :

1. **Assumer.** C'est cohérent avec le reste du programme, et c'est un choix
   qui se défend — mais il faut savoir qu'il désigne l'électorat le plus
   nombreux et le plus votant comme perdant.
2. **Moduler la contribution** selon la nature du revenu, comme la CSG le fait
   déjà. Techniquement simple, mais cela entame l'argument de lisibilité.
3. **Étaler.** Faire converger les taux sur la durée du mandat plutôt qu'à la
   bascule.

Tant que ce n'est pas tranché, la phrase du simulateur reste la bonne : nous
n'avons pas de réponse qui l'annule, et nous le disons.

---

## 2. Ce qui était faux, périmé, ou mal nommé — corrigé

Chacun de ces points était une prise directe. Tous sont corrigés dans ce
commit.

| Où | Ce qui était écrit | Ce qui est vrai |
| --- | --- | --- |
| Accueil, titre | « La santé la plus chère d'Europe » | L'Allemagne dépense davantage — et le tableau du site le disait déjà. Contredire sa propre page est le pire des cas. |
| Accueil, titre | « six mois pour un rendez-vous » | Aucune source. La DREES mesure 52 jours en médiane chez l'ophtalmologue, 2 jours chez le généraliste. |
| Données | TSA à 13,27 % | 15,27 % depuis la LFSS 2025. |
| Données, accueil | Déficit maladie ≈ 14 Md€ (2024) | 15,9 Md€ en 2025. |
| Réforme, mesure 1 | « taxe spéciale sur les conventions d'assurance » | C'est la *taxe de solidarité additionnelle*. La TSCA est une autre taxe. |
| Réforme, mesure 1 | Les 7,6 Md€ de gestion « reviennent dans le soin » | Un assureur unique garde des frais ; le premier étage en a déjà 7,3 Md€. Ce que la fusion économise, c'est le doublon — dont le montant n'est pas connu. |
| Réforme, mesure 3 | « Aucun patient en ALD ne perd de droits » | Voir 1.4. |
| Comparaisons | Franchise néerlandaise « environ 400 € » | 385 €, inchangée depuis 2016. |
| Comparaisons | « trois d'entre eux dépensent moins que nous » | Dépend de l'édition OCDE retenue : selon l'édition, la Suisse passe devant ou derrière la France. |
| Comparaisons | Parts de PIB sans source ni millésime | Les quatre pays portent désormais leur source, leur année et leur réserve. |
| Données | Hypothèse publiée `taux_prime_liberale` à 9 % | **Ce paramètre n'existait pas.** Le calcul employait `cout_moyen_par_personne` (3 700 €). La page publiait une hypothèse fausse et en taisait huit autres. |

Le dernier point est le plus embarrassant des douze, parce qu'il touche la
promesse centrale du site : *« un chiffre n'existe qu'une fois »*. Le tableau
des hypothèses était recopié à la main. Il est maintenant engendré depuis la
table des paramètres, et ne peut plus diverger.

---

## 3. Ce que le site ne vérifiait pas de lui-même

Les témoins vérifiaient que **tout chiffre déclaré paraît sur la page
Données**. Ils ne vérifiaient pas la réciproque — qu'aucun chiffre écrit au
fil d'une phrase n'échappe à la table. C'est par ce trou que « six mois pour
un rendez-vous » s'était installé en tête de la page d'accueil.

Quatre témoins ont été ajoutés :

- `test_aucun_chiffre_orphelin` — tout nombre suivi de `%`, `€`, `Md€`,
  « millions » ou « milliards » doit venir de `donnees.py`, ou figurer dans
  `CHIFFRES_TOLERES` avec la raison écrite ;
- `test_chaque_tolerance_est_justifiee_et_sert` — une tolérance sans raison,
  ou devenue inutile, doit disparaître ;
- `test_chaque_parametre_parait_dans_la_page_donnees` — la page qui prétend
  donner toutes les hypothèses doit les donner toutes ;
- `test_le_calcul_n_emploie_aucun_nombre_qui_lui_soit_propre` — le simulateur
  ne peut plus contenir de constante écrite en dur. Il en avait trois
  (le taux des indépendants, son seuil, et la part de la franchise rendue en
  baisse de prime) ; elles sont désormais dans `donnees.py`, donc publiées.

Vérifié par sabotage : chacun échoue quand on réintroduit la faute.

Corrigé au passage : la barre du simulateur débordait de son cadre dès que les
soins d'un assuré coûtaient plus que ce qu'il verse — le cas de toute pension
modeste, c'est-à-dire le cas dont la capture d'écran est la plus facile à
retourner contre nous.

---

## 4. Ce qui reste à faire, par ordre d'urgence

1. **Vérifier les trois chiffres « à vérifier » qui paraissent en page
   d'accueil** : dette sociale, frais de gestion des complémentaires,
   personnes sans médecin traitant. Un adversaire n'a qu'à citer notre propre
   étiquette : « leur site dit lui-même que le chiffre n'est pas vérifié ».
   Rien ne devrait figurer sur la page d'accueil sans être « publié ».
2. **Reprendre le tableau des comparaisons dans une seule édition** du Système
   de comptes de la santé de l'OCDE, les cinq lignes ensemble. Deux chiffres
   vrais pris dans deux éditions font un tableau faux.
3. **Rafraîchir les millésimes.** Le site est calé sur 2023-2025 ; l'ONDAM et
   la LFSS ont changé depuis. Un programme publié en 2026 avec des chiffres de
   2023 se fait répondre sur la date, pas sur le fond.
4. **Trancher 1.3, 1.4 et 1.6** — le calibrage de l'allocation, le plafond du
   bouclier pour les affections longues, et le sort des retraités. Le
   troisième est le plus coûteux politiquement, et c'est celui qui n'a pas de
   réponse technique.
5. **Trancher le recalibrage de l'allocation** (tableau en 1.3). Deux nombres
   à changer, et ils décident si l'allocation est un filet ou un régime.
6. **Calibrer `taux_contribution_revenu`.** Les 8 % retenus sont l'ordre de
   grandeur qu'exige la moitié d'une dépense de 250 Md€ rapportée à l'assiette
   de la CSG. Un économiste doit le refaire sur l'assiette réelle avant toute
   publication : c'est le paramètre dont dépendent tous les écarts affichés
   par le simulateur.
7. **Faire relire par un contradicteur réel.** Ce document est une relecture
   interne ; elle trouve ce qu'elle sait chercher.
