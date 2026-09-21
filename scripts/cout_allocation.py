#!/usr/bin/env python3
"""Chiffre l'allocation santé, et dit ce qu'elle coûte au mécanisme.

    python3 scripts/cout_allocation.py

Rien à installer. Les entrées sont dans ``src/sante/donnees.py``, chacune avec
sa source ; la méthode est dans ``src/sante/allocation.py``, et elle tient en
une soustraction faite dix fois. Ce script ne fait que la dérouler à voix
haute, pour que le chiffre publié sur le site puisse être refait par n'importe
qui, y compris par un contradicteur.
"""

from __future__ import annotations

import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "src"))

from sante import allocation, donnees  # noqa: E402  (après sys.path)

MILLIARD = 1e9


def euros(montant: float) -> str:
    return f"{montant / MILLIARD:>6.1f} Md€"


def courant_points(resultat) -> str:
    return (f"{resultat.a_lever / MILLIARD:.0f} Md€, soit "
            f"{resultat.points_csg:.1f} points de CSG")


def titre(texte: str) -> None:
    print(f"\n{texte}\n{'─' * len(texte)}")


def main() -> int:
    adultes = donnees.POPULATION - donnees.MINEURS
    prime = allocation.prime_pleine()

    titre("Les entrées")
    print(f"  population                {donnees.POPULATION / 1e6:>6.1f} M")
    print(f"  dont mineurs              {donnees.MINEURS / 1e6:>6.1f} M "
          "(aucune prime avant 18 ans)")
    print(f"  adultes redevables        {adultes / 1e6:>6.1f} M")
    print(f"  dépense de santé          {euros(donnees.DEPENSE_TOTALE)}")
    print(f"  niveau de vie moyen       {sum(donnees.DECILES_NIVEAU_VIE) / 10:>6.0f} €"
          "   (INSEE, moyenne des dix déciles)")
    print(f"  prime avant allocation    {prime:>6.0f} €")
    print(f"  plafond d'allocation      "
          f"{float(donnees.PARAMETRES_SIMULATEUR['plafond_prime_part_revenu']):>6.1%}"
          " du revenu")

    titre("Le coût, selon l'assiette retenue")
    for assiette in ("personne", "foyer"):
        resultat = allocation.chiffrer(assiette)
        print(f"  assiette {assiette:<9} plafond {resultat.taux_effectif:>5.2%}"
              f" → {euros(resultat.cout)}"
              f", {resultat.adultes_aides:>4.0%} des adultes aidés")
    courant = allocation.chiffrer("personne")
    print(f"\n  net des {euros(allocation.cout_actuel_couverture())} déjà "
          "consacrés à la couverture complémentaire :"
          f" {euros(courant.cout - allocation.cout_actuel_couverture())}")
    print(f"  repère : le zorgtoeslag néerlandais transposé à la France vaut "
          f"{euros(allocation.repere_neerlandais())}")

    titre("Ce que l'allocation fait au partage entre les deux étages")
    print(f"  primes dues par les adultes      {euros(adultes * prime)}"
          f"  = {courant.part_prime_due:>4.0%} de la dépense")
    print(f"  primes réellement encaissées     {euros(adultes * prime - courant.cout)}"
          f"  = {courant.part_prime_reelle:>4.0%} de la dépense")
    print(f"  reste à lever par la contribution {euros(courant.a_lever)}"
          f" = {courant.points_csg:.1f} points de CSG")
    plafond_actuel = float(
        donnees.PARAMETRES_SIMULATEUR["plafond_prime_part_revenu"])
    maximum = allocation.encaissement_maximal()
    print(f"\n  PLAFOND STRUCTUREL : à {plafond_actuel:.0%} de plafonnement, les "
          "primes ne peuvent")
    print(f"  pas rapporter plus de {euros(maximum)}, soit "
          f"{maximum / donnees.DEPENSE_TOTALE:.0%} de la dépense —")
    print("  quelle que soit leur hauteur, chaque euro ajouté au-delà étant")
    print("  repris par l'allocation. Le partage moitié-moitié voulu par la")
    print("  loi est donc " + ("ATTEIGNABLE." if maximum >= donnees.DEPENSE_TOTALE / 2
                               else "IMPOSSIBLE à ce plafond."))
    print(f"  Il exige un plafond d'au moins "
          f"{allocation.plafond_pour_partage(0.5):.1%}.")

    titre("Ce que le chiffrage a fait changer")
    print(f"  Le programme appliquait une prime de {allocation.PRIME_ABANDONNEE:.0f} €"
          f" — la moitié du coût par")
    print("  HABITANT — et un plafond de "
          f"{allocation.PLAFOND_ABANDONNE:.0%}. Les deux ont été corrigés après")
    print("  ce calcul, et non avant : c'est le chiffrage qui a décidé.\n")
    print("  prime    plafond   allocation   adultes aidés   part des primes")
    scenarios = [(allocation.PRIME_ABANDONNEE, allocation.PLAFOND_ABANDONNE)]
    scenarios += [(allocation.prime_pleine(), plafond)
                  for plafond in (0.05, 0.08, 0.10, 0.12)]
    for prime_essai, plafond in scenarios:
        cout, aides, part = allocation.cout_scenario(prime_essai, plafond)
        retenu = (abs(prime_essai - allocation.prime_pleine()) < 1
                  and abs(plafond - plafond_actuel) < 1e-9)
        ancien = prime_essai == allocation.PRIME_ABANDONNEE
        marque = "  ← retenu" if retenu else ("  ← abandonné" if ancien else "")
        print(f"  {prime_essai:>5.0f} €   {plafond:>5.0%}    {euros(cout)}"
              f"       {aides:>4.0%}            {part:>4.0%}{marque}")

    titre("Les deux paramètres que ce calcul DÉDUIT")
    print(f"  prime avant allocation     {allocation.prime_pleine():>6.0f} €")
    print("     = la part de la dépense que la loi laisse au second étage,")
    print("       rapportée aux seuls adultes qui la paient.")
    print(f"  taux de la contribution    "
          f"{allocation.taux_contribution():>6.2%}")
    print(f"     = les {courant_points(courant)} qu'il reste à lever,")
    print("       sur l'assiette de la CSG.")
    print("\n  Aucun des deux n'est écrit dans donnees.py : les deux l'ont")
    print("  été, et les deux étaient faux. Un paramètre de financement qui")
    print("  ne découle pas du financement finit par le démentir.")

    titre("Les limites de ce calcul")
    for limite in allocation.LIMITES:
        print(f"  • {limite}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
