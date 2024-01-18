"""
Created on Thu Jan 11 10:50:11 2024

@author: rbouv
"""

import pandas as pd

def readCsv():
    """
    la fonction readCsv permet de lire et d'ouvrir le fichier CSV dans python

    Returns
    -------
    ADE : pandas.DataFrame
        ADE contient le fichier csv avec les colonnes 0, 1, 4 et 5 et sans la colonne des indices

    """
    ADE = pd.read_csv("fichier_separe.csv", delimiter=";", encoding="ISO-8859-1", usecols=[1, 4, 5])
    print(ADE)
    print(ADE["TD"].unique())
    return ADE

def transformTp(ADE):
    """
    la fonction transforme les cours qui ont comme classe un TP en cours avec un TD 

    Parameters
    ----------
    ADE : pandas.DataFrame
        le fichier csv avec les TP

    Returns
    -------
    ADE : pandas.DataFrame
        la fichier csv avec uniquement des TD dans la colonne "TD"

    """
    for ligne in range(len(ADE)):  #on itère sur toutes les lignes du DataFrame
        #si la colonne est un TP, on le change par un TD
        if ADE.loc[int(ligne), "TD"] in ["TP1", "TP2", "TP3", "TP4", "TP5"]:
            if ADE.loc[int(ligne), "TD"] == "TP1" or ADE.loc[int(ligne), "TD"] == "TP2":
                ADE.loc[int(ligne), "TD"] = "TDA"
            elif ADE.loc[int(ligne), "TD"] == "TP3" or ADE.loc[int(ligne), "TD"] == "TP4":
                ADE.loc[int(ligne), "TD"] = "TDB"
            else:
                ADE.loc[int(ligne), "TD"] = "TDC"
    print(ADE["TD"].unique())
    return ADE
    
def getTd(nomTd:str, ADE):
    """
    la fonction getTd permet de récuperer les cours uniquement pour le TD concerné

    Parameters
    ----------
    nomTd : str
        nomTd est le nom du TD duquel on veut le planning

    ADE : pandas.DataFrame
        ADE contient le fichier csv
        
    Returns
    -------
    ADE : pandas.Dataframe
        ADE contient le fichier csv avec les lignes qui ne sont pas du bon TD qui ont été supprimé

    """
    
    ligneASupprimer = [] #on fait une liste des lignes à supprimer
    print(ADE["TD"].unique())
    for ligne in range(len(ADE)): #pour chaque ligne du dataframe
        #on regarde si le nom ne correspond pas au TD
        #print(f"Nom du TD: {ADE.loc[int(ligne), 'TD']}")
        if (nomTd != ADE.loc[int(ligne), "TD"]) & (nomTd + "-PT" != ADE.loc[int(ligne), "TD"]) & ("Cours" != ADE.loc[int(ligne), "TD"]) & ("Examen" != ADE.loc[int(ligne), "TD"]):
            ligneASupprimer.append(ligne) #si il ne correspond pas, on l'ajoute à la liste des lignes à supprimer
    ADE.drop(index=ligneASupprimer, inplace=True) #on supprime les lignes à supprimer
    
    ADE.reset_index(drop=True, inplace=True) #on remet les indices de 1 à n
    return ADE

getTd("TDB", transformTp(readCsv()))

def getMatières(ADE):
    """
    La fonction getMatières permet d'avoir une liste contenant toutes les matières de l'emploi du temps

    Parameters
    ----------
    ADE : pandas.DataFrame
        le DataFrame contenant les données

    Returns
    -------
    listeMatière : list
        liste contenant toutes les matières

    """
    listeMatière = [] #on créer une liste vide qui va contenir les matière
    for ligne in range(len(ADE)): #pour chaque ligne du DataFrame
        if ADE.loc[int(ligne), "Summary"] not in listeMatière: #si la matière de la ligne n'est pas déjà dans la liste listeMatière
            listeMatière.append(ADE.loc[int(ligne), "Summary"]) #on ajoute cette matière dans la liste 
    return listeMatière #on retourne la liste listeMatière



def getDates(ADE, matiere):
    """
    la fonction getDates récupère les dates de début et de fin pour la matière mis en paramètre

    Parameters
    ----------
    ADE : pandas.DataFrame
        le DataFrame contenant les données
    matiere : str
        le nom de la matière dont on récupère les dates de début et de fin

    Returns
    -------
    debut, fin : str
        les dates de début et de fin pour la matière mis en argument
    """
    ligneMatiere = ADE[ADE["Summary"] == matiere] #on sélectionne uniquement les lignes avec la matière spécifié
    print(ligneMatiere)
    debut = ligneMatiere["Date"].min() #on regarde le minimum de la date donc la date de début
    fin = ligneMatiere["Date"].max() #on regarde le maximum de la date donc la date de fin
    return debut, fin #on retourne les deux variables début et fin

def construireListeDates(ADE, listeMatiere):
    """
    la fonction construireListeDates construit une liste de dictionnaires avec les dates de 
    début et de fin de chaque matière contenu dans le dataframe

    Parameters
    ----------
    ADE : pandas.DataFrame
        le DataFrame contenant les données.
    listeMatiere : list
        la liste des matières dont on récupère les dates
        liste créer par la fonction getMatières(ADE)

    Returns
    -------
    listeDates : list
        la liste de dictionnaires représentant les dates de début et de fin pour chaque matière
    """
    listeDates = [] #on créer la liste qui va contenir les dictionnaires
    for matiere in listeMatiere: #pour chaque matière dans listeMatiere
        debut, fin = getDates(ADE, matiere) #on récupère les dates avec la fonction getDates
        dates_dict = {"Matière": matiere, "DateDébut": debut, "DateFin": fin} #on met la nom et les dates dans un dictionnaire 
        listeDates.append(dates_dict) #on ajoute le dictionnaire dans la liste
    return listeDates

def affichage(listeDates):
    """
    fonction qui gère l'affichage des résultats et des dictionnaires

    Parameters
    ----------
    listeDates : TYPE
        la liste contenant les dictionnaires avec les dates de début et de fin des matières

    Returns
    -------
    None.

    """
    for i in range(len(listeDates)):
        print(f" **** \n Matière: {listeDates[i]['Matière']} \n Date de début: {listeDates[i]['DateDébut']} \n Date de fin : {listeDates[i]['DateFin']} \n **** \n")



def main(nomTd):
    """
    fonction qui fait les appels de fonction et permet d'avoir le résultat final

    Parameters
    ----------
    nomTd : TYPE
        nom du TD dont on veut les dates de début et de fin

    Returns
    -------
    None.

    """
    ADE = transformTp(readCsv()) #on lit le csv en changeant les TP par les TD
    ADE = getTd(nomTd, ADE) #on garde les cours du TD demandé
    listeMatiere = getMatières(ADE) #on fait la liste des matières
    listeDates = construireListeDates(ADE, listeMatiere) #on construit la liste des dictionnaires avec les dates
    
    affichage(listeDates) #on affiche le tout  

#main("TDB")