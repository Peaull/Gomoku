from gomoku import *

def creer_plateau():
    plateau = [["." for _ in range(15)] for _ in range(15)]
    plateau[7][7] = "N"
    return plateau


def afficher_plateau(plateau):
    print("  " + " ".join(map(str, range(15))))
    for i in range(15):
        print(chr(65 + i) + " " + " ".join(plateau[i]))
        
def verifier_victoire(plateau, joueur):
    for x in range(15):
        for y in range(15):
            if plateau[x][y] != joueur:
                continue
            directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
            for dx, dy in directions:
                alignes = 0
                for i in range(5):
                    nx, ny = x + i * dx, y + i * dy
                    if 0 <= nx < 15 and 0 <= ny < 15 and plateau[nx][ny] == joueur:
                        alignes += 1
                    else:
                        break
                if alignes == 5:
                    return True
    return False


def est_valide(plateau, x, y, joueur, restriction):
    if plateau[x][y] != ".":
        return False
    if joueur == "N" and restriction:
        if 3 <= x <= 11 and 3 <= y <= 11:
            return False
    if x > 14 or y > 14:
        return False
    return True


def jouer_coup(plateau, x, y, joueur):
    plateau[x][y] = joueur
    
def jouer():
    plateau = creer_plateau()
    afficher_plateau(plateau)

    print("Voulez-vous jouer les noirs (1er) ou les blancs (2eme) ? (N/B)")
    joueur_humain = input().strip().upper()

    joueur_actuel = "B"
    restriction = False
    pions_restants = {"N": 59, "B": 60}

    premier_tour = True
    tour_actuel = 0
    
    while True:
        if pions_restants["N"] == 0 and pions_restants["B"] == 0:
            print("Match nul.")
            break

        if joueur_actuel == joueur_humain:
            coup = input("Entrez votre coup (ex: H7) : ").strip().upper()
            x, y = ord(coup[0]) - 65, int(coup[1:])
        else:
            if restriction:
                if plateau[2][7] != "B" and plateau[6][7] != "B":
                    x = 2 
                    y = 7
                else :
                    x =12
                    y = 7
            else :
                temp = coup_ia(plateau, joueur_actuel, tour_actuel)
                x= temp[0]
                y= temp[1]

            print(f"L'IA joue : {chr(65 + x)}{y}")

        if not (0 <= x < 15 and 0 <= y < 15):
            print("Coup invalide. Réessayez.")
            continue

        if not est_valide(plateau, x, y, joueur_actuel, restriction):
            print("Coup invalide. Réessayez.")
            continue

        jouer_coup(plateau, x, y, joueur_actuel)
        afficher_plateau(plateau)
        pions_restants[joueur_actuel] -= 1

        if tour_actuel > 6:
            if verifier_victoire(plateau, joueur_actuel):
                print(f"Le joueur {joueur_actuel} a gagné !")
                break

        if premier_tour:
            if joueur_actuel == "B":
                restriction = True
            premier_tour = False

        joueur_actuel = "B" if joueur_actuel == "N" else "N"
        restriction = joueur_actuel == "N" and restriction
        tour_actuel += 1

def jouer2IA():
    plateau = creer_plateau()
    afficher_plateau(plateau)

    IA1 = "B"
    
    joueur_actuel = "B"
    restriction = False
    pions_restants = {"N": 59, "B": 60}

    premier_tour = True
    tour_actuel = 0
    
    while True:
        if pions_restants["N"] == 0 and pions_restants["B"] == 0:
            print("Match nul.")
            break

        if joueur_actuel == IA1:
            if restriction:
                if plateau[2][7] != "B" and plateau[6][7] != "B":
                    x = 2 
                    y = 7
                else :
                    x =12
                    y = 7
            else:
                temp = coup_ia(plateau, joueur_actuel, tour_actuel)
                x= temp[0]
                y= temp[1]
            print(f"L'IA 1 joue : {chr(65 + x)}{y}")
        else:
            if restriction:
                if plateau[2][7] != "B" and plateau[6][7] != "B":
                    x = 2 
                    y = 7
                else :
                    x =12
                    y = 7
            else :
                temp = coup_ia(plateau, joueur_actuel, tour_actuel)
                x= temp[0]
                y= temp[1]

            print(f"L'IA 2 joue : {chr(65 + x)}{y}")

        if not (0 <= x < 15 and 0 <= y < 15):
            print("Coup invalide. Réessayez.")
            continue

        if not est_valide(plateau, x, y, joueur_actuel, restriction):
            print("Coup invalide. Réessayez.")
            continue

        jouer_coup(plateau, x, y, joueur_actuel)
        afficher_plateau(plateau)
        pions_restants[joueur_actuel] -= 1

        if tour_actuel > 6:
            if verifier_victoire(plateau, joueur_actuel):
                print(f"Le joueur {joueur_actuel} a gagné !")
                break

        if premier_tour:
            if joueur_actuel == "B":
                restriction = True
            premier_tour = False

        joueur_actuel = "B" if joueur_actuel == "N" else "N"
        restriction = joueur_actuel == "N" and restriction
        tour_actuel += 1


jouer2IA()