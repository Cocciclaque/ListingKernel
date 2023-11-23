#SCHMITT Kilian - MNS, 16/11/2023, 16:05

import os
import binascii
from treeClass import Tree

directory = str(input("Quel répertoire dois-je analyser ? "))


root = Tree(directory, 1, "", 0) #some setup

root.fill_children()

root.show_hierarchy()

continueLoop = True

while continueLoop:

    what_to_do = str(input("Que dois-je faire ? ")).split(" ")

    if what_to_do[0] == "Fin" and len(what_to_do) == 1:
        continueLoop = False

    if what_to_do[0] == "Architecture" and len(what_to_do)==1:
        print(root.show_hierarchy())


    if what_to_do[0] == "Liste":
        if what_to_do[1] == "Totale" and len(what_to_do) == 2:
            print(root.total_list())
        elif what_to_do[1] == "Partielle" and len(what_to_do) == 3:
            print(root.partial_list(what_to_do[2]))
        elif len(what_to_do) == 2 and what_to_do[1].isalpha:
            print(root.show_one_file_extension_only("." + what_to_do[1]))

    if what_to_do[0] == "SaveListe" and len(what_to_do) == 2:
        with open(what_to_do[1], "w") as f:
            f.write(root.total_list())

    if what_to_do[0] == "SaveArchi" and len(what_to_do) == 2:
        with open(what_to_do[1], "w") as f:
            f.write(root.show_hierarchy())

    if what_to_do[0] == "Maxi" and len(what_to_do) == 2:
        print(root.show_maxi(int(what_to_do[1])))

    if what_to_do[0] == "Dupli" and len(what_to_do) == 2:
        if what_to_do[1] == "Show":
            for elt in root.detect_duplicates(root.store_files_sizes()):
                print(elt)
                print("\n")
                print("---------------------")
                print("\n")
    if what_to_do[0] == "Dupli" and what_to_do[1] == "Compare" and what_to_do[2] == "Delete" and len(what_to_do) == 3:

        ask_path = str(input("Quel est le chemin du dossier que vous souhaitez affiner ?"))

        compareTree = Tree(ask_path, 1, "", 0)
        compareTree.fill_children()

        print(root.detect_duplicates_between_two_dirs(root.store_files_sizes(), compareTree.store_files_sizes()))


