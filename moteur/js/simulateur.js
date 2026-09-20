// Le simulateur : ce que la santé prélève sur un revenu, aujourd'hui et sous
// la réforme proposée.
//
// Il tient en un fichier et n'emploie aucune bibliothèque, pour la même raison
// que le reste du site : la page ne demande rien à un tiers, et la promesse
// faite à qui remplit le formulaire — « tout se calcule dans votre navigateur,
// rien n'est envoyé » — ne souffre aucune requête sortante.
//
// Ses paramètres ne sont PAS écrits ici. Ils viennent de `moteur/donnees.json`,
// lui-même écrit depuis `src/sante/donnees.py` : le taux qu'affiche la page
// « Données et sources » et celui qu'applique ce calcul sont le même nombre,
// et ne peuvent pas diverger.
//
// Ce que ce fichier ne prétend pas être : un modèle. Il applique quatre taux
// publics à un revenu saisi, puis décompose le même total en deux parts — ce
// que coûtent vos soins, ce qui finance ceux des autres. Il n'annonce aucune
// économie : le site dit ailleurs qu'il ne sait pas chiffrer la réforme, et il
// ne le saurait pas davantage ici. Les hypothèses sont écrites en toutes
// lettres sous le résultat, parce qu'un chiffre dont on ignore les hypothèses
// ne vaut rien dans un débat.

const FINE = " ";

let PARAMETRES = null;
let RESERVES = [];

// -- mise en forme -----------------------------------------------------------

function nombre(valeur, decimales = 0) {
  return valeur.toFixed(decimales)
    .replace(/\B(?=(\d{3})+(?!\d))/g, FINE)
    .replace(".", ",");
}

function euros(valeur) {
  return `${nombre(Math.round(valeur))}${FINE}€`;
}

function pourcentage(valeur, decimales = 1) {
  return `${nombre(valeur * 100, decimales)}${FINE}%`;
}

function echapper(texte) {
  return String(texte).replace(/[&<>"']/g, (caractere) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#x27;",
  }[caractere]));
}

// -- le calcul ---------------------------------------------------------------

/**
 * Ce que le système actuel prélève pour la santé, sur un an.
 *
 * Quatre lignes, et trois d'entre elles n'apparaissent sur aucun document que
 * reçoit l'assuré. C'est le seul fait que ce simulateur cherche à établir.
 */
function prelevementActuel(saisie) {
  const p = PARAMETRES;
  const brutAnnuel = saisie.revenu * 12;
  const smicAnnuel = p.smic_brut_mensuel * 12;

  // Cotisation maladie de l'employeur. Le taux réduit vaut jusqu'à 2,5 SMIC
  // annuels ; au-delà, le taux plein s'applique à la TOTALITÉ du salaire, et
  // non à la seule fraction qui dépasse — c'est la règle, et elle surprend.
  let cotisation = 0;
  if (saisie.statut === "salarie") {
    const seuil = p.seuil_taux_plein_smic * smicAnnuel;
    const taux = brutAnnuel > seuil ? p.taux_maladie_plein : p.taux_maladie_reduit;
    cotisation = brutAnnuel * taux;
  } else if (saisie.statut === "independant") {
    // Cotisation maladie-maternité des travailleurs indépendants : le taux est
    // progressif avec le revenu, de 0 à 6,5 %. La valeur retenue est le haut de
    // cette fourchette, appliqué au-dessus de 1,1 SMIC — un ORDRE DE GRANDEUR,
    // et la page Données le dit.
    cotisation = brutAnnuel > 1.1 * smicAnnuel ? brutAnnuel * 0.065 : 0;
  }
  // Un retraité ne verse aucune cotisation maladie sur sa pension : sa part du
  // financement passe par la CSG, dont le taux est différent.

  // CSG. Seule la fraction affectée à la branche maladie est comptée ici : la
  // CSG finance aussi la famille, l'autonomie et la dette sociale.
  const tauxCsg = saisie.statut === "retraite"
    ? p.taux_csg_retraite : p.taux_csg;
  const assiette = saisie.statut === "retraite" ? 1 : p.assiette_csg;
  const csgSante = brutAnnuel * assiette * tauxCsg * p.part_csg_maladie;

  // Complémentaire. La part de l'employeur est une part de la rémunération :
  // l'oublier revient à croire qu'une moitié de la cotisation est gratuite.
  const mutuelleAssure = saisie.mutuelle * 12;
  const mutuelleEmployeur = saisie.statut === "salarie"
    ? mutuelleAssure * (p.part_employeur_complementaire
                        / (1 - p.part_employeur_complementaire))
    : 0;

  const participations = p.participations_annuelles;

  const lignes = [
    ["Cotisation maladie de l'employeur", cotisation,
     "Prélevée sur ce que votre travail rapporte, avant votre salaire brut."],
    ["Part de la CSG affectée à la maladie", csgSante,
     "La CSG finance aussi la famille, l'autonomie et la dette sociale : "
     + "seule la fraction santé est comptée ici."],
    ["Complémentaire santé, votre part", mutuelleAssure,
     "Ce que vous versez vous-même, taxe comprise."],
    ["Complémentaire santé, part de l'employeur", mutuelleEmployeur,
     "Au moins la moitié en contrat collectif. C'est une part de votre "
     + "rémunération, pas un cadeau."],
    ["Participations forfaitaires et franchises", participations,
     "2 € par consultation, 1 € par boîte, plafonnés à 50 € par an chacun."],
  ].filter(([, montant]) => montant > 0);

  const total = lignes.reduce((somme, [, montant]) => somme + montant, 0);
  return { lignes, total, brutAnnuel };
}

