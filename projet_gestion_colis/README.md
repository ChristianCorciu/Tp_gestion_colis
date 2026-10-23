# Gestion des livraisons — TP algorithmique

## Langage choisi
Python 3.10 ou plus récent. Python permet de présenter clairement les structures de données et les algorithmes, tout en gardant une implémentation courte et testable. Aucun paquet externe n'est nécessaire.

## Arborescence

projet/
├── src/
│   └── main.py
├── README.md
└── rapport.pdf


## Lancer le programme
Depuis la racine du projet :
bash
python src/main.py

Le programme démarre avec cinq colis d'exemple. Les poids et la capacité sont supposés être des nombres entiers de kilogrammes.

## Fonctionnalités
- Ajouter un colis avec validation et identifiant unique.
- Afficher les colis.
- Rechercher par identifiant.
- Trier par poids croissant, valeur décroissante ou priorité décroissante.
- Préparer un chargement par programmation dynamique.
- Afficher des statistiques simples.
- Mesurer à titre indicatif les temps d'ajout, de recherche et de tri sur 100, 1 000, 10 000 et 100 000 colis.

## Choix de l'optimisation
Le score d'un colis est `valeur * (priorité + 3)`. Il s'agit d'une règle métier proposée : priorité 1 multiplie la valeur par 4, priorité 5 par 8. La programmation dynamique maximise la somme de ces scores sous la contrainte de capacité. Si l'entreprise veut maximiser strictement la valeur monétaire, il faut utiliser `valeur` comme utilité et traiter la priorité comme un critère secondaire ou une contrainte séparée.

## Limite importante
Le sac à dos dynamique dépend de la capacité entière `C` : temps `O(n*C)`. Il convient lorsque la capacité exprimée en unités entières reste modérée. Pour une capacité très élevée ou des poids décimaux, une autre stratégie (algorithme approché, branchement et bornes, ou programmation dynamique sur les valeurs) peut être préférable.
