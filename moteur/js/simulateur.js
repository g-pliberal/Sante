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
// publics à un revenu saisi, puis calcule SÉPARÉMENT ce que prélèveraient les
// deux étages du système proposé — une contribution assise sur le revenu, une
// prime versée à l'assureur choisi. L'écart entre les deux colonnes est donc
// un résultat, et non une construction : il se dit, quel que soit son signe.
// Il n'annonce aucune économie collective — le site dit ailleurs qu'il ne sait
// pas chiffrer la réforme, et il ne le saurait pas davantage ici. Les
// hypothèses sont écrites en toutes lettres sous le résultat, parce qu'un
// chiffre dont on ignore les hypothèses ne vaut rien dans un débat.

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
    cotisation = brutAnnuel > p.seuil_independant_smic * smicAnnuel
      ? brutAnnuel * p.taux_maladie_independant : 0;
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
 * Ce que le système proposé prélèverait, sous les hypothèses écrites.
 *
 * La prime et le plafond de l'allocation ont été corrigés APRÈS chiffrage :
 * une prime calée sur la moitié du coût par habitant ne pouvait pas lever sa
 * moitié, puisque les mineurs n'en paient aucune, et un plafond à 5 % du
 * revenu bornait ce que les primes peuvent rapporter au tiers de la dépense.
 * Voir `src/sante/allocation.py`.
 *
 * Deux étages, et c'est tout le sujet. Une réforme qui ferait porter le
 * financement de la santé à une prime forfaitaire seule serait une capitation :
 * le même montant pour un SMIC et pour un très haut revenu. Ce n'est pas ce que
 * pratiquent les pays dont ce programme s'inspire, et ce n'est pas ce qu'il
 * propose.
 *
 *   * une CONTRIBUTION ASSISE SUR LE REVENU, qui remplace la cotisation
 *     maladie de l'employeur et la part de CSG affectée à la santé, et qui
 *     alimente le fonds de péréquation — pas votre assureur ;
 *   * une PRIME versée à l'assureur que vous avez choisi, égale pour tous à
 *     l'intérieur d'un contrat, et c'est elle qui porte la concurrence.
 *
 * La loi néerlandaise fixe ses taux pour que le partage reste à moitié-moitié.
 * Le paramètre `part_prime_nominale` est ce partage, et il est le choix
 * politique de cette réforme : la page Données le dit en toutes lettres.
 */
function prelevementPropose(saisie, brutAnnuel) {
  const p = PARAMETRES;

  const contribution = brutAnnuel * p.taux_contribution_revenu;

  // La prime baisse avec la franchise choisie : c'est le mécanisme suisse, et
  // c'est tout l'intérêt de la franchise. L'abattement vaut une part de la
  // franchise, bornée par ce que le petit risque coûte en moyenne — un
  // assureur ne peut pas rendre plus que ce qu'il cesse de rembourser.
  const franchisePayee = Math.min(saisie.franchise,
                                  p.depense_moyenne_petit_risque);
  const abattement = franchisePayee * p.part_franchise_rendue;
  const primePleine = Math.max(0, p.prime_nominale - abattement);

  // L'allocation santé : la prime ne peut pas dépasser une part du revenu. En
  // dessous de ce seuil, la collectivité paie la différence — c'est le
  // zorgtoeslag néerlandais et la réduction de prime suisse.
  const plafondPrime = brutAnnuel * p.plafond_prime_part_revenu;
  const allocation = Math.max(0, primePleine - plafondPrime);
  const primeNette = primePleine - allocation;

  // Le bouclier : le reste à charge annuel ne peut pas dépasser une part du
  // revenu. Il ne mord presque jamais sur une franchise modeste — c'est voulu,
  // il est là pour la maladie grave, pas pour l'année ordinaire.
  const plafondResteACharge = Math.min(brutAnnuel * p.franchise_part_revenu,
                                       p.franchise_plafond);
  const resteACharge = Math.min(franchisePayee, plafondResteACharge);

  const lignes = [
    ["Contribution santé assise sur votre revenu", contribution,
     "Elle remplace la cotisation maladie de l'employeur et la part de CSG, "
     + "et va au fonds de péréquation — pas à votre assureur."],
    ["Prime de votre assureur", primePleine,
     "Égale pour tous à l'intérieur d'un contrat : ni l'âge, ni le sexe, ni "
     + "l'état de santé ne la modulent. C'est la moitié de la dépense de "
     + "santé rapportée aux adultes qui la paient."],
    ["Allocation santé reçue", -allocation,
     "Elle plafonne la prime à une part de votre revenu, et se verse "
     + "directement à l'assureur : vous n'avancez rien."],
    ["Franchise, dépense moyenne attendue", resteACharge,
     `Vous ne payez que ce que vous consommez, dans la limite de la franchise `
     + `choisie et du bouclier (${euros(plafondResteACharge)} par an).`],
  ].filter(([, montant]) => montant !== 0);

  // Zéro, et il faut le VOIR : c'est la réponse à la question qu'on posera en
  // premier. Une ligne absente se lit comme une ligne oubliée.
  if (saisie.enfants > 0) {
    lignes.push(["Prime de vos enfants à charge", 0,
      "Aucune prime avant 18 ans : l'État verse la leur au fonds. Une famille "
      + "ne paie pas autant de primes qu'elle compte de têtes."]);
  }

  const total = contribution + primeNette + resteACharge;
  return { lignes, total, contribution, primeNette, resteACharge };
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
  const propose = prelevementPropose(saisie, actuel.brutAnnuel);
  const echelle = Math.max(actuel.total, propose.total, 1);
  // Sans revenu saisi, une part de revenu ne veut rien dire : la division par
  // un dénominateur de secours affichait « 10 000 % de votre revenu brut ».
  const partDuRevenu = actuel.brutAnnuel > 0
    ? `Soit <strong>${pourcentage(actuel.total / actuel.brutAnnuel)}</strong> `
      + `de votre revenu brut, et ${euros(actuel.total / 12)} par mois. `
    : `Soit ${euros(actuel.total / 12)} par mois. `;

  // Les deux barres se lisent sur la MÊME échelle, celle du plus grand des
  // deux totaux. Rapporter la seconde au prélèvement actuel la faisait
  // déborder de son cadre dès que les soins d'un assuré coûtent plus que ce
  // qu'il verse — le cas de toute pension modeste, c'est-à-dire le cas où la
  // capture d'écran est la plus facile à retourner contre nous.
  const partActuel = (actuel.total / echelle) * 100;
  const partSoins = (propose.total / echelle) * 100;

  const reserves = RESERVES.map(({ parametre, texte }) =>
    `<li><strong>${echapper(parametre)}</strong> — ${echapper(texte)}</li>`).join("");

  const partPrime = propose.primeNette / (propose.total || 1);

  return `
<h2>Ce que la santé vous coûte</h2>
${scenario("Le système actuel", "prélevé pour la santé", actuel.total,
    partActuel, "actuel",
    partDuRevenu + "Trois de ces quatre lignes n'apparaissent sur aucun "
    + "document que vous recevez.")}
${scenario("La réforme proposée", "prélevé pour la santé", propose.total,
    partSoins, "liberal",
    `Une contribution assise sur votre revenu (${euros(propose.contribution)}) `
    + `et une prime versée à l'assureur que vous choisissez `
    + `(${euros(propose.primeNette)}).`
    + (propose.primeNette > 0
      ? ` Soit <strong>${pourcentage(partPrime)}</strong> du total qui dépend `
        + "de votre assureur plutôt que de votre fiche de paie — et c'est sur "
        + "cette part-là que vous pouvez agir en partant ailleurs."
      : " À ce niveau de revenu, l'allocation santé couvre la prime en "
        + "entier : vous choisissez votre assureur sans rien lui verser."))}

