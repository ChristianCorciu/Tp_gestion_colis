from dataclasses import dataclass
from time import perf_counter
from random import Random


@dataclass(frozen=True)
class Colis:
    identifiant: int
    poids: int
    valeur: int
    priorite: int
    destination: str

    def __post_init__(self):
        if self.identifiant < 0:
            raise ValueError("L'identifiant doit être positif ou nul.")
        if self.poids <= 0:
            raise ValueError("Le poids doit être strictement positif.")
        if self.valeur < 0:
            raise ValueError("La valeur doit être positive ou nulle.")
        if not 1 <= self.priorite <= 5:
            raise ValueError("La priorité doit être comprise entre 1 et 5.")
        if not self.destination.strip():
            raise ValueError("La destination ne peut pas être vide.")


class GestionColis:
    def __init__(self):
        # Accès direct par identifiant : O(1) en moyenne.
        self.colis = {}

    def ajouter(self, colis):
        if colis.identifiant in self.colis:
            raise ValueError(f"L'identifiant {colis.identifiant} existe déjà.")
        self.colis[colis.identifiant] = colis

    def rechercher(self, identifiant):
        return self.colis.get(identifiant)

    def afficher(self):
        return sorted(self.colis.values(), key=lambda c: c.identifiant)

    def trier(self, critere):
        cles = {
            "poids": lambda c: (c.poids, c.identifiant),
            "valeur": lambda c: (-c.valeur, c.identifiant),
            "priorite": lambda c: (-c.priorite, c.identifiant),
        }
        if critere not in cles:
            raise ValueError("Critère inconnu.")
        return sorted(self.colis.values(), key=cles[critere])

    def statistiques(self):
        liste = list(self.colis.values())
        if not liste:
            return {"nombre": 0, "poids_total": 0, "valeur_totale": 0}
        return {
            "nombre": len(liste),
            "poids_total": sum(c.poids for c in liste),
            "valeur_totale": sum(c.valeur for c in liste),
        }


def score_colis(colis):
    """
    Score d'utilité = valeur * (priorité + 3).
    Priorité 1 : multiplicateur 4 ; priorité 5 : multiplicateur 8.
    Cette règle explicite donne davantage de poids aux colis prioritaires.
    Elle optimise un score pondéré, pas nécessairement la valeur monétaire brute.
    """
    return colis.valeur * (colis.priorite + 3)


def preparer_camion(colis, capacite):
    if capacite < 0:
        raise ValueError("La capacité doit être positive ou nulle.")
    colis = list(colis)
    n = len(colis)
   
    dp = [0] * (capacite + 1)
   
    decisions = [bytearray(capacite + 1) for _ in range(n)]

    for i, c in enumerate(colis):
        w = c.poids
        utilite = score_colis(c)
        if w > capacite:
            continue
       
        for cap in range(capacite, w - 1, -1):
            candidat = dp[cap - w] + utilite
            if candidat > dp[cap]:
                dp[cap] = candidat
                decisions[i][cap] = 1

    
    retenus = []
    cap = capacite
    for i in range(n - 1, -1, -1):
        if decisions[i][cap]:
            retenus.append(colis[i])
            cap -= colis[i].poids
    retenus.reverse()

    return {
        "colis": retenus,
        "poids_total": sum(c.poids for c in retenus),
        "valeur_totale": sum(c.valeur for c in retenus),
        "score_total": sum(score_colis(c) for c in retenus),
        "capacite": capacite,
    }


def afficher_colis(colis):
    if not colis:
        print("Aucun colis.")
        return
    print(f"{'ID':>6} {'Poids':>7} {'Valeur':>8} {'Priorité':>9} Destination")
    for c in colis:
        print(f"{c.identifiant:>6} {c.poids:>7} {c.valeur:>8} "
              f"{c.priorite:>9} {c.destination}")


def charger_exemple(gestion):
    exemples = [
        Colis(101, 8, 20, 2, "Paris"),
        Colis(102, 3, 10, 5, "Lille"),
        Colis(103, 12, 40, 1, "Lyon"),
        Colis(104, 5, 25, 4, "Paris"),
        Colis(105, 2, 15, 3, "Lille"),
    ]
    for c in exemples:
        gestion.ajouter(c)


def benchmark():
    print("\nMesure indicative (temps dépendant de la machine) :")
    rng = Random(42)
    for n in (100, 1_000, 10_000, 100_000):
        g = GestionColis()
        donnees = [
            Colis(i, rng.randint(1, 30), rng.randint(1, 500),
                  rng.randint(1, 5), f"Ville-{rng.randint(1, 30)}")
            for i in range(n)
        ]
        debut = perf_counter()
        for c in donnees:
            g.ajouter(c)
        ajout = perf_counter() - debut
        debut = perf_counter()
        g.trier("valeur")
        tri = perf_counter() - debut
        debut = perf_counter()
        g.rechercher(n // 2)
        recherche = perf_counter() - debut
        print(f"n={n:>6}: ajout={ajout:.6f}s, tri={tri:.6f}s, "
              f"recherche={recherche:.8f}s")


def menu():
    gestion = GestionColis()
    charger_exemple(gestion)

    while True:
        print("\n===== GESTION DES LIVRAISONS =====")
        print("1. Afficher les colis")
        print("2. Ajouter un colis")
        print("3. Rechercher un colis")
        print("4. Organiser les colis")
        print("5. Préparer un camion")
        print("6. Afficher les statistiques")
        print("7. Lancer les tests de performance")
        print("0. Quitter")
        choix = input("Choix : ").strip()

        try:
            if choix == "1":
                afficher_colis(gestion.afficher())
            elif choix == "2":
                c = Colis(
                    int(input("Identifiant : ")),
                    int(input("Poids entier (kg) : ")),
                    int(input("Valeur : ")),
                    int(input("Priorité (1 à 5) : ")),
                    input("Destination : ").strip(),
                )
                gestion.ajouter(c)
                print("Colis ajouté.")
            elif choix == "3":
                identifiant = int(input("Identifiant recherché : "))
                c = gestion.rechercher(identifiant)
                afficher_colis([c] if c else [])
            elif choix == "4":
                print("1. Poids croissant  2. Valeur décroissante  3. Priorité décroissante")
                sous_choix = input("Critère : ").strip()
                critere = {"1": "poids", "2": "valeur", "3": "priorite"}.get(sous_choix)
                if critere:
                    afficher_colis(gestion.trier(critere))
                else:
                    print("Critère invalide.")
            elif choix == "5":
                capacite = int(input("Capacité du camion (kg entiers) : "))
                resultat = preparer_camion(gestion.colis.values(), capacite)
                print("\nColis sélectionnés :")
                afficher_colis(resultat["colis"])
                print(f"Poids total : {resultat['poids_total']} / {capacite} kg")
                print(f"Valeur brute totale : {resultat['valeur_totale']}")
                print(f"Score pondéré total : {resultat['score_total']}")
            elif choix == "6":
                stats = gestion.statistiques()
                print(f"Nombre de colis : {stats['nombre']}")
                print(f"Somme des poids : {stats['poids_total']} kg")
                print(f"Somme des valeurs : {stats['valeur_totale']}")
            elif choix == "7":
                benchmark()
            elif choix == "0":
                print("Au revoir.")
                break
            else:
                print("Choix invalide.")
        except (ValueError, OverflowError) as exc:
            print(f"Erreur : {exc}")


if __name__ == "__main__":
    menu()