/**
 * Ce que le système proposé ferait APPARAÎTRE, sous les hypothèses écrites.
 *
 * Ce bloc ne promet aucune économie, et c'est le point le plus important de ce
 * fichier. La réforme proposée ne réduit pas, la première année, ce qui est
 * prélevé : elle en change la FORME. Le calcul ci-dessous décompose donc le
 * même total en deux parts que le système actuel mélange —
 *
 *   * ce que coûtent vos propres soins, c'est-à-dire la prime d'assurance
 *     adossée à la dépense moyenne par habitant, moins l'allocation santé si
 *     la prime dépasse la part du revenu que la loi accepte d'y consacrer ;
 *   * ce qui finance les soins des autres, qui est un choix politique
 *     parfaitement légitime, mais que personne, aujourd'hui, ne peut chiffrer
 *     pour son propre cas.
 *
 * Une économie affichée ici serait une économie inventée : le site dit
 * ailleurs qu'il ne sait pas chiffrer la réforme à l'échelle du pays, et il ne
 * peut pas le savoir davantage à l'échelle d'un contribuable.
 */
function prelevementPropose(saisie, brutAnnuel, totalActuel) {
  const p = PARAMETRES;

  // La prime baisse avec la franchise choisie : c'est le mécanisme suisse, et
  // c'est tout l'intérêt de la franchise. L'abattement vaut une part de la
  // franchise, bornée par ce que le petit risque coûte en moyenne — un
  // assureur ne peut pas rendre plus que ce qu'il cesse de rembourser.
  const franchisePayee = Math.min(saisie.franchise,
                                  p.depense_moyenne_petit_risque);
  const abattement = franchisePayee * 0.6;
  const primePleine = Math.max(0, p.cout_moyen_par_personne - abattement);

  // L'allocation santé : la prime de base ne peut pas dépasser une part du
  // revenu. En dessous de ce seuil, la collectivité paie la différence — c'est
  // le zorgtoeslag néerlandais et la réduction de prime suisse.
  const plafondPrime = brutAnnuel * p.plafond_prime_part_revenu;
  const allocation = Math.max(0, primePleine - plafondPrime);
  const primeNette = primePleine - allocation;

  // Le bouclier : le reste à charge annuel ne peut pas dépasser une part du
  // revenu. Il ne mord presque jamais sur une franchise modeste — c'est voulu,
  // il est là pour la maladie grave, pas pour l'année ordinaire.
  const plafondResteACharge = Math.min(brutAnnuel * p.franchise_part_revenu,
                                       p.franchise_plafond);
  const resteACharge = Math.min(franchisePayee, plafondResteACharge);

  const vosSoins = primeNette + resteACharge;
  // Ce qui reste du prélèvement actuel une fois vos propres soins payés : la
  // solidarité, positive quand vous financez celle des autres, négative quand
  // la collectivité ajoute pour vous.
  const solidarite = totalActuel - vosSoins;

  const lignes = [
    ["Prime d'assurance, au coût moyen des soins", primePleine,
     "La dépense de soins par habitant, diminuée de ce que la franchise "
     + "choisie cesse de faire rembourser."],
    ["Allocation santé reçue", -allocation,
     "Elle plafonne la prime à une part de votre revenu, et se verse "
     + "directement à l'assureur : vous n'avancez rien."],
    ["Franchise, dépense moyenne attendue", resteACharge,
     `Vous ne payez que ce que vous consommez, dans la limite de la franchise `
     + `choisie et du bouclier (${euros(plafondResteACharge)} par an).`],
  ].filter(([, montant]) => montant !== 0);

  return { lignes, total: vosSoins, solidarite, plafondResteACharge };
}

