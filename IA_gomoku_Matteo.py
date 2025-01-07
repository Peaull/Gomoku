def Actions(plateau):
    actions = set()
    n = len(plateau)
    for x in range(n):
        for y in range(n):
            if plateau[x][y] != ".":
                for dx in range(-3, 4):
                    for dy in range(-3, 4):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and plateau[nx][ny] == ".":
                            actions.add((nx, ny))
    return list(actions)


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
            score += 10000
        elif s.count(adversaire) == 5:  
            score -= 10000
        elif s.count(joueur) == 4 and s.count(".") == 1:
            score += 5000
        elif s.count(adversaire) == 4 and s.count(".") == 1: 
            score -= 5000
        elif s.count(joueur) == 3 and s.count(".") == 2:  
            score += 100
        elif s.count(adversaire) == 3 and s.count(".") == 2:  
            score -= 100
        elif s.count(joueur) == 2 and s.count(".") == 3: 
            score += 10
        elif s.count(adversaire) == 2 and s.count(".") == 3: 
            score -= 10
        elif s.count(joueur) == 1 and s.count(".") == 4:  
            score += 1
        elif s.count(adversaire) == 1 and s.count(".") == 4:
            score -= 1

    return score

def Coups_Critiques(plateau, joueur):
    # Modèles pour les coups critiques
    coups_critiques = {
        "N": [("NNNN.",1), (".NNNN",1), ("NN.NN",1), ("N.NNN",1), ("NNN.N",1), (".NNN.",2), ("NN.N.",2), (".N.NN",2)],
        "B": [(".BBB.",2), ("BBBB.",1), (".BBBB",1), ("BB.BB",1), ("B.BBB",1), ("BBB.B",1), ("BB.B.",2), (".B.BB",2)]
    }
    
    adversaire = "B" if joueur == "N" else "N"
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  
    
    coups_crit_att = [None,None]
    coups_crit_def = [None,None]

    for x in range(15):
        for y in range(15):
            for dx, dy in directions:
                temp = "" 
                temp_coup = [] 
                for i in range(5):
                    nx, ny = x + i * dx, y + i * dy
                    if 0 <= nx < 15 and 0 <= ny < 15:
                        symbole = plateau[nx][ny]
                        temp += symbole
                        if symbole == '.':
                            temp_coup.append((nx, ny))
                
                for i in coups_critiques[joueur]:
                    if temp == i[0]:
                        if i[1] == 1:
                            coups_crit_att[0] = temp_coup
                        else:
                            coups_crit_att[1] = temp_coup
                
                for i in coups_critiques[adversaire]:
                    if temp == i[0]:
                        if i[1] == 1:
                            coups_crit_def[0] = temp_coup
                        else:
                            coups_crit_def[1] = temp_coup
                
    
    if coups_crit_att[0] != None:
        return list(coups_crit_att[0])
    
    if coups_crit_def[0] != None:
        return list(coups_crit_def[0])
    
    if coups_crit_att[1] != None:
        return list(coups_crit_att[1])
    
    if coups_crit_def[1] != None:
        return list(coups_crit_def[1])
    return None


def AlphaBeta(plateau, joueur):
    import time
    debut = time.time()
    temps_limite = 5

    coups_critiques = Coups_Critiques(plateau, joueur)
    if coups_critiques != None:  
        return coups_critiques[0]  

    def Max_Value(plateau, alpha, beta):
        if Terminal_Test(plateau):
            return Utility(plateau, joueur), None

        if time.time() - debut > temps_limite:
            return Utility(plateau, joueur), None

        v = float("-inf")
        meilleure_action = None
        actions = Actions(plateau)
        actions.sort(key=lambda a: Utility(Result(plateau, a, joueur), joueur), reverse=True)

        for action in actions:
            if time.time() - debut > temps_limite:
                break
            score, _ = Min_Value(Result(plateau, action, joueur), alpha, beta)
            if score > v:
                v = score
                meilleure_action = action
            if v >= beta:
                return v, meilleure_action
            alpha = max(alpha, v)

        return v, meilleure_action

    def Min_Value(plateau, alpha, beta):
        if Terminal_Test(plateau):
            return Utility(plateau, joueur), None

        if time.time() - debut > temps_limite:
            return Utility(plateau, joueur), None

        v = float("inf")
        meilleure_action = None
        actions = Actions(plateau)
        actions.sort(key=lambda a: Utility(Result(plateau, a, "N" if joueur == "B" else "B"), joueur), reverse=True)

        for action in actions:
            if time.time() - debut > temps_limite:
                break
            score, _ = Max_Value(Result(plateau, action, "N" if joueur == "B" else "B"), alpha, beta)
            if score < v:
                v = score
                meilleure_action = action
            if v <= alpha:
                return v, meilleure_action
            beta = min(beta, v)

        return v, meilleure_action

    _, meilleure_action = Max_Value(plateau, float("-inf"), float("inf"))
    
    return meilleure_action


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


def coup_ia(plateau, joueur, tour_actuel):
    
    res = AlphaBeta(plateau, joueur)
    x, y = res
    return x, y


def jouerr():
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

jouerr()