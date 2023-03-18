
from time import sleep
from random import randint

points = {
        1 : 1,
        2 : 3,
        3 : 6,
        4 : 10,
        5 : 15,
        6 : 21,
        7 : 28,
        8 : 36,
        9 : 45,
        10: 55,
        11: 66,
        12: 75
    }
 

# To get the name of the players
def get_noms_joueurs():
    """
    None -> Str
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
    Str -> Bool
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
def select_player():
    """
    None -> List
    Fonction retournant la liste des joueurs.
    """

    global LISTE_JOUEUR
    global i

    LISTE_JOUEUR = []

    while True:
        number = input("Entrez le nombre de joueur (2 à 5 joueurs): ")
        
        if not check_user_input(number):
            print("[ERREUR: Vous devez entrez un nombre]")
            continue

        number_int = int(float(number))
        if 2 <= number_int <= 5:
            break

    for i in range(number_int):
        LISTE_JOUEUR.append(get_noms_joueurs())

    return LISTE_JOUEUR

# The order will be random
def who_starts():
    pass


# When a line is locked, the dice of color is removed
def remove_dice(couleur):
    liste_couleur[indice_couleur(couleur)] = None


def get_dice():
    """
    None -> list
    Fonction qui renvoie une liste contenant les valeurs des dés
    """

    liste_dice = [randint(1, 6) if x is not None else None for x in liste_couleur]

    return liste_dice


# probleme avec remove_dice
def fusion_dice(liste_dice):
    # ask dice color
    while True:
        print("Entrez la couleur du dé à combiner:", end = " ")
        
        for color, dice_value in zip(liste_couleur[:-2], liste_dice):
            if color is not None:
                print(f"{color}({dice_value})", end = " ")

        choix2 = input("\n> ")
        
        if choix2.lower() in liste_couleur[:-2]:
            break
        print("[ERREUR : Couleur de dé introuvable]\n")

    # ask white dice to combine with
    while True:
        choix3 = input("\nVous voulez combiner cette couleur avec lequel des dés blancs ? {} qui valent {}: \n> ".format(liste_couleur[-2:], liste_dice[-2:]))

        if choix3 in liste_couleur[-2:]:
            break    
        print("[ERREUR: Couleur de dé introuvable]")

    # somme = valeur(couleur) + valeur(blanc)
    somme = liste_dice[liste_couleur.index(choix2)] + liste_dice[liste_couleur.index(choix3)]
                    
    return somme


# Convert the color as a number
def indice_couleur(couleur):
    """
    Str -> Int 
    Fonction retournant l'indice de la couleur.
    """

    if couleur == "rouge" or couleur == "r":
        return 0
    
    elif couleur == "jaune" or couleur == "j":
        return 1
    
    elif couleur == "bleu" or couleur == "b":
        return 2
    
    # Ligne est vert
    return 3


# Check if the number can be cross on a line.
def verif_num_supp(player_fiche, couleur, value):
    """
    List x Int x Int -> Bool
    Fonction retournant True si la valeur est plus grande que la dernière valeur de la ligne, False sinon. 
    """

    if player_fiche[couleur] == []:
        return True

    # Ligne jaune et rouge.
    if 0 <= couleur <= 1:
        if player_fiche[couleur][-1] < value:
            return True
        return False

    # Ligne bleue et verte.
    if player_fiche[couleur][-1] > value:
        return True
    return False
    

# Check if the line is lockable (>5 cross)
def verif_line_lockable(player_fiche, couleur):
    if len(player_fiche[couleur]) < 5:
        return False
    return True


# Cross number on the line
def ajoute_numero(player_fiche, couleur, value):
    """
    List x Int x Int -> None
    Processus qui permet d'ajouter le numéro coché sur la fiche
    """

    player_fiche[couleur].append(value)


# Check if the line is lock or not (+5 crossed numbers and lock number is crossed)
def is_locked(player_fiche, couleur):
    """
    List, Int -> Bool
    Fonction retournant True si la ligne comporte 5 cases cochées et le dernier numéro coché.
    """
    # ligne jaune et rouge
    if 0 <= couleur <= 1 and 12 in player_fiche[couleur]:
        return True

    # ligne bleue et verte
    if 2 <= couleur <= 4 and 2 in player_fiche[couleur]:
        return True        
    return False


def place_x(player_fiche, dice_value) :
    #ajouter des lignes pour afficher les dé actifs
    while True:
        ask_color = input(f"Entrez une couleur de ligne pour cocher le numéro {dice_value}: \n> ")
        
        if ask_color.lower() not in liste_couleur:
            print("[ERREUR: Cette couleur de ligne n'existe pas]\n")
            continue

        couleur = indice_couleur(ask_color.lower())
        
        if not verif_num_supp(player_fiche, couleur, dice_value):
            print(f"{dice_value} ne peut pas être coché sur cette ligne. Recommencez.")
            continue

        ajoute_numero(player_fiche, couleur, dice_value)
        break

        
def play(player_name, player_fiche, liste_dice, dice_value, skip = 0, lock = False) :
    ask = input(f"{player_name} voulez-vous cocher la somme des dés blancs {dice_value} (oui/pass)? \n> ")

    # players turn 
    if ask.lower() == "oui" or ask.lower() == "o" :
        place_x(player_fiche, dice_value)
    
    elif ask.lower() == "pass" or ask.lower() == "p":
        print("Vous avez passé votre tour.")
        skip += 1
    
    else:
        print("[ERREUR: Commande invalide]")
        return play(player_name, player_fiche, liste_dice, dice_value)

    # active player seconde turn
    if player_name == active_player and not(lock):
        print("\nVous êtes le joueur actif.")
        sleep(0.5)
        print("Vous pouvez combiner un dé blanc avec un dé coloré.")
        sleep(0.5)

        dice_value = fusion_dice(liste_dice)

        while True:
            ask = input(f"\n{player_name} voulez-vous cocher le numéro {dice_value} (oui/pass)? \n> ")
            
            if ask.lower() == "oui" or ask.lower() == "o" :
                player_fiche = place_x(player_fiche, dice_value)
                break
            
            elif ask.lower() == "pass" or ask.lower() == "p":
                print("Vous avez passé votre tour.")
                skip += 1
                break
            print("[ERREUR: Commande invalide]")

    # if active player skip twice
    if skip == 2:
        player_fiche[-1] += 1
        print(f"Vous avez obtenu une pénalité. | Pénalités: {player_fiche[-1]}.")


# End/Win conditions
def check_end(player_fiche, player_name, couleurs):
    #if someone has 4 penalties
    if player_fiche[-1] == 4 :
        print(f"{player_name} a 4 pénalité.")
        return True
    
    #if 2 lines are locked <==> 2 dices are removed
    if len(couleurs) == 4:
        print("Vous avez enlevez le deuxieme dé coloré.")
        return True
    
    return False

#calculates points and tells who is the winner
#normally the fiche_joueurs should be in playing order so it matches the names in order
def who_won(fiche_joueurs, player_names):
    """
    Compte des points et affiche le gagnant
    """
    print("Le jeu est terminé. \nLes points sont calculés... \n")
    sleep(2)
    
    points_joueurs = [0 for i in range(len(fiche_joueurs))]

    for player in range(len(fiche_joueurs)) :
        # add points for each colour
        for couleur in range(4) :
            nombre_x = len(fiche_joueurs[player][couleur])
            points_joueurs[player] += points[nombre_x]
            
        # minus points for skips (penalty)
        points_joueurs[player] -= (fiche_joueurs[player][-1] * 5)
    
    winner_index = points_joueurs.index(max(points_joueurs))
    print(f"Vous avez gagné, {player_names[winner_index]} avec {max(points_joueurs)} points.")
    

## Notes et problèmes ##

# Les éléments primaires sont: la fiche du joueur, les dés (2w, 1r, 1g, 1b, 1y), 
# Les éléments secondaires sont: les conditions d'arrêt, cocher un case de la fiche, les conditions pour pouvoir cocher une case, sélection de personnage, tour par tour, pénalités, active_player

# fiche_player: liste d'élément, chaque élément correspond à une ligne de la fiche écrit en str, les str sont les numéros cochés enregistrés en base 16. La pénalité (int) est le dernier élément de la liste. 

# condition d'arrêt [PAS CODER]
# 
##



#setup
dice = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
liste_couleur = ["rouge", "jaune", "bleu", "vert", "blanc1", "blanc2"]


def game_no_bot():
    global active_player

    print("\n======================")
    print("     JEU DU QWIXX")
    print("======================\n")  


    # [Initialisation provisoire]
    liste_joueurs = select_player()
    fiche_joueurs = [[[], [], [], [], 0] for i in range(len(liste_joueurs))]
    ordre_joueur = liste_joueurs

    sleep(1)
    print(f"\nVous pouvez commencer! Ordre de lancer: {ordre_joueur} \n")
    sleep(0.5)

    # Start
    running = True
    while running:
        for active_player in ordre_joueur:
            print(f"\n[Tour de lancer: {active_player}]")

            # Trow dice
            input("Appuyer sur ENTER pour lancer le dé: ")
            liste_dice = get_dice()
            white_dice = liste_dice[-2] + liste_dice[-1]

            # Affiche la valeur des dés blancs
            print(f"\nLes dés blancs: {liste_couleur[-2]}({liste_dice[-2]}) {liste_couleur[-1]}({liste_dice[-1]})")

            sleep(0.5)

            # Affiche la valeur des dés colorés
            print("Les dés colorés:", end = " ")
            for index, dice_value in enumerate(liste_dice[:-2]):
                print(f"{liste_couleur[index]}({dice_value})", end = " ")
            
            print()
            sleep(1)
        
            # play
            for player_number, player in enumerate(ordre_joueur):
                # Set up player_fiche
                player_fiche = fiche_joueurs[player_number] 

                print(f"\n[{player}]")
                play(player, player_fiche, liste_dice, white_dice)

            
game_no_bot()