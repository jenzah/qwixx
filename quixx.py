
from sys import exit
from time import sleep
from itertools import product
from colorama import Fore, Style
from random import randint,choice
import json
import os

points = {
    0: 0,
    1: 1,
    2: 3,
    3: 6,
    4: 10,
    5: 15,
    6: 21,
    7: 28,
    8: 36,
    9: 45,
    10: 55,
    11: 66,
    12: 75
}


## save/load game
def save_game(data_to_save, save_file):
    """
    Saves game to a json file
    """

    with open(os.path.join(SAVE_DIR, save_file), "w") as f:
        json.dump(data_to_save, f)


def load_game(save_file):
    """
    List --> List
    Loads game from json file
    """

    with open(os.path.join(SAVE_DIR, save_file)) as f:
        data_to_save = json.load(f)
    return data_to_save


def choose_save_file():
    """
    None --> Str
    Ask player to choose which file to save in
    """

    sleep(1)
    print("Entrez un nombre pour choisir un fichier pour sauvegarder le jeu : ")

    existing_saves = os.listdir(SAVE_DIR)
    save_files = existing_saves

    nb_saves = len(save_files)
    while nb_saves < 3:
        save_files.append(preset_save_files[nb_saves])
        nb_saves += 1

    for index, file in enumerate(save_files):
        print(f"{index + 1}. {file}")

    save_as = input("> ")

    if save_as.isdigit() and 1 <= int(save_as) <= 3:
        index = int(save_as) - 1
        return save_files[index]

    else:
        print("[ERREUR] Commande invalide. \n")
        return choose_save_file()


def choose_load_file():
    """
    None --> Str
    Ask player which file to load
    """

    print("Entrez un nombre pour choisir un fichier à ouvrir (1-3) :")
    for index, file in enumerate(os.listdir(SAVE_DIR)):
        print(f"{index + 1}. {file}")
    loaded_file = input("> ")

    if loaded_file.isdigit() and 1 <= int(loaded_file) <= 3:
        try:
            index = int(loaded_file) - 1
            filename = os.listdir(SAVE_DIR)[index]
            return filename
        except (IndexError):
            return None

    else:
        print("[ERREUR] Commande invalide. Réessayez. \n")
        return choose_load_file()


def ask_to_load():
    global data_to_save
    global current_dir
    global game_mode

    current_dir = os.getcwd()

    while True:
        game_mode = 0
        load = input("Voulez-vous continuer votre jeu précédent (o/n) ? ")

        if load.lower() == "o" or load.lower() == "n":
            break

        print("[ERREUR : Commande invalide] \n")
        sleep(1)

    if load.lower() == "n":
        loaded_game = False
        print("Vous commencez une nouvelle partie. \n")

    # if player asks to reload game, if there is a saved game it loads it
    # otherwise it starts a new game
    elif load.lower() == "o":
        save_file = choose_load_file()

        try:
            data_to_save = load_game(save_file)
            loaded_game = True
            game_mode = "0"
            print("Jeu précédent chargé avec succès.")
            print("\n[Mode local avec joueurs]")
        except:
            loaded_game = False
            print("[ERREUR : Aucun jeu précédent trouvé] \nVous commencez une nouvelle partie. \n")

    return loaded_game


def saved_game_orders():
    """
    None --> List x List
    retourne la liste
    """
    joueurs, fiches = zip(*data_to_save)

    liste_joueurs = list(joueurs)
    fiche_joueurs = list(fiches)

    return liste_joueurs, fiche_joueurs
##


# To get the name of the players
def get_noms_joueurs():
    """
    None --> Str
    Fonction retournant le nom (str) d'un joueur.
    """

    joueur_nom = None

    while not joueur_nom:
        joueur_nom = input(f"Entrez le nom du joueur {i + 1}: ")

        if joueur_nom in LISTE_JOUEUR:
            print("Ce nom a déjà été pris. Réessayez.")
            joueur_nom = None

    return joueur_nom


def check_user_input(input):
    """
    Str --> Bool
    Fonction retournant True si input est un nombre, False sinon.
    """

    try:
        # Convert it into integer
        int(input)
        return True

    except ValueError:
        try:
            # Convert it into float
            float(input)
            return True

        except ValueError:
            return False


