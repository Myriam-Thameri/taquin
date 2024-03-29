from copy import deepcopy
import random
liste = [[1,0,2],[8,4,3],[7,6,5]]
goal = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]


#liste = shuffle_liste()
t = deepcopy(liste)



def etat_depart():
    return liste


def etat_final(table, goal):
    return table == goal


def case_vide(table):
    for i in range(3):
        for j in range(3):
            if table[i][j] == 0:
                return i, j


def numero(table, x, y):
    return table[x][y]


def permuter(table, c1, c2):
    aux = table[c1[0]][c1[1]]
    table[c1[0]][c1[1]] = table[c2[0]][c2[1]]
    table[c2[0]][c2[1]] = aux
    return table


def transition(table):
    moves = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    valid_moves = []
    x_vide, y_vide = case_vide(table)
    for m in moves:
        x_new, y_new = x_vide + m[0], y_vide + m[1]
        if (0 <= x_new < 3) and (0 <= y_new < len(table[0])):
            valid_moves.append([x_new, y_new])
    return valid_moves


def successor(table):
    resultat = []
    s = transition(table)
    for i in range(len(s)):
        new_table = deepcopy(table)
        x_vide, y_vide = case_vide(table)
        new_table = permuter(new_table, [x_vide, y_vide], s[i])
        resultat.append(new_table)
    return resultat

def clean(closedNodes):
    seen = []
    for node in closedNodes:
        if node not in seen:
            seen.append(node)
    return seen

def recherche_dfs_limite(t,goal,dfs=True,L=3):
    freeNodes = [deepcopy(t)]
    closedNodes = []
    goalNodes = None
    success = False
    path = []
    pas = 0
    while len(freeNodes) > 0 and not success:
        if pas%3 == 0:
            node = freeNodes.pop(0)
        else:
            node = freeNodes.pop()
        closedNodes.append(node)
        closedNodes = clean(closedNodes)
        pas += 1
        path.append(node)
        generatedStates = successor(node)
        generatedStates = [s for s in generatedStates if s not in freeNodes and s not in closedNodes]
        if (etat_final(node, goal)):
            path.append(node)
            success = True
            break
        for s in generatedStates:
            if etat_final(s, goal) == True:
                path.append(s)
                success = True
                goalNodes = s
                break
            if s not in closedNodes and s not in freeNodes:
                freeNodes.append(s)
        print(pas)
    return path, pas
def recherche_dfs(t, goal, dfs=True):
    freeNodes = [deepcopy(t)]
    closedNodes = []
    goalNodes = None
    success = False
    path = []
    pas = 0
    while len(freeNodes)>0 and not success:
        node = freeNodes.pop()
        closedNodes.append(node)
        closedNodes = clean(closedNodes)
        pas+=1
        path.append(node)
        generatedStates = successor(node)
        generatedStates = [s for s in generatedStates if s not in freeNodes and s not in closedNodes]
        if (etat_final(node,goal)):
            path.append(node)
            success = True
            break
        for s in generatedStates:
            if etat_final(s, goal) == True:
                path.append(s)
                success = True
                goalNodes = s
                break
            if s not in freeNodes and s not in closedNodes:
                freeNodes.append(s)
        print(pas)
    return path ,pas


path,pas = recherche_dfs_limite(liste,goal,True,3)
print(path)
print(pas)

