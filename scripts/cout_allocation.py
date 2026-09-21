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
    print(f"\n  PLAFOND STRUCTUREL : à ce taux de plafonnement, les primes ne")
    print(f"  peuvent pas rapporter plus de {euros(allocation.encaissement_maximal())}"
          f", soit {allocation.encaissement_maximal() / donnees.DEPENSE_TOTALE:.0%} de la")
    print("  dépense — quelle que soit leur hauteur, chaque euro ajouté")
    print("  au-delà étant repris par l'allocation. Le partage moitié-moitié")
    print("  n'est pas mal calibré à ce plafond : il est impossible.")

    titre("Ce qu'il faudrait pour que les primes en portent la moitié")
    juste = allocation.prime_pour_partage(0.5)
    print(f"  prime calée sur les ADULTES et non sur les habitants : {juste:.0f} €")
    print(f"  plafond minimal pour que ce soit atteignable : "
          f"{allocation.plafond_pour_partage(0.5):.1%}\n")
    print("  plafond   allocation   adultes aidés   part des primes")
    for plafond in (0.05, 0.08, 0.10, 0.12):
        cout, aides, part = allocation.cout_scenario(juste, plafond)
        marque = " ←" if abs(plafond - allocation.PLAFOND_RECALIBRE) < 1e-9 else ""
        print(f"   {plafond:>5.0%}    {euros(cout)}       {aides:>4.0%}"
              f"            {part:>4.0%}{marque}")

    titre("Les limites de ce calcul")
    for limite in allocation.LIMITES:
        print(f"  • {limite}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
