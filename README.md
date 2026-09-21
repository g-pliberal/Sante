# Santé — le programme du Parti libéral français

Un site de sept pages qui fait deux choses : **décrire le système de santé
français tel qu'il est**, et **proposer une alternative libérale**, mesure par
mesure, avec ses chiffres, ses sources, ses objections et ses limites.

C'est le volet santé d'un programme dont le volet retraites est
[retraitecomptenotionelle](https://github.com/g-pliberal/retraitecomptenotionelle),
et il en reprend l'apparence : même affiche vert profond, mêmes capitales
massives, même or pour ce qui compte. Deux volets d'un même programme doivent
se reconnaître au premier coup d'œil.

## Les pages

| Fichier | Ce qu'elle fait |
| --- | --- |
| `index.html` | Le programme : quatre engagements chiffrés, la réforme en trois gestes, ce qu'elle change |
| `diagnostic.html` | Le système actuel : comment il marche, ce qu'il coûte, les six défauts qui se tiennent, et ce qu'il ne faut pas casser |
| `comparaisons.html` | Pays-Bas, Suisse, Allemagne, Singapour — quatre couvertures universelles sans monopole, et ce qu'elles ne prouvent pas |
| `reforme.html` | Les six mesures, chacune avec son mécanisme, son effet, et l'objection la plus sérieuse qu'on lui oppose |
| `simulateur.html` | Ce que la santé prélève réellement sur un revenu, et comment ce total se décompose |
| `objections.html` | Dix objections et leurs réponses, y compris les deux auxquelles nous répondons mal |
| `donnees.html` | Tous les chiffres du site, avec leur source, leur millésime et leur degré de fiabilité |

## Construire le site

```sh
python3 scripts/construire_site.py
```

Rien à installer : le script n'utilise que la bibliothèque standard, et écrit à
la racine les sept fichiers HTML que GitHub Pages sert tels quels.

**Les fichiers `*.html` de la racine sont engendrés.** Une correction faite
directement dans l'un d'eux disparaîtrait à la construction suivante : le texte
est dans `src/sante/pages.py`, les chiffres dans `src/sante/donnees.py`, et le
gabarit dans `src/sante/gabarit.py`. Un témoin et une action GitHub vérifient
que les pages du dépôt sont bien celles que le script écrirait.

Pour le regarder dans un navigateur, il faut un serveur : les modules
JavaScript et le paquet de données ne se chargent pas depuis `file://`.

```sh
python3 -m http.server 8765   # puis http://localhost:8765/
```

## Les témoins

```sh
python3 -m unittest discover -s tests
```

Ils vérifient ce qu'un site de programme politique ne peut pas se permettre de
rater : qu'aucune page engendrée n'a divergé de son texte, qu'aucun onglet ne
mène nulle part, que chaque chiffre cité paraît sur la page Données avec sa
source — **et qu'aucun chiffre écrit au fil d'une phrase n'échappe à la
table**, que chaque pays comparé porte son millésime et sa réserve, que toutes
les hypothèses du simulateur sont publiées et qu'il n'en cache aucune dans son
code, et qu'aucune page ne charge de ressource tierce.

## La relecture adverse

[`RELECTURE.md`](RELECTURE.md) lit le programme comme le lirait quelqu'un qui
veut le démolir : ce qui y était faux ou périmé, ce que les témoins ne
vérifiaient pas, et les décisions de fond qui ne sont pas prises — au premier
rang desquelles le financement, qu'une prime forfaitaire ne peut pas porter
seule. Ce n'est pas une page du site : c'est un document de travail, et il
doit rester à jour tant que le programme évolue.

## Comment c'est fait

```
src/sante/donnees.py   les chiffres, leurs sources, leur fiabilité, les pays comparés
src/sante/allocation.py  le chiffrage de l'allocation santé, entrées sourcées
src/sante/gabarit.py   tout ce que le site écrit : bandeau, affiche, cartes, tableaux
src/sante/pages.py     le texte des sept pages
scripts/construire_site.py  assemble les pages et écrit moteur/donnees.json
scripts/cout_allocation.py  refait le chiffrage à voix haute
moteur/style.css       la feuille de style, reprise du site retraites
moteur/js/site.js      le glossaire dépliable — tout le reste se lit sans JavaScript
moteur/js/simulateur.js le seul calcul du site, dans le navigateur
moteur/polices/        Public Sans et Instrument Serif (OFL), servies par le dépôt
moteur/icones/         les pictogrammes originaux de Lucide (ISC)
```

Trois règles tiennent l'ensemble :

1. **Un chiffre n'existe qu'une fois.** Les pages l'appellent par sa clé ; la
   page « Données et sources » est engendrée par la même table. Un chiffre ne
   peut donc pas dire une chose ici et une autre là.
2. **Le site ne charge rien d'un tiers.** Polices, pictogrammes, feuille de
   style : tout vient du dépôt. Une requête vers un serveur extérieur
   emporterait l'adresse IP du lecteur, et la page du simulateur promet le
   contraire.
3. **Le simulateur calcule dans le navigateur.** Aucune saisie n'est
   transmise, enregistrée ni mesurée.

## Sur les chiffres

**Les chiffres marqués « à vérifier » sont de seconde main et doivent être
confrontés à leur source avant toute reprise publique.** Le site le dit
lui-même, sur chaque rangée concernée de la page Données, plutôt que dans une
note que personne n'ouvre. Les trois degrés de fiabilité sont définis en tête
de `src/sante/donnees.py` :

- **publié** — recopié d'une publication officielle nommée ;
- **ordre de grandeur** — arrondi, agrégé ou reconstitué ;
- **à vérifier** — de seconde main, à confronter à la source.

Le site ne chiffre pas la réforme à l'échelle du pays, et
[il explique pourquoi](reforme.html) : un tel chiffrage exigerait un modèle de
la dépense de santé que ce dépôt ne contient pas. Une économie annoncée sans ce
modèle serait inventée.

**Il chiffre en revanche l'allocation santé**, qui est la seule dépense que la
réforme crée — un programme qui refuse de chiffrer ses économies ne peut pas
refuser de chiffrer une dépense qu'il invente. Le calcul ne demande aucun
modèle de comportement : l'allocation vaut l'écart entre la prime et le
plafond, sommé sur les déciles de revenu que publie l'INSEE.

```sh
python3 scripts/cout_allocation.py
```

Son résultat porte l'étiquette « estimé », qui n'est ni « publié » ni « ordre
de grandeur » : elle dit qu'un calcul de ce dépôt l'a produit, et qu'on peut
le refaire. Le script dit aussi ses limites, et elles sont dans le même
fichier que la méthode.

## Licences

- Code : Apache 2.0 (`LICENSE`).
- Textes et contenus du site : CC BY-SA 4.0.
- Polices : SIL Open Font License (`moteur/polices/`).
- Pictogrammes : [Lucide](https://lucide.dev), ISC (`moteur/icones/LICENSE`).
