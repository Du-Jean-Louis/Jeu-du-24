import numpy as np
from colored import fg, attr
from functools import partial

def operation_elementaire(a, b, color_a, color_b):
    """ Renvoie un dictionnaire ayant pour clés le détail du calcul en couleur et pour valeur le résultat de l'opération mathématique """  
    res = {}
    
    # Ajout addition
    res[f"{fg(color_a)}{a}{attr('reset')}+{fg(color_b)}{b}"] = a+b
    
    # Ajout soustraction
    res[f"{fg(color_a)}{a}{attr('reset')}-{fg(color_b)}{b}"] = a-b
    res[f"{fg(color_b)}{b}{attr('reset')}-{fg(color_a)}{a}"] = b-a

    # Ajout multiplication
    res[f"{fg(color_a)}{a}{attr('reset')}*{fg(color_b)}{b}"] = a*b

    # Ajout division
    if b!=0:
        res[f"{fg(color_a)}{a}{attr('reset')}/{fg(color_b)}{b}"] = a/b
    
    if a!=0:
        res[f"{fg(color_b)}{b}{attr('reset')}/{fg(color_a)}{a}"] = b/a

    return res

def f4(values,goal=24,start=True, affichage=True ,colors=[],commentaires=""):
    """ Etant donné une liste de nombres, renvoie s'il est possible d'obtenir 24 en utilisant chaque nombre une unique fois. 
    Lorsque cela est possible, il print une façon de le calculer. Cette fonction fonctionne par récursion.

    Entrées :
    - list : liste de nombres
    - goal : nombre que l'on souhaite atteindre, pas forcément 24
    - start : pour réaliser l'affichage que dans le premier lancement de la fonction
    - color : pour l'affichage en couleur du calcul, pour savoir d'où provient chaque valeur (pas à renseigner, intervient seulement dans la récursion)
    - commentaire : pour garder le détail des calculs (pas à renseigner, intervient seulement dans la récursion)
    """

    # On initialise une variable globale pour imprimer les solutions lors du lancement de la fonction uniquement
    if start:
        global solutions
        solutions = []

    # Longueur de la liste
    n = len(values)

    # Lors du première appel à la fonction, on doit initialiser les couleurs et les commentaires
    
    # Assigne à chaque élément de la liste une couleur
    if not colors:
        colors = np.arange(1,n+1)

    # Rédige l'état initiale du calcul
    if not commentaires:
        commentaires = "Nombres utilisés : "
        for color, value in zip(colors, values):
            commentaires += f"{fg(color)}{value} "
    
    # Condition d'arrêt de la récursion, lorsqu'il ne reste qu'un terme. On vérifie si on a bien la valeur souhaitée.
    if n==1:
        # Problèmes certaines solutions fractionnelles, ne tombent pas sur 24 pile
        if np.abs(values[0] - goal)<0.0001:
            # On affiche le calcul permettant d'obtenir la solution et on renvoie True
            #print(commentaires)
            return True
        else :
            return False
    
    # On réalise les calculs élémentaires sur chaque paire de valeurs
    for i in range(n):
        for j in range(i+1,n):
            l = operation_elementaire(values[i],values[j],colors[i],colors[j])
            
            # On garde les valeurs qui n'ont pas été combinés par opérations élémentaires
            values_k = []
            colors_k = []
            for k in range(n):
                if k!=i and k!=j:
                    values_k.append(values[k])
                    colors_k.append(colors[k])

            # On rappelle la fonction sur les valeurs non utilisé + un des résultats obtenues par calcul élémentaire 
            for comm, r in l.items():
                new_values = values_k.copy()
                new_colors = colors_k.copy()
                new_values.append(r)
                new_colors.append(max(colors)+1)
                # On garde en mémoire le calcul réalisé pour en arriver ici
                new_comm = commentaires + "\n" + comm + f"{attr('reset')}=" + f"{fg(new_colors[-1])}{r}" + f"{attr('reset')}"
                if f4(new_values, goal, False, False, new_colors, new_comm):
                    solutions.append(new_comm)

    if start:
        if affichage : print(f"Il y a {len(solutions)} solutions possibles")
        for num,solution in enumerate(solutions):
            if affichage : print(f"Solution numéro {num+1} :\n{solution}\n_________\n")
        return len(solutions)

print("debut")

from functools import partial


def demande_entier(entree, strictement_positif=False):
    while True:
        try:
            valeur = int(input(entree))
            if strictement_positif and valeur <= 0:
                raise ValueError
            return valeur
        except ValueError:
            if strictement_positif:
                print("Il faut un nombre entier strictement positif.")
            else:
                print("Il faut entrer un entier.")

goal = demande_entier("Quel est le goal ? ")

nombre_cartes = demande_entier(
    "Combien de cartes faut-il piocher ? ",
    strictement_positif=True
)

valeurs = [
    demande_entier(f"Valeur de la carte n°{i+1} ? ")
    for i in range(nombre_cartes)
]

f4_goal = partial(f4, goal=goal)
f4_goal(valeurs)