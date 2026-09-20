# Les pictogrammes du site

Ils viennent tous de **[Lucide](https://lucide.dev) 1.46.0**, sous licence ISC
(`LICENSE`, à côté). Une seule grille — 24 × 24, trait de 2, extrémités et
jointures arrondies —, et rien qui soit dessiné à la main : c'est ce qui les
fait tenir ensemble à toutes les tailles, ce qu'un emoji ou un caractère
Unicode ne font pas, leur dessin changeant d'un système à l'autre.

**Les fichiers de ce dossier sont les originaux.** Le site ne les charge pas :
le gabarit écrit leur tracé DANS la page (`ICONES`, dans
`src/sante/gabarit.py`), parce que la page ne demande aucune ressource à un
tiers — un test du dépôt l'exige.

`../icone.svg` est l'icône du site elle-même : la même grille, le même trait,
le tracé d'`activity` posé sur un carré à l'arrondi de la charte.

## Une réserve, et elle est écrite ici plutôt que tue

`chevron-down.svg`, `circle-help.svg`, `triangle-alert.svg`, `share-2.svg` et
`arrow-left.svg` ont été recopiés sans retouche depuis le dépôt du site
retraites, qui les tient du paquet `lucide-static` 1.46.0.

`activity.svg` n'en vient pas : son tracé a été **transcrit**, et non copié
depuis le paquet. Il faut le confronter à l'original de Lucide avant toute
réutilisation hors de ce site — c'est deux minutes, et cela évite de
redistribuer un dessin qui ne serait pas tout à fait celui qu'il dit être.

## Ajouter un pictogramme

1. Récupérer le fichier chez Lucide, sans le retoucher, et le déposer ici.
2. Recopier son contenu — les seuls `<path>`, `<circle>`, `<line>` — dans la
   table `ICONES` de `src/sante/gabarit.py`.
3. Ne jamais changer l'enveloppe : c'est elle qui donne la grille commune.
