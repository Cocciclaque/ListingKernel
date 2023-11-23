import os
import binascii
from treeClass import Tree

directory1 = str(input("Quel répertoire dois-je utiliser comme origine ? "))
directory2 = str(input("Quel répertoire est une copie ?"))

root = Tree(directory1, 1, "", 0)

root.fill_children()

continueLoop = True

compareTree = Tree(directory2, 1, "", 0)
compareTree.fill_children()

print(root.detect_duplicates_between_two_dirs(root.store_files_sizes(), compareTree.store_files_sizes()))
print("sont en double, et à supprimer.")