// -- rendu -------------------------------------------------------------------

function tableauLignes(lignes, total, intitule) {
  const corps = lignes.map(([libelle, montant, glose]) => `
    <tr><th scope="row">${echapper(libelle)}<span class="dont">${echapper(glose)}</span></th>
    <td class="nombre">${euros(montant)}</td>
    <td class="nombre">${euros(montant / 12)}</td></tr>`).join("");
  return `<div class="defilant"><table>
    <caption>${echapper(intitule)}</caption>
    <thead><tr><th scope="col">Ce qui est prélevé</th>
      <th scope="col" class="nombre">Par an</th>
      <th scope="col" class="nombre">Par mois</th></tr></thead>
    <tbody>${corps}
      <tr><th scope="row"><strong>Total</strong></th>
      <td class="nombre"><strong>${euros(total)}</strong></td>
      <td class="nombre"><strong>${euros(total / 12)}</strong></td></tr>
    </tbody></table></div>`;
}

function scenario(titre, categorie, total, largeur, classe, glose) {
  return `<div class="scenario">
  <div class="entete">
    <span class="titre">${echapper(titre)}</span>
    <span class="montant">
      <span class="chiffre principal">
        <span class="categorie">${echapper(categorie)}</span>
        <span class="somme">${euros(total)}</span>
        <span class="unite">par an</span>
      </span>
    </span>
  </div>
  <div class="barre ${classe}"><span style="width:${largeur.toFixed(1)}%"></span></div>
  <p class="glose">${glose}</p>
</div>`;
}

function rendre(saisie) {
  const actuel = prelevementActuel(saisie);
  const propose = prelevementPropose(saisie, actuel.brutAnnuel, actuel.total);
  const maximum = Math.max(actuel.total, 1);
  const partDuRevenu = actuel.total / (actuel.brutAnnuel || 1);
  const solidarite = propose.solidarite;

  // La barre de la réforme se lit sur la même échelle que celle du prélèvement
  // actuel : les deux parts y tiennent bout à bout, et leur somme est, par
  // construction, le total d'aujourd'hui. C'est le seul message de ce bloc.
  const partSoins = (propose.total / maximum) * 100;

  const reserves = RESERVES.map(({ parametre, texte }) =>
    `<li><strong>${echapper(parametre)}</strong> — ${echapper(texte)}</li>`).join("");

  const glosesSolidarite = solidarite >= 0
    ? `Le reste — <strong>${euros(solidarite)} par an</strong> — finance les `
      + "soins des autres, la dette de la branche maladie et les frais de "
      + "gestion des deux étages. C'est un choix politique légitime, et "
      + "aujourd'hui personne ne peut le chiffrer pour son propre cas."
    : `Vos soins coûtent <strong>${euros(-solidarite)} de plus par an</strong> `
      + "que ce que vous versez : la différence est financée par les autres "
      + "assurés et par l'impôt. La réforme ne vous retire pas cette aide — "
      + "elle l'écrit noir sur blanc, au lieu de la noyer dans quatre "
      + "prélèvements.";

  return `
<h2>Ce que la santé vous coûte</h2>
${scenario("Le système actuel", "prélevé pour la santé", actuel.total,
    100, "actuel",
    `Soit <strong>${pourcentage(partDuRevenu)}</strong> de votre revenu brut, `
    + `et ${euros(actuel.total / 12)} par mois. Trois de ces quatre lignes `
    + "n'apparaissent sur aucun document que vous recevez.")}
${scenario("La réforme proposée — ce que vos soins coûtent",
    "pour vos propres soins", propose.total, partSoins, "liberal",
    "Prime d'assurance au coût moyen des soins, allocation santé déduite, "
    + "franchise comprise. " + glosesSolidarite)}

${avertissementTotal(actuel.total, propose.total, solidarite)}

<div class="paire">
  <div>${tableauLignes(actuel.lignes, actuel.total,
    "Le détail de ce qui est prélevé aujourd'hui")}</div>
  <div>${tableauLignes(propose.lignes, propose.total,
    "Le détail sous la réforme proposée")}</div>
</div>

<div class="note avertissement">
  <div>
  <p><strong>Ce calcul illustre des ordres de grandeur, il ne prédit rien.</strong>
  La colonne de gauche s'appuie sur des taux publics ; celle de droite sur des
  hypothèses de travail, qui ne sont pas des mesures. Les voici :</p>
  <ul class="serree">${reserves}</ul>
  <p class="discret"><a href="donnees.html#simulateur">Toutes les hypothèses,
  avec leurs sources</a> · <a href="reforme.html#financement">ce que nous ne
  pouvons pas chiffrer</a></p>
  </div>
</div>`;
}

