# *************************************************************************************************************************************
# Titre : test lire les tensions d'un accelerometre analogique
# Auteur : Y SKO
# Date :
# Microcontroleur : RPI Pico
# IDE : Thonny 3.3.13 sous windows 10 64 bits
# Interpreteur : MicroPython v1.14 on 2021-02-05
# Accelerometre : Module GY-61 – Accéléromètre 3 axes à ADXL335 – Sortie analogique
# Aide sur : http://www.mon-club-elec.fr/pmwiki_mon_club_elec/pmwiki.php?n=MAIN.MaterielCapteurAnalogAccelerometreADXL3353axes3g
# Support 3 D : https://www.thingiverse.com/thing:662505
#**************************************************************************************************************************************



#*****************************************************************************************************************************************
#DEBUT DU PROGRAMME
#*****************************************************************************************************************************************


#*****************************************************************************************************************************************
# Importation des bibliotheques utilisées
import machine # permet de nommer les broches du pico
import utime   # Permet d'utiliser des tempos en millisecondes


#*****************************************************************************************************************************************
# Definition des pins du pico vers ADXL335
Axe_X = machine.ADC(28)                                                          # Broche analogique 28
Axe_Y = machine.ADC(27)                                                          # Broche analogique 27
Axe_Z = machine.ADC(26)                                                          # Broche analogique 26
Interrupteur = machine.Pin(20, machine.Pin.IN, machine.Pin.PULL_UP)              # broche interrupteur d'etallonnage 20


#*****************************************************************************************************************************************
# definition des constantes

# facteur de conversion
Conversion_CAN = 3.3 / (65535)                                                   # pour une mesure 16bits de 0 à 65535 paliers avec une tension de 3.3 V
arrondit = 2                                                                     # permet d'arrondir les mesures apres la virgule


#*****************************************************************************************************************************************
# Fonction de mise a zero etalonnage 
def etallonnage () :
    x=float                                                                      # variable intermediaire pour recuperer la valeur de l'axe x en 16 bits
    y=float                                                                      # variable intermediaire pour recuperer la valeur de l'axe y en 16 bits
    z=float                                                                      # variable intermediaire pour recuperer la valeur de l'axe z en 16 bits
    liste_x=[]                                                                   # liste des accelerations en x pour faire une moyenne (50 mesures)
    liste_y=[]                                                                   # liste des accelerations en y pour faire une moyenne (50 mesures)
    liste_z=[]                                                                   # liste des accelerations en z pour faire une moyenne (50 mesures)
    global Zero_X                                                                # variable finale en x de l'acceleration a l'état initial (offset)
    global Zero_Y                                                                # variable finale en y de l'acceleration a l'état initial (offset)
    global Zero_Z                                                                # variable finale en z de l'acceleration a l'état initial (offset)
    i=0
    for i in range (50) :                                                        # On fait 50 mesures pour une moyenne
        x = Axe_X.read_u16()                                                     # lire la valeur 16 bits de la broche 28
        y = Axe_Y.read_u16()                                                     # lire la valeur 16 bits de la broche 27
        z = Axe_Z.read_u16()                                                     # lire la valeur 16 bits de la broche 26
        liste_x.append(x)                                                        # creation d'une liste de valeurs contenant les 20 mesures d'accelerations en x
        liste_y.append(y)                                                        # creation d'une liste de valeurs contenant les 20 mesures d'accelerations en y
        liste_z.append(z)                                                        # creation d'une liste de valeurs contenant les 20 mesures d'accelerations en z

    Zero_X = sum(liste_x) * Conversion_CAN /50                                                        # Moyenne de l'acceleration en X sur 50 mesures
    Zero_Y = sum(liste_y) * Conversion_CAN /50                                                        # Moyenne de l'acceleration en Y sur 50 mesures
    Zero_Z = sum(liste_z) * Conversion_CAN /50                                                        # Moyenne de l'acceleration en Z sur 50 mesures
    vecteur_Acc_initial=[round(Zero_X,arrondit), round(Zero_Y,arrondit), round(Zero_Z,arrondit)]      # Création vecteur acceleration [X, Y, Z]
    print('\033[31m' + "Conditions initiales")                                                        # Affiche en rouge le texte 
    print ("  en X     en Y   en Z" '\033[0m')                                                        # Affiche le vecteur
    print(vecteur_Acc_initial)                                                                        # Donne le vecteur

