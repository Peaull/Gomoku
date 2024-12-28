def Actions(plateau):
    actions =  []
    for x in range(len(plateau)):
        for y in range(len(plateau)):
            if plateau[x][y] == ".":
                actions.append((x, y))
    return actions

def Result(plateau, action, joueur):
    nouveau_plateau = [ligne[:] for ligne in plateau]
    i, j = action
    nouveau_plateau[i][j] = joueur
    return nouveau_plateau


def Terminal_Test(plateau):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for x in range(len(plateau)):
        for y in range(len(plateau[0])):
            if plateau[x][y] == ".":
                continue
            joueur = plateau[x][y]
            for dx, dy in directions:
                alignes = 0
                for i in range(5):
                    nx, ny = x + i * dx, y + i * dy
                    if 0 <= nx < len(plateau) and 0 <= ny < len(plateau[0]) and plateau[nx][ny] == joueur:
                        alignes += 1
                        if alignes == 5:
                            return True
                    else:
                        break
    return False


def Utility(plateau, joueur):
    adversaire = "N" if joueur == "B" else "B"
    val = 0

    for ligne in plateau:
        val += eval_ligne(ligne, joueur, adversaire)

    for col in range(len(plateau)):
        val += eval_ligne([plateau[ligne][col] for ligne in range(len(plateau))], joueur, adversaire)

    val += eval_ligne([plateau[i][i] for i in range(len(plateau))], joueur, adversaire)
    val += eval_ligne([plateau[i][len(plateau) - 1 - i] for i in range(len(plateau))], joueur, adversaire)

    return val


def eval_ligne(ligne, joueur, adversaire):
    score = 0
    longueur = len(ligne)

    for i in range(longueur - 4):  
        s = ligne[i:i + 5]

        if s.count(joueur) == 5: 
            score += 1000
        elif s.count(adversaire) == 5:  
            score -= 1000
        elif s.count(joueur) == 4 and s.count(".") == 1:  
            score += 500
        elif s.count(adversaire) == 4 and s.count(".") == 1:  
            score -= 500
        elif s.count(joueur) == 3 and s.count(".") == 2:  
            score += 50
        elif s.count(adversaire) == 3 and s.count(".") == 2:  
            score -= 50
        elif s.count(joueur) == 2 and s.count(".") == 3:  
            score += 10
        elif s.count(adversaire) == 2 and s.count(".") == 3: 
            score -= 10
        elif s.count(joueur) == 1 and s.count(".") == 4:  
            score += 1
        elif s.count(adversaire) == 1 and s.count(".") == 4:
            score -= 1

    return score



def AlphaBeta(plateau, joueur, limite):

    def Max_Value(plateau, alpha, beta, limite):

        if Terminal_Test(plateau) or limite == 0:
            val = Utility(plateau, joueur)
            return val, None

        v = float("-inf")
        meilleure_action = None
        for action in Actions(plateau):
            score, _ = Min_Value(Result(plateau, action, joueur), alpha, beta, limite - 1)
            if score > v:
                v = score
                meilleure_action = action
            if v >= beta:
                return v, meilleure_action
            alpha = max(alpha, v)

        return v, meilleure_action

    def Min_Value(plateau, alpha, beta, limite):

        if Terminal_Test(plateau) or limite == 0:
            val = Utility(plateau, joueur)
            return val, None

        v = float("inf")
        meilleure_action = None
        for action in Actions(plateau):
            score, _ = Max_Value(Result(plateau, action, "N" if joueur == "B" else "B"), alpha, beta, limite - 1)
            if score < v:
                v = score
                meilleure_action = action
            if v <= alpha:
                return v, meilleure_action
            beta = min(beta, v)

        return v, meilleure_action

    _, meilleure_action = Max_Value(plateau, float("-inf"), float("inf"), limite)
    return meilleure_action


# def creer_plateau():
#     plateau = [["." for _ in range(15)] for _ in range(15)]
#     plateau[7][7] = "N"
#     return plateau


# def afficher_plateau(plateau):
#     print("  " + " ".join(map(str, range(15))))
#     for i in range(15):
#         print(chr(65 + i) + " " + " ".join(plateau[i]))