# To get the number of player and their names (game of 2 to 5 players)
def add_player():
    """
    None --> List
    Fonction retournant la liste des joueurs.
    """

    global LISTE_JOUEUR
    global i

    LISTE_JOUEUR = []

    while True:
        number = input("Entrez le nombre de joueurs (2 à 5 joueurs): ")

        if not check_user_input(number):
            print("[ERREUR: Vous devez entrer un nombre]")
            continue

        number_int = int(float(number))
        if 2 <= number_int <= 5:
            break

    for i in range(number_int):
        LISTE_JOUEUR.append(get_noms_joueurs())

    return LISTE_JOUEUR


# active player plays at the end
def playing_order(liste_joueurs, fiche_joueurs, active_player):
    """
    List x Str --> List
    renvoie la liste des joueurs où le joueur actif joue après les joueurs passifs
    """
    # Find active player
    liste_joueurs2 = liste_joueurs.copy()
    fiches = fiche_joueurs.copy()
    active_ind = liste_joueurs.index(active_player)

    # Remove active player
    liste_joueurs2.remove(active_player)
    active_fiche = fiches.pop(active_ind)

    # Add active player at the end
    liste_joueurs2.append(active_player)
    fiches.append(active_fiche)

    return liste_joueurs2, fiches


# Convert the color into an index number
def indice_couleur(couleur):
    """
    Str --> Int
    Fonction retournant l'indice de la couleur.
    """
    # rouge = 0, jaune = 1, bleu = 2, vert = 3
    return liste_couleur.index(couleur)


def get_dices():
    """
    None --> List
    Fonction qui renvoie une liste contenant les valeurs des dés
    """
    liste_dice = [randint(1, 6) if x is not None else None for x in liste_couleur]

    return liste_dice


def affiche_des(liste_dice):
    """
    List --> None
    affiche les valeurs des dés
    """
    # Affiche la valeur des dés blancs
    affiche(f"\nLes dés blancs: blanc1({liste_dice[-2]}) blanc2({liste_dice[-1]})")

    # Affiche la valeur des dés colorés
    affiche("Les dés colorés:", ask_end=" ")
    for couleur, dice_value in zip(liste_couleur[:-2], liste_dice):
        if couleur is not None:
            color_value = (f"{couleur}({dice_value})")
            affiche(f"{is_colored(color_value, couleur)}", ask_end=" ")
    affiche("")


def add_to_dict(line_color, combo):
    """
    List x Int --> None
    ajoute la somme d'un dé blanc et un dé coloré dans le dict global proposition
    """
    if line_color in proposition and combo not in proposition[line_color]:
        proposition[line_color].append(combo)

    else:
        if line_color is not None:
            proposition[line_color] = [combo]


# Adds 2 or 12 to the list of propositions if they can be added
def add_special(player_fiche, line_color, dice_value, type=list):
    """
    List x Str x Int (x Type) --> Str / None
    retourne le couleur de la ligne (ou ajoute des valeurs dans le dictionnaire global proposition)
    avec des possibles placements quand la somme de dés est 2 ou 12
    """
    line_couleur_ind = indice_couleur(line_color)

    if verif_premier(player_fiche, line_couleur_ind, dice_value):
        if type is list:
            return line_color

        add_to_dict(line_color, dice_value)


    elif verif_dernier(player_fiche, line_couleur_ind, dice_value):
        if type is list:
            return line_color

        add_to_dict(line_color, dice_value)


# Somme: blanc1 + blanc2
def combine_whites(liste_dice):
    """
    List --> INt
    retourne la somme de dés blancs
    """
    return liste_dice[-2] + liste_dice[-1]


# List of possible placements for the sum of white dices + the sum of the dices
def propose_white(player_fiche, white_dices):
    """
    List x Int --> List
    retourne une liste des couleurs oú la somme des dés blancs peut etre crochée (liste sans proposition si il n'y en a pas)
    """

    lines = []

    for line_color in liste_couleur[:-2]:
        # Check if line_color is locked
        if line_color is None:
            continue

        if white_dices in [12, 2]:
            line = add_special(player_fiche, line_color, white_dices)
            if line is not None:
                lines.append(line)

        # if it's any number {3, 4, 5, 6, 7, 8, 9, 10, 11}
        elif is_playable(player_fiche, indice_couleur(line_color), white_dices):
            lines.append(line_color)

    lines.append(white_dices)

    return lines


