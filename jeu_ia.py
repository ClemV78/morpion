import numpy as np


def gagne(plateau):
    # Colonne
    somme = np.sum(plateau, axis=0)
    for a in somme:
        if a == 0:
            return(True, 0)
        if a == 3:
            return(True, 1)
    # Ligne
    somme = np.sum(plateau, axis=1)
    for a in somme:
        if a == 0:
            return(True, 0)
        if a == 3:
            return(True, 1)
    # Diag
    somme = [0, 0]
    somme[0] = plateau[0, 0]+plateau[1, 1]+plateau[2, 2]
    somme[1] = plateau[0, 2]+plateau[1, 1]+plateau[2, 0]
    for a in somme:
        if a == 0:
            return(True, 0)
        if a == 3:
            return(True, 1)
    return(False, -3)


def libre(plateau):
    l = []
    for i in range(3):
        for j in range(3):
            if plateau[i, j] == -3:
                l.append([i, j])
    return(l)


def minimax(plateau, joueur, profondeur=1):

    def dedans(case):
        i, j = case
        if 0 <= i < 3 and 0 <= j < 3:
            return(True)
        return(False)

    directions = np.array(
        [[0, 1], [1, 0], [0, -1], [-1, 0], [-1, -1], [-1, 1], [1, 1], [1, -1]])

    def nb_cases_jointes(case, direct, joueur_case):
        if list(direct) == [0, 0]:
            l_score = []
            for direct in directions:
                if dedans(case+direct):
                    l_score.append(nb_cases_jointes(
                        case+direct, direct, joueur_case))
            m = max(l_score, key=lambda x: x[0])[0]
            if m == 2:
                return(5)
            compteur = 0
            for sc, direct in l_score:
                if sc == m:
                    compteur += 1
            return(compteur*m)
        else:
            i, j = case
            if plateau[i, j] != joueur_case:
                return(0, np.zeros(2))
            if dedans(case+direct):
                sc, direct = nb_cases_jointes(case+direct, direct, joueur_case)
                return(1+sc, direct)
            return(1, direct)

    def score2(case):
        i, j = case
        sc = nb_cases_jointes(case, np.zeros(2), plateau[i, j])
        if sc == 0:
            return(0)
        return(sc*2)

    def score(joueur):
        if plateau[0, 0] == joueur and plateau[1, 0] == joueur and plateau[2, 0] == joueur:
            return(12)
        if plateau[0, 0] == joueur and plateau[1, 1] == joueur and plateau[2, 2] == joueur:
            return(12)
        if plateau[0, 0] == joueur and plateau[0, 1] == joueur and plateau[0, 2] == joueur:
            return(12)
        if plateau[1, 0] == joueur and plateau[1, 1] == joueur and plateau[1, 2] == joueur:
            return(12)
        if plateau[2, 0] == joueur and plateau[2, 1] == joueur and plateau[2, 2] == joueur:
            return(12)
        if plateau[0, 1] == joueur and plateau[1, 1] == joueur and plateau[2, 1] == joueur:
            return(12)
        if plateau[0, 2] == joueur and plateau[1, 2] == joueur and plateau[2, 2] == joueur:
            return(12)
        if plateau[2, 0] == joueur and plateau[1, 1] == joueur and plateau[0, 2] == joueur:
            return(12)

        compteur = 0
        if plateau[0, 0] == joueur and plateau[1, 0] == joueur:
            compteur += 2
        if plateau[0, 0] == joueur and plateau[0, 1] == joueur:
            compteur += 2
        if plateau[0, 0] == joueur and plateau[1, 1] == joueur:
            compteur += 2
        if plateau[0, 1] == joueur and plateau[0, 2] == joueur:
            compteur += 2
        if plateau[0, 1] == joueur and plateau[1, 1] == joueur:
            compteur += 2
        if plateau[0, 2] == joueur and plateau[1, 2] == joueur:
            compteur += 2
        if plateau[1, 0] == joueur and plateau[2, 0] == joueur:
            compteur += 2
        if plateau[1, 0] == joueur and plateau[1, 1] == joueur:
            compteur += 2
        if plateau[1, 1] == joueur and plateau[1, 2] == joueur:
            compteur += 2
        if plateau[1, 1] == joueur and plateau[2, 1] == joueur:
            compteur += 2
        if plateau[1, 2] == joueur and plateau[2, 2] == joueur:
            compteur += 2
        return(compteur)

    if profondeur == 1:
        lib = libre(plateau)
        if lib == []:
            return(0, [-1, -1])
        score_max = -1
        for i, j in libre(plateau):
            plateau[i, j] = joueur
            sc = score(joueur)
            plateau[i, j] = -3
            if score_max == -1:
                score_max = sc
                case_max = [i, j]
            elif sc > score_max:
                score_max, case_max = sc, [i, j]
        return(score_max, case_max)
    else:
        score_max, case_max = 0, [0, 0]
        l_score = []
        lib = libre(plateau)
        if lib == []:
            return(0, [-1, -1])

        for i, j in lib:
            plateau[i, j] = joueur
            if score(joueur) == 12:  # si on peut gagner, on gagne
                plateau[i, j] = -3
                return([12, [i, j]])
            l_score.append(
                [minimax(plateau, 1-joueur, profondeur-1)[0], [i, j]])
            plateau[i, j] = -3
        mini = min(l_score, key=lambda x: x[0])[0]
        if mini == 12:  # si on ne peut que perdre, on perd
            return([0, [i, j]])
        l_mini = []
        for sc, cs in l_score:
            if sc == mini:
                l_mini.append(cs)
        l_score = []
        for cs in l_mini:
            i, j = cs
            plateau[i, j] = joueur
            l_score.append([score(joueur), cs])
            plateau[i, j] = -3
        return(max(l_score, key=lambda x: x[0]))


def main():
    bol, j = gagne(plateau)
    joueur = 0
    while not bol:
        if libre() == []:
            break
        sc, [i_mm, j_mm] = minimax(plateau, joueur, 1)
        print(plateau)
        print('Le minimax propose de jouer : '+str(i_mm)+str(j_mm))
        i, j = input("Veuiller entrer la case à remplir :")
        i, j = int(i), int(j)
        if plateau[i, j] == -3:
            plateau[i, j] = joueur
            joueur = 1-joueur
            bol, j = gagne(plateau)
        else:
            print("")
            print("Case déjà prise")
        print("")
    if libre() == []:
        print('Egalité')
    else:
        print(plateau)
        print('Bravo ', j)


if __name__ == '__main__':
    plateau = np.array([[-3 for _ in range(3)] for _ in range(3)])
    plateau[0, 0] = 0
    plateau[0, 1] = 0
    plateau[1, 1] = 1
    plateau[0, 2] = 1
    # plateau[2, 1] = 1
    # plateau[1, 2] = 1
    # plateau[1, 0] = 0
    plateau[2, 0] = 0
    print(minimax(plateau, 1, 4))
    main()