# def verifier_victoire(plateau, joueur):
#     for x in range(15):
#         for y in range(15):
#             if plateau[x][y] != joueur:
#                 continue
#             directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
#             for dx, dy in directions:
#                 alignes = 0
#                 for i in range(5):
#                     nx, ny = x + i * dx, y + i * dy
#                     if 0 <= nx < 15 and 0 <= ny < 15 and plateau[nx][ny] == joueur:
#                         alignes += 1
#                     else:
#                         break
#                 if alignes == 5:
#                     return True
#     return False


# def est_valide(plateau, x, y, joueur, restriction):
#     if plateau[x][y] != ".":
#         return False
#     if joueur == "N" and restriction:
#         if 3 <= x <= 11 and 3 <= y <= 11:
#             return False
#     if x > 14 or y > 14:
#         return False
#     return True


# def jouer_coup(plateau, x, y, joueur):
#     plateau[x][y] = joueur


def coup_ia(plateau, joueur, tour_actuel):
    x=0
    y=0
    taille_sous_plateau = 3 if tour_actuel < 8 else \
              5 if tour_actuel < 16 else \
              7 if tour_actuel < 20 else \
              10 if tour_actuel < 30 else 15

    if taille_sous_plateau == 15:
        res = AlphaBeta(plateau, joueur)
        x=res[0]
        y=res[1]
    else:
        sous_plateau_centre = sous_plateau(plateau, taille_sous_plateau)
        if tour_actuel < 7:
            res =AlphaBeta(sous_plateau_centre, joueur, 3)
        else:
            res = AlphaBeta(sous_plateau_centre, joueur,2)
        x = res[0] + max(0, 7 - taille_sous_plateau)
        y = res[1] + max(0, 7 - taille_sous_plateau)
    return (x,y)


def sous_plateau(plateau, taille):
    centre_x=7
    centre_y=7
    min_x = max(0, centre_x - taille)
    max_x = min(len(plateau) - 1, centre_x + taille)
    min_y = max(0, centre_y - taille)
    max_y = min(len(plateau[0]) - 1, centre_y + taille)

    sous_plateau = [ligne[min_y:max_y + 1] for ligne in plateau[min_x:max_x + 1]]
    return sous_plateau


# def jouer():
#     plateau = creer_plateau()
#     afficher_plateau(plateau)

#     print("Voulez-vous jouer les noirs (1er) ou les blancs (2eme) ? (N/B)")
#     joueur_humain = input().strip().upper()

#     joueur_actuel = "B"
#     restriction = False
#     pions_restants = {"N": 59, "B": 60}

#     premier_tour = True
#     tour_actuel = 0
    
#     while True:
#         if pions_restants["N"] == 0 and pions_restants["B"] == 0:
#             print("Match nul.")
#             break

#         if joueur_actuel == joueur_humain:
#             coup = input("Entrez votre coup (ex: H7) : ").strip().upper()
#             x, y = ord(coup[0]) - 65, int(coup[1:])
#         else:
#             if restriction:
#                 if plateau[2][7] != "B" and plateau[6][7] != "B":
#                     x = 2 
#                     y = 7
#                 else :
#                     x =12
#                     y = 7
#             else :
#                 temp = coup_ia(plateau, joueur_actuel, tour_actuel)
#                 x= temp[0]
#                 y= temp[1]

#             print(f"L'IA joue : {chr(65 + x)}{y}")

#         if not (0 <= x < 15 and 0 <= y < 15):
#             print("Coup invalide. Réessayez.")
#             continue

#         if not est_valide(plateau, x, y, joueur_actuel, restriction):
#             print("Coup invalide. Réessayez.")
#             continue

#         jouer_coup(plateau, x, y, joueur_actuel)
#         afficher_plateau(plateau)
#         pions_restants[joueur_actuel] -= 1

#         if tour_actuel > 6:
#             if verifier_victoire(plateau, joueur_actuel):
#                 print(f"Le joueur {joueur_actuel} a gagné !")
#                 break

#         if premier_tour:
#             if joueur_actuel == "B":
#                 restriction = True
#             premier_tour = False

#         joueur_actuel = "B" if joueur_actuel == "N" else "N"
#         restriction = joueur_actuel == "N" and restriction
#         tour_actuel += 1


# jouer()