# Dictionary of possible placements for the combination of dices
# key = color, value = number that can be placed
def propose_combo(player_fiche, liste_dice):
    """
    List x List --> Dict
    retourne la dictionnaire des possible placements dans les lignes colorées
    """
    global proposition

    proposition = dict()
    index = 0

    for white, color in product(liste_dice[-2:], liste_dice[:-2]):
        line_color = liste_couleur[index]
        index += 1

        if color is None:
            continue

        combo = white + color

        # if it's [12, 2]
        if combo in [12, 2]:
            add_special(player_fiche, line_color, combo, type=dict)

        # else if it's any other number [3, 4, 5, 6, 7, 8, 9, 10, 11]
        elif is_playable(player_fiche, indice_couleur(line_color), combo):
            add_to_dict(line_color, combo)

        if index == 4:
            index = 0

    return proposition


def affiche_proposition(proposition):
    """
    List / Dict --> None
    affiche les lignes et nombres crochable
    """
    if type(proposition) is list:
        aff_proposition = []
        for i in range(len(proposition[:-1])):
            aff_proposition.append(is_colored(proposition[i], proposition[i]))
        affiche(f"Vous pouvez cocher {proposition[-1]} dans : {', '.join(str(color) for color in aff_proposition)}.")
        return
    
    for color in proposition:
        print(f"Ligne {is_colored(color, color)} : {', '.join(map(str, proposition[color]))}")


# Check if the number can be crossed on a line
def is_playable(player_fiche, couleur_ind, value):
    """
    List x Int x Int --> Bool
    Fonction retournant True si la valeur est plus grande que la dernière valeur de la ligne, False sinon.
    """
    if player_fiche[couleur_ind] == []:
        return True

    # Lignes jaune et rouge.
    if 0 <= couleur_ind <= 1:
        if player_fiche[couleur_ind][-1] < value:
            return True
        return False

    # Lignes bleue et verte.
    if player_fiche[couleur_ind][-1] > value:
        return True
    return False


# If number is 2 or 12, check if it can be placed as first element of the line
def verif_premier(player_fiche, couleur_ind, dice_value):
    """
    List x Int x Int --> Bool
    si le joueur veut crocher le premier numéro d'une ligne
    retourne vrai si c'est possible, faux sinon
    """
    # lignes jaune et rouge
    if dice_value == 2 and 0 <= couleur_ind <= 1 and is_playable(player_fiche, couleur_ind, dice_value):
        return True

    # lignes verte et bleue
    if dice_value == 12 and 2 <= couleur_ind <= 3 and is_playable(player_fiche, couleur_ind, dice_value):
        return True
    return False


# If number is 2 or 12, check if the line is lockable
def verif_dernier(player_fiche, couleur_ind, dice_value):
    """
    List x Int x Int --> Bool
    si le joueur veut crocher le dernier numéro d'une ligne
    retourne vrai si c'est possible, faux sinon
    """
    color_line_in_fiche = player_fiche[couleur_ind]

    # lignes jaune et rouge
    if dice_value == 12 and 0 <= couleur_ind <= 1 and len(color_line_in_fiche) >= 5 and 12 not in color_line_in_fiche:
        return True

    # lignes verte et bleue
    if dice_value == 2 and 2 <= couleur_ind <= 3 and len(color_line_in_fiche) >= 5 and 2 not in color_line_in_fiche:
        return True
    return False


# Add crossed number into player_fiche
def ajoute_numero(player_fiche, couleur_ind, value):
    """
    List x Int x Int --> None
    Processus qui permet d'ajouter le numéro coché sur la fiche
    """
    player_fiche[couleur_ind].append(value)


# Check if the line is locked (+5 crossed numbers and lock number is crossed)
def is_prelocked(player_fiche, color_ind):
    """
    List x Int --> Bool
    Fonction retournant True si la ligne comporte 5 cases cochées et le dernier numéro coché.
    """
    # lignes jaune et rouge
    if 0 <= color_ind <= 1 and 12 in player_fiche[color_ind]:
        return True

    # lignes bleue et verte
    if 2 <= color_ind <= 3 and 2 in player_fiche[color_ind]:
        return True
    return False