#******************************************************************************************************************************************
# Programme de l'attente de detection le compte à rebours        
def attente_de_detection() :
    print("Detection dans :")
    num_seconds = 3                                          # Routine de decompte 3.2.1.Go
    for compteur in reversed(range(num_seconds + 1)):        # pour 
        if compteur > 0:                                     # test si le decompte arrive à zero
            print(compteur, end='...')                       # affiche le compteur et passe ... à la fin 
            utime.sleep(1)                                   # Attente 1 seconde et reboucle
        else:                                                # Si compteur finit affiche c'est partit
            print("C'est partit !")
            print( "  ")

#******************************************************************************************************************************************
# Programme de mesures directes
def mesure () :
    vecteur_Acc = [3]                                        # Definition d'un vecteur acceleration 10 mesures
    i=0                                                      # initialisation du compteur de 10 mesures
    x2, y2, z2 =float, float, float                          # variable intermediaire pour recuperer la valeur de l'axe x en 16 bits
   # y2=float                                                # variable intermediaire pour recuperer la valeur de l'axe x en 16 bits
   # z2=float                                                # variable intermediaire pour recuperer la valeur de l'axe x en 16 bits
    liste_x2=[]                                              # liste des accelerations en x pour faire une moyenne (10 mesures)
    liste_y2=[]                                              # liste des accelerations en y pour faire une moyenne (10 mesures)
    liste_z2=[]                                              # liste des accelerations en z pour faire une moyenne (10 mesures)
    global X                                                 # variable finale en x de l'acceleration sans avoir enlevé l'offset
    global Y                                                 # variable finale en x de l'acceleration sans avoir enlevé l'offset
    global Z                                                 # variable finale en x de l'acceleration sans avoir enlevé l'offset
    for i in range(10) :                                     # Va lire 10 fois la valeur de l'acceleration pour chaque axe
        
        x2 = Axe_X.read_u16()                                # lire la valeur 16 bits de la broche 28
        liste_x2.append(x2)                                  # creer une liste des valeurs en x
        y2 = Axe_Y.read_u16()                                # lire la valeur 16 bits de la broche 27
        liste_y2.append(y2)                                  # creer une liste des valeurs en y
        z2 = Axe_Z.read_u16()                                # lire la valeur 16 bits de la broche 26
        liste_z2.append(z2)                                  # creer une liste des valeurs en z
        
    X = sum(liste_x2) * Conversion_CAN /(10)                 # fait la moyenne des acceleration en x et convertit en volts
    Y = sum(liste_y2) * Conversion_CAN /(10)                 # fait la moyenne des acceleration en y et convertit en volts
    Z = sum(liste_z2) * Conversion_CAN /(10)                 # fait la moyenne des acceleration en z et convertit en volts
    acc_X_enV = X - Zero_X                                   # on enleve la mesure d'étalonnage en x
    acc_Y_enV = Y - Zero_Y                                   # on enleve la mesure d'étalonnage en y
    acc_Z_enV = Z - Zero_Z                                   # on enleve la mesure d'étalonnage en z

#*****************************************************************************************************************************************
# creation du vecteur acceleration et arrondit à la valeur definie le nombre de chiffre apres la virgule
    vecteur_Acc= [round(acc_X_enV,arrondit), round(acc_Y_enV,arrondit), round(acc_Z_enV,arrondit)]     
    print ("  en X   en Y    en Z")                                                                     # affiche le print x y z
    print(vecteur_Acc)                                                                                  # affiche le vecteur en liste
    print ("")                                                                                          # passe une ligne
   
    return vecteur_Acc

#*****************************************************************************************************************************************
# def graphique() : # va falloir lancer un script dans un autre environnement ATTENTION 


#*****************************************************************************************************************************************
# Programme de test si etallonnage demandé par l'utilisateur

def demande_etalonnage() :
    if not Interrupteur.value() == False:
        print ("")
        print ("")
        print ('\033[92m' + "etallonnage demandé par l'user" '\033[0m')
        print ("  ")
        etallonnage()
        attente_de_detection()
    else :
        print ("Accelerations mesurées")
        mesure()
    utime.sleep_ms(500)        


#*****************************************************************************************************************************************
# programme principal

etallonnage()                                                                                  # lance l'etallonage
attente_de_detection()                                                                         # programme de decompte it's fun
while True :                                                                                   # Boucle infinie tant que vrai 
    demande_etalonnage()                                                                       # lance les mesures 
    utime.sleep_ms(500)                                                                        # Attente 