/**
 * La phrase que ce simulateur existe pour écrire.
 *
 * Elle dit que le total ne bouge pas, et que c'est sa DÉCOMPOSITION qui
 * change. Sans elle, deux barres de longueurs différentes se lisent comme une
 * économie — ce qu'elles ne sont pas.
 */
function avertissementTotal(totalActuel, vosSoins, solidarite) {
  const part = solidarite >= 0
    ? `${euros(vosSoins)} pour vos soins, ${euros(solidarite)} pour ceux des autres`
    : `${euros(vosSoins)} pour vos soins, dont ${euros(-solidarite)} financés par les autres`;
  return `<div class="note resume">
  <p><strong>Le total ne baisse pas : il se décompose.</strong> La réforme ne
  promet pas de vous prélever moins la première année — elle promet que les
  ${euros(totalActuel)} prélevés aujourd'hui s'écrivent enfin : ${part}. Un
  prélèvement qu'on ne voit pas n'est jamais discuté, et ce qui n'est jamais
  discuté ne s'améliore pas.</p>
</div>`;
}

// -- démarrage ---------------------------------------------------------------

function lireSaisie(formulaire) {
  const valeur = (nom) => formulaire.elements[nom].value;
  return {
    statut: valeur("statut"),
    revenu: Math.max(0, Number(valeur("revenu")) || 0),
    mutuelle: Math.max(0, Number(valeur("mutuelle")) || 0),
    franchise: Math.max(0, Number(valeur("franchise")) || 0),
  };
}

async function demarrer() {
  const formulaire = document.getElementById("formulaire");
  const sortie = document.getElementById("resultat");
  if (!formulaire || !sortie) { return; }

  try {
    const reponse = await fetch("moteur/donnees.json", { cache: "force-cache" });
    if (!reponse.ok) { throw new Error(`donnees.json (${reponse.status})`); }
    const paquet = await reponse.json();
    PARAMETRES = paquet.parametres;
    RESERVES = paquet.reserves || [];
  } catch (erreur) {
    sortie.innerHTML = '<div class="erreur">Les paramètres du simulateur '
      + "n'ont pas pu être chargés. Le détail du calcul et toutes ses "
      + 'hypothèses restent lisibles sur la page <a href="donnees.html#simulateur">'
      + "Données et sources</a>.</div>";
    return;
  }

  const calculer = (evenement) => {
    if (evenement) { evenement.preventDefault(); }
    sortie.innerHTML = rendre(lireSaisie(formulaire));
  };

  formulaire.addEventListener("submit", calculer);
  // Le résultat suit la saisie : recalculer à chaque changement évite d'avoir
  // à valider pour voir l'effet d'un choix de franchise, qui est justement ce
  // que cette page veut faire éprouver.
  formulaire.addEventListener("change", calculer);
  calculer(null);
}

demarrer();