## Pour cocher blanc1 + blanc2 et les combo de couleur
def place_x(player_fiche, propositions, couleur, skip=0, dice_value=None, active_play=False):
    """
    List x List/Dict x Int (x Bool) --> Int
    demande au joueur de cocher un numéro, le coche si c'est possible et
    retourne skip+1 si le joueur decide de passer son tour
    """
    while True:
        # Pour tous les joueurs, choisir la ligne pour cocher la somme des blancs
        if not active_play:
            dice_value = propositions[-1]

        # Pour joueur actif (2nd round), choisir numéro
        if type(propositions) is dict:
            while dice_value not in propositions[couleur]:
                dice_value = affiche("Choisissez un numéro à cocher : ", ask_input=True)

                try:
                    dice_value = int(dice_value)
                except ValueError:
                    affiche("[ERREUR: Entrez un numéro.]")
                    continue

                if dice_value in propositions[couleur]:
                    break
                affiche("[ERREUR: Vous ne pouvez crocher ce numéro.]")

        # confirmer le choix
        couleur_ind = indice_couleur(couleur)
        confirm = affiche(f"Vous allez cocher le {is_colored(couleur, couleur)} {dice_value}. Etes-vous sûr (oui/non/pass) ? ", ask_input=True)

        if confirm.lower() in ["oui", "o"]:
            print(f"Vous avez coché le {is_colored(couleur + ' ' + str(dice_value), couleur)}.")
            
            if dice_value in [2, 12] and verif_dernier(player_fiche, couleur_ind, dice_value):
                affiche(f"You have successfully locked the {is_colored(couleur, couleur)} line.")
            
            ajoute_numero(player_fiche, couleur_ind, dice_value)

            break

        elif confirm.lower() in ["non", "n"]:
            affiche_proposition(propositions)
            while True:
                couleur = affiche("\nCochez dans la ligne (couleur/pass) : ", ask_input=True)
                if couleur in propositions or couleur in ["pass", "p"]:
                    break
                
                affiche("[ERREUR: Vous ne pouvez cocher dans cette ligne]")
            if couleur in propositions:
                dice_value = None
                continue
            else:
                affiche("Vous avez décidé de ne pas cocher de numéros.")
                skip += 1
                break

        elif confirm.lower() in ["pass", "p"]:
            affiche("Vous avez décidé de ne pas cocher de numéros.")
            skip += 1
            break

    return skip


def play_white(player_fiche, prop_whites, skip=0, bot = False):
    """
    List x Int (x Int) --> Int
    demande à tous les joueurs s'il veut c=ocher la somme de dés blancs
    retourne skip+1 si le joueur a décidé de passer ce tour
    """
    white_dice = prop_whites[-1]

    # si le joueur ne peut pas jouer, on quitte la fonction
    if len(prop_whites) == 1:
        affiche(f"Vous ne pouvez pas cocher {white_dice} dans aucune des lignes.")
        skip += 1
        return skip

    if not bot or player_name == "Joueur":
        while True:
            couleur = affiche(f"Cochez {white_dice} dans la ligne (couleur/pass) : ", ask_input=True)

            if couleur.lower() in prop_whites:
                skip += place_x(player_fiche, prop_whites, couleur)
                break

            elif couleur.lower() in ["pass", "p"]:
                affiche("Vous avez décidé de ne pas cocher de numéros.")
                skip += 1
                break
            affiche("[ERREUR: Commande invalide]")
    
    else:
        if player_name == "Roland" :
            couleur = choice(prop_whites[:-1] + ["pass"])

            if couleur in prop_whites :
                skip += place_x_bot(player_fiche, prop_whites, couleur)

            elif couleur == "pass" :
                affiche(f"{player_name} a décidé de ne pas cocher de numéros.")
                skip += 1

    return skip


