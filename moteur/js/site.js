// Le script commun aux sept pages, et il ne fait qu'une chose : ouvrir les
// définitions du glossaire. Tout le reste du site est du HTML statique, lisible
// sans JavaScript — c'est une exigence, pas une conséquence : une page qui
// explique un programme politique doit se lire dans un navigateur bridé, sur un
// téléphone qui a coupé les scripts, et dans un lecteur d'écran.
//
// Deux comportements, tous deux en écoute déléguée sur le document : les mots
// du glossaire sont écrits par le gabarit à des dizaines d'endroits, et poser
// un écouteur sur chacun coûterait une boucle à chaque chargement.

/** Ouvre ou ferme la définition posée sous un mot du glossaire. */
function basculer(terme) {
  const ouvert = terme.getAttribute("aria-expanded") === "true";
  const bulle = terme.nextElementSibling;
  terme.setAttribute("aria-expanded", ouvert ? "false" : "true");
  if (bulle && bulle.classList.contains("bulle")) {
    bulle.hidden = ouvert;
  }
}

/** Referme toutes les définitions, sauf celle qu'on vient d'ouvrir. */
function refermerLesAutres(sauf) {
  document.querySelectorAll('.mot > .terme[aria-expanded="true"]')
    .forEach((terme) => {
      if (terme !== sauf) {
        terme.setAttribute("aria-expanded", "false");
        const bulle = terme.nextElementSibling;
        if (bulle && bulle.classList.contains("bulle")) { bulle.hidden = true; }
      }
    });
}

document.addEventListener("click", (evenement) => {
  const terme = evenement.target.closest(".mot > .terme");
  if (terme) {
    refermerLesAutres(terme);
    basculer(terme);
    return;
  }
  // Un clic hors d'une bulle la referme : sans quoi la page se couvre de
  // définitions ouvertes que personne ne pense à fermer.
  if (!evenement.target.closest(".mot")) {
    refermerLesAutres(null);
  }
});

// Le mot du glossaire est un `<span role="button">` et non un `<button>` : il
// doit donc répondre lui-même à l'espace et à l'entrée, que le navigateur
// n'envoie qu'aux vrais boutons.
document.addEventListener("keydown", (evenement) => {
  const terme = evenement.target.closest(".mot > .terme");
  if (!terme) {
    if (evenement.key === "Escape") { refermerLesAutres(null); }
    return;
  }
  if (evenement.key === "Enter" || evenement.key === " ") {
    evenement.preventDefault();
    refermerLesAutres(terme);
    basculer(terme);
  }
});

// Le sommaire d'une page longue pointe vers des sections repliées : suivre le
// lien ne sert à rien si la section reste fermée. Le navigateur sait le faire
// seul depuis peu (`hidden=until-found`), pas partout ; quatre lignes le font
// partout.
document.addEventListener("click", (evenement) => {
  const lien = evenement.target.closest(".plan a[data-vers]");
  if (!lien) { return; }
  const cible = document.getElementById(lien.dataset.vers);
  if (!cible) { return; }
  if (cible.tagName === "DETAILS") { cible.open = true; }
  // Le focus, et pas seulement le défilement : au clavier, arriver sur une
  // section sans y poser le focus fait repartir la tabulation du haut de la
  // page au coup suivant.
  if (cible.hasAttribute("tabindex") || cible.tagName === "DETAILS") {
    cible.focus({ preventScroll: true });
  }
});