${avertissementTotal(actuel.total, propose, saisie.statut)}

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
 * Elle disait autrefois que le total ne bouge pas, et c'était une pétition de
 * principe : le total était CONSTRUIT constant, puisque la part « solidarité »
 * n'était que le reste d'une soustraction. Les deux colonnes sont désormais
 * calculées séparément, et leur écart est donc un résultat. Il se dit.
 */
function avertissementTotal(totalActuel, propose, statut) {
  const ecart = propose.total - totalActuel;
  const sens = Math.abs(ecart) < totalActuel * 0.02
    ? "À votre niveau de revenu, les deux totaux sont du même ordre."
    : ecart < 0
      ? `À votre niveau de revenu, la réforme prélèverait `
        + `<strong>${euros(-ecart)} de moins par an</strong>.`
      : `À votre niveau de revenu, la réforme prélèverait `
        + `<strong>${euros(ecart)} de plus par an</strong>.`;
  // Les deux cas qu'il serait le plus tentant de taire, et les plus coûteux à
  // taire : ils ne se découvrent pas, ils s'écrivent.
  let pourquoi = "";
  if (ecart > 0 && statut === "retraite") {
    pourquoi = " Une pension ne supporte aujourd'hui aucune cotisation "
      + "maladie et une CSG au taux réduit, alors que la dépense de santé se "
      + "concentre sur les âges élevés : une contribution assise sur tous les "
      + "revenus et une prime due par tous les adultes prélèvent donc "
      + "davantage sur elle. C'est l'effet le plus impopulaire de cette "
      + "réforme, et nous n'avons pas de réponse qui l'annule.";
  } else if (ecart > 0) {
    pourquoi = " À ce niveau de revenu, l'allocation santé ne couvre plus la "
      + "prime : elle s'éteint un peu au-dessus du SMIC, et l'écart entre les "
      + "deux systèmes s'inverse autour de trois mille euros bruts par mois. "
      + "Le plafond de l'allocation est le seul bouton de réglage de cette "
      + "réforme — le relever protège plus de monde et coûte plus cher, et "
      + "<a href=\"reforme.html#financement\">le barème est publié</a>.";
  }
  return `<div class="note resume">
  <p><strong>Ce que ce chiffre est, et ce qu'il n'est pas.</strong> ${sens}${pourquoi}
  Cet écart n'est pas une économie : c'est la conséquence arithmétique d'un
  taux de contribution qui est une hypothèse de travail, appliqué à un seul
  cas. Un système qui déplace le financement d'un prélèvement assis sur le
  travail vers une prime égale pour tous fait forcément des gagnants et des
  perdants, et il serait malhonnête de ne montrer que les premiers. ${
    propose.total > 0
      ? `Ce que la réforme promet, c'est que les ${euros(propose.total)} `
        + `soient enfin ÉCRITS : ${euros(propose.contribution)} de `
        + `contribution, ${euros(propose.primeNette)} de prime que vous pouvez `
        + "emporter ailleurs."
      : "Ce que la réforme promet, c'est que ce qui est prélevé soit enfin "
        + "écrit : une contribution et une prime, l'une et l'autre visibles."
  } Un prélèvement qu'on ne voit pas n'est jamais discuté, et ce qui n'est
  jamais discuté ne s'améliore pas.</p>
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
    enfants: Math.max(0, Number(valeur("enfants")) || 0),
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