def play_color(player_fiche, prop_color, skip=0, bot = False):
    """
    List x List x Int --> Int
    Fonction qui permet le jeu et qui renvoie le nombre de skip.
    """
    if not bot or player_name == "Joueur":
        
        if prop_color == {}:
            affiche(f"Vous ne pouvez pas cocher de numéros dans aucune ligne.")
            skip += 1
            return skip

        affiche("\n[Dé blanc + Dé couleur]")
        while True:
            couleur = affiche("\nCochez dans la ligne (couleur/pass) : ", ask_input=True)
            
            if couleur in ["pass", "p"]:
                affiche("Vous avez décidé de ne pas cocher de numéros.")
                skip += 1
                break

            if couleur not in liste_couleur:
                affiche("[ERREUR: Cette couleur de ligne n'existe pas]")
                continue

            elif couleur not in prop_color:
                affiche("[ERREUR: Vous ne pouvez cocher dans cette ligne]")
                continue

            elif couleur in prop_color:
                skip = place_x(player_fiche, prop_color, couleur, active_play=True)
                break
            affiche("[ERREUR: Commande invalide]")

    # if bot
    else :
        if prop_color == {}:
            affiche(f"{player_name} ne peut pas cocher de numéros dans aucune ligne.")
            skip += 1
            return skip

        affiche("\n[Dé blanc + Dé couleur]\nCochez dans la ligne (couleur/pass) :  ")
        couleur = choice(list(prop_color.keys()) + ["pass"])
        if couleur in prop_color :
            skip = place_x_bot(player_fiche, prop_color, couleur, active_play=True)

        else:
            affiche(f"{player_name} a décidé de ne pas cocher de numéros da.")
            skip += 1

    return skip
##

# Count skip (max: 2 for penaltie)
def count_skip(player_fiche, skip):
    """
    List x Int --> None
    Procédure qui compte le nombre de skip du joueur actif.
    """

    # if active player skip twice
    if skip == 2:
        player_fiche[-1] += 1
        affiche(f"Vous avez passé votre tour 2 fois, vous obtenez une pénalité. | Pénalités: {player_fiche[-1]}.")


# If the line has the locking number in it, it removes the dice
def lock_line(fiche_joueurs):
    """
    List --> None
    si la ligne est locked, le dé de la ligne est retiré
    """
    for fiche in fiche_joueurs:
        for color_ind in range(4):
            if is_prelocked(fiche, color_ind):
                remove_dice(color_ind)


# When a line is locked, the dice of color is removed
def remove_dice(couleur_ind):
    """
    Int --> None
    Procédure qui enleve un dé de la liste de dés.
    """
    line_color = liste_couleur[couleur_ind]

    if line_color is not None:
        affiche(f"Le dé {is_colored(line_color, line_color)} est retiré du jeu.")
        liste_couleur[couleur_ind] = None


## End conditions & calculates points to announce the winner
def check_end(fiche):
    """
    List --> Bool
    retourne True si le jeux est terminé, False sinon
    """
    # if someone has 4 penalties
    if fiche[-1] == 4:
        affiche(f"{player_name} a 4 pénalité.")
        return True

    # if 2 lines are locked <==> 2 dices are removed
    nones = sum(1 for i in liste_couleur if i is None)
    if nones == 2:
        affiche("Vous avez enlevez le deuxieme dé coloré.")
        return True

    return False


def who_won(fiche_joueurs, noms):
    """
    List x List --> None
    Compte des points et affiche le gagnant
    """
    affiche("Le jeu est terminé. \nLes points sont calculés... \n")
    sleep(2)

    points_joueurs = [0 for i in range(len(fiche_joueurs))]

    for player in range(len(fiche_joueurs)):
        # add points for each color
        for couleur in range(4):
            nombre_x = len(fiche_joueurs[player][couleur])
            points_joueurs[player] += points[nombre_x]

        # minus points for skips (penalty)
        points_joueurs[player] -= (fiche_joueurs[player][-1] * 5)

    winner_index = points_joueurs.index(max(points_joueurs))

    affiche(f"Vous avez gagné, {noms[winner_index]} avec {max(points_joueurs)} points.")
    affiche("Merci d'avoir joué ! \n[Exiting program...]")

    sleep(3)
    exit()
##


### Affichage
def create_fiche(reverse=False):
    """
    Bool --> Generator
    Generateur qui crée une liste de nombre pour la fiche à afficher.
    """

    if not reverse:
        for n in range(2, 13):
            if n != 2 and n != 12:
                yield " "
            elif n == 2:
                yield "2 "
            elif n == 12:
                yield "12"

    else:
        for n in range(12, 1, -1):
            if n != 2 and n != 12:
                yield " "
            if n == 12:
                yield "12"
            if n == 2:
                yield " 2"


def is_colored(str, color):
    """
    Int --> None
    Fonction qui retourne un texte donnée en texte colorié.
    """
    # texte rouge
    if color == "rouge" or color == "r" :
        colored = (f"{Fore.RED}{str}{Style.RESET_ALL}")

    # texte jaune
    elif color == "jaune" or color == "j" :
        colored = (f"{Fore.YELLOW}{str}{Style.RESET_ALL}")

    # texte bleu
    elif color == "bleu" or color == "b" :
        colored = (f"{Fore.BLUE}{str}{Style.RESET_ALL}")

    # texte vert
    else:
        colored = (f"{Fore.GREEN}{str}{Style.RESET_ALL}")
    return colored


def update_fiche(fiche, player_fiche, index=0):
    """
    List x List x Int --> None
    Procédure qui ajoute des 'x' aux cases cochés dans fiche à afficher.
    """

    for fiche_couleur in player_fiche[:-1]:
        if fiche_couleur == []:
            index += 1
            continue

        for value in fiche_couleur:
            if 0 <= index <= 1:
                if value == 2:
                    fiche[index][value - 2] = "x "
                elif value == 12:
                    fiche[index][value - 2] = " x"
                else:
                    fiche[index][value - 2] = "x"

            else:
                if value == 2:
                    fiche[index][12 - value] = " x"
                elif value == 12:
                    fiche[index][12 - value] = "x "
                else:
                    fiche[index][12 - value] = "x"

        index += 1


def affiche_fiche(fiche):
    """
    List --> None
    Procédure qui affiche la fiche du joueur.
    """

    for index, fiche_couleur in enumerate(fiche):
        # Pour afficher r, j, b, v en couleur
        firstcolor_letter = liste_couleur[index][0]
        print(f"{is_colored(firstcolor_letter, firstcolor_letter)} |", end="")

        for case in fiche_couleur:
            print(f" {case} |", end="")

        if fiche[index][10] == " x" or fiche[index][10] == " x":
            print(" fermée")
        else:
            print()


def affiche(texte, ask_input=False, ask_end=None, full_bot=False):
    """
    str x Bool -> Elem (si ask_input est vrai, None sinon)
    Fonction permettant l'affichage et la demande d'input.
    """

    if full_bot:
        return

    # if input()
    if ask_input:
        sleep(0.5)
        ask = input(texte)
        sleep(0.5)
        return ask

    # if print(str, end="")
    if ask_end is not None:
        print(texte, end=ask_end)

    # print(str) standard
    else:
        print(texte)
        sleep(0.5)

###


#### Notes et problèmes ####

# Les éléments primaires sont: la fiche du joueur, les dés (2w, 1r, 1g, 1b, 1y),
# Les éléments secondaires sont: les conditions d'arrêt, cocher un case de la fiche, les conditions pour pouvoir cocher une case, sélection de personnage, tour par tour, pénalités, active_player

# fiche_player: liste d'élément, chaque élément correspond à une ligne de la fiche écrit en str, les str sont les numéros cochés enregistrés en base 16. La pénalité (int) est le dernier élément de la liste.
# #

def mode_dev():
    dice_value = [int(x) for x in input("Entrez 6 dés (rjbv/b1b2): ").split(" ")]
    return dice_value


# setup
liste_couleur = ["rouge", "jaune", "bleu", "vert", "blanc1", "blanc2"]
# dictionnaire stockant le nom des IA
difficultes = {"facile" : "Roland", "moyen" : "Jordan", "difficile": "Jennifer"}

CURR_DIR = os.getcwd()
SAVE_DIR = os.path.join(CURR_DIR, "saved_games")
preset_save_files = ["save1.json", "save2.json", "save3.json"]


def game_no_bot(loaded_game):
    global active_player, player_name
    global data_to_save

    print("\n======================")
    print("     JEU DU QWIXX")
    print("======================\n")

    affiche("[Pour sauvegarder, tapez SAVE ou SAUVEGARDER avant lancer le dé.]\n")

    # [Initialisation]
    if loaded_game:
        liste_joueurs, fiche_joueurs = saved_game_orders()

    else:
        liste_joueurs = add_player()
        fiche_joueurs = [[[], [], [], [], 0] for i in liste_joueurs]

    affiche(f"\nVous pouvez commencer! Ordre de lancer: {liste_joueurs} \n")

    # Start
    mode = input("mode dev (o/n)? ")

    running = True
    while running:
        for active_player in liste_joueurs:
            affiche(f"\n[Tour de lancer: {active_player}]")

            # Trow dice
            if mode == "o":
                liste_dice = mode_dev()
            else:
                start_round = input("Appuyer sur ENTER pour lancer le dé: ")
                # to save game
                if start_round.lower() in ["save", "sauvegarder"]:
                    save_file = choose_save_file()
                    save_game(data_to_save, save_file)
                    new_filename = input(
                        "Saisissez un nouveau nom pour le fichier (laissez vide pour utiliser le nom existant) : ")

                    if new_filename.strip() != "":
                        new_filename += ".json"
                        os.rename(os.path.join(SAVE_DIR, save_file), os.path.join(SAVE_DIR, new_filename))
                        save_file = new_filename
                        save_game(data_to_save, save_file)

                    affiche(f"Jeu sauvegardé ! Vos données : {data_to_save}")
                    sleep(1)

                    affiche("Merci d'avoir joué ! \n[Exiting program...]")
                    sleep(3)
                    exit()

                else:
                    liste_dice = get_dices()

            # Additionner les dés blancs et affiche la valeur des dés
            affiche_des(liste_dice)
            white_dice = combine_whites(liste_dice)

            # set up ordre_joueur
            ordre_joueur, ordre_fiche = playing_order(liste_joueurs, fiche_joueurs, active_player)
            sleep(1)

            # Play2
            for player_num, player_name in enumerate(ordre_joueur):
                print(f"\n  [{player_name}]")

                # set up player_fiche
                player_fiche = ordre_fiche[player_num]
                fiche = [list(create_fiche()) for i in range(2)] + [list(create_fiche(reverse=True)) for i in range(2)]

                # update and affiche fiche
                update_fiche(fiche, player_fiche)
                affiche_fiche(fiche)
                
                # propositions
                prop_whites = propose_white(player_fiche, white_dice)
                prop_color = propose_combo(player_fiche, liste_dice)

                if player_name != active_player :
                    affiche_proposition(prop_whites)
                    nb_skip = play_white(player_fiche, prop_whites)

                else :
                    affiche("Vous êtes le joueur actif.")
                    affiche_proposition(prop_whites)
                    
                    affiche("En plus, vous pouvez combiner un dé blanc avec un dé coloré.")
                    affiche_proposition(prop_color)

                    affiche("\n[Dés blancs]")
                    nb_skip = play_white(player_fiche, prop_whites)

                    if nb_skip != 1 :
                        prop_color = propose_combo(player_fiche, liste_dice)
                        affiche_proposition(prop_color)
                    nb_skip += play_color(player_fiche, prop_color)
                    
                    # check penalties
                    count_skip(player_fiche, nb_skip)

            # if a line was locked, remove its dice
            lock_line(fiche_joueurs)

            # check end conditions
            if check_end(player_fiche):
                running = False
                break

            data_to_save = list(zip(ordre_joueur, ordre_fiche))

    # Calcul et affiche le vainqueur
    who_won(fiche_joueurs, ordre_joueur)


# [note:on pourra affronter plusieurs bots identiques ? [niveau for niveau in difficultes] ou list(niveau for niveau in difficultes) ?]
def get_difficulte_bot():
    """
    Int --> List
    Fonction retournant la liste des difficultés de chaque bot
    """

    while True:
        difficulte = input("Veuillez entrer la difficulté du bot: ")

        if difficulte in difficultes:
            return difficultes[difficulte]
        
        affiche(f"Cette difficulté n'existe pas. Les difficultés disponibles sont: \n{[niveau for niveau in difficultes]}")


def place_x_bot(player_fiche, propositions, couleur, skip=0, dice_value=None, active_play=False, full_bot=False):
    """
    List x List/Dict x Int (x Str) --> Int
    demande au joueur de cocher un numéro, le coche si c'est possible et
    retourne skip+1 si le joueur decide de passer son tour
    """
    
    while True:
        # Choisir la ligne pour cocher la somme des blancs
        if not active_play:
            dice_value = propositions[-1]
            affiche(f"{player_name} a coché le {is_colored(couleur + ' ' + str(dice_value), couleur)}.", full_bot)
        
        # Pour joueur actif in his second round, same as above
        if type(propositions) is dict:
            dice_value = choice(proposition[couleur])
            affiche(f"{player_name} a coché le {is_colored(couleur + ' ' + str(dice_value), couleur)}.")

        couleur_ind = indice_couleur(couleur)

        if dice_value in [2, 12] and verif_dernier(player_fiche, couleur_ind, dice_value):
            affiche(f"You have successfully locked the {is_colored(couleur, couleur)} line.", full_bot)

        ajoute_numero(player_fiche, couleur_ind, dice_value)
        break

    return skip


# [note: le bot ne peut pas get_dices() ? on sauvegarde les données dans game_with_bot ?]
def game_with_bot():
    global active_player, player_name

    print("\n======================")
    print("     JEU DU QWIXX")
    print("======================\n")

    # [Initialisation]
    liste_joueurs = ["Joueur", get_difficulte_bot()]
    fiche_joueurs = [[[], [], [], [], 0] for i in liste_joueurs]
    
    affiche(f"Vous allez jouer contre {liste_joueurs[1]}.")
    affiche(f"\nVous pouvez commencer! Ordre de lancer: {liste_joueurs} \n")

    # Start
    running = True
    while running:
        for active_player in liste_joueurs :
            affiche(f"\n[Tour de lancer: {active_player}]")

            # Trow dice
            if active_player == "Joueur" :
                input("Appuyer sur ENTER pour lancer le dé: ")
            liste_dice = get_dices()

            # Addition les dés blancs et affiche la valeur des dés
            affiche_des(liste_dice)
            white_dice = combine_whites(liste_dice)

            # set up ordre_joueur
            ordre_joueur, ordre_fiche = playing_order(liste_joueurs, fiche_joueurs, active_player)
            sleep(1)

            # Play2
            for player_num, player_name in enumerate(ordre_joueur):
                print(f"\n  [{player_name}]")

                # set up player_fiche
                player_fiche = ordre_fiche[player_num]
                fiche = [list(create_fiche()) for i in range(2)] + [list(create_fiche(reverse=True)) for i in range(2)]

                # update and affiche fiche
                update_fiche(fiche, player_fiche)
                affiche_fiche(fiche)

                # propositions
                prop_whites = propose_white(player_fiche, white_dice)
                prop_color = propose_combo(player_fiche, liste_dice)

                if player_name != active_player :
                    affiche_proposition(prop_whites)
                    nb_skip = play_white(player_fiche, prop_whites, bot = True)

                else:
                    affiche("Vous êtes le joueur actif.")
                    affiche_proposition(prop_whites)
                    
                    affiche("En plus, vous pouvez combiner un dé blanc avec un dé coloré.")
                    affiche_proposition(prop_color)

                    affiche("\n[Dés blancs]")
                    nb_skip = play_white(player_fiche, prop_whites, bot = True)

                    if nb_skip != 1 :
                        prop_color = propose_combo(player_fiche, liste_dice)
                        affiche_proposition(prop_color)
                    nb_skip += play_color(player_fiche, prop_color, bot = True)
                    
                    # check penalties
                    count_skip(player_fiche, nb_skip)

            # if a line was locked, remove its dice
            lock_line(fiche_joueurs)

            # check end conditions
            if check_end(player_fiche):
                running = False
                break

    # Calcul et affiche le vainqueur
    who_won(fiche_joueurs, ordre_joueur)


def game_full_bot():
    pass


# [note: le game_no_bot fait un exit(), "else" nécessaire ?]
## choose game mode
def choice_gamemode():
    global bot_game

    # ask if player wants to load previous game
    loaded_game = ask_to_load()
    bot_game = False

    if loaded_game:
        affiche("\n")
        game_no_bot(loaded_game)

    else:
        # ask gamemodes
        while True:
            affiche("(1) Mode local avec joueurs\n(2) Mode solo avec bots\n(3) Mode uniquement bots")

            game_mode = input("Entrez un mode de jeu : ")

            if game_mode in ["1", "2", "3"]:
                break

            affiche("[ERREUR : Ce mode ne fait pas partie des modes de jeu]\n")

        sleep(1)
        if game_mode == "1":
            affiche("\n\n[Mode local avec joueurs]")
            game_no_bot(loaded_game)

        elif game_mode == "2":
            affiche("\n\n[Mode solo avec bots]")
            game_with_bot()

        else:
            bot_game = True
            affiche("\n\n[Mode uniquement bots]")
            game_full_bot()


# Commandes start
choice_gamemode()
