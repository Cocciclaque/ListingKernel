#SCHMITT Kilian - MNS, 16/11/2023, 16:05

import os
import binascii

class Tree:
    def __init__(self, path: str, depth: int, name: str, crc32: str):
        """
        Tree Class :
            a Tree node used for os exploration. Contains other Tree nodes.

        Attributes:
            path(str) : The path of the Tree node.
            
            depth(int) : The depth of the Tree node. 
            Is used to know how deep into the root directory exploration we are.

            name(str) : The name of the Tree node. Is used for clean displaying of the node's architecture.
        
        """
        self.name = name
        self.depth = depth
        self.path = path
        self.children = []
        self.print = crc32

    def show_hierarchy(self)-> str:
        """
        show_hierarchy method:
            returns the architecture of a directory at the node's path.
        """
        return_list = ""
        for elt in self.children:
            str_construct = ""
            for i in range(elt.depth-1):
                str_construct += "   "
            if os.path.isdir(elt.path):
                str_construct += ">>>"
            str_construct += (elt.name + "\n")
            return_list += str_construct
            return_list += elt.show_hierarchy()
        return return_list
    
    def show_one_file_extension_only(self, e: str)-> str:
        """
        show_one_file_extension_only method:
            returns the architecture of a directory at the node's path. Ignores every file except files with precised extension.

            Can call method without addind a . before the extension

        Parameters:
            e(str) : The extension of the only files getting displayed. Don't write a . before.
        
        """
        return_list = ""
        for elt in self.children:
            str_construct = ""
            if os.path.splitext(elt.path)[1] == e or os.path.isdir(elt.path):
                for i in range(elt.depth-1):
                    str_construct += "   "
                    if os.path.isdir(elt.path):
                        str_construct += ">>>"
                str_construct += (elt.name + "\n")
                return_list += str_construct
            return_list += elt.show_one_file_extension_only(e)
        return return_list

    def is_empty(self)-> bool:
        """
        is_empty method:
            Returns True if the node is empty, and Flase if the node has children.
        """
        if len(self.children) == 0:
            return True
        return False

    def add_children(self):
        """
        add_children method:
            Adds the content of a directory at path into the children attribute.
        """
        try: 
            list_children = os.listdir(self.path)
            for i in range(len(list_children)):
                self.children.append(Tree(self.path + "/" + list_children[i], self.depth + 1, list_children[i], "0"))

        except:
            pass
    
    def CRC32_from_file(self, filename):
        buf = open(filename,'rb').read()
        buf = (binascii.crc32(buf) & 0xFFFFFFFF)
        return "%08X" % buf

    def fill_children(self):
        """
        fill_children method:
            Recursive method that fills the whole directory tree, adding the content of everything inside of path.
        """
        self.add_children()
        for elt in self.children:
            if os.path.isdir(elt.path):
                elt.fill_children()

    def total_list(self)-> list[str]:
        """
        total_list method:
            returns the list of all directories and their contents at path in alphabetical order.
        """
        return_list = ""
        if self.children != []:
            if os.path.isdir(self.path):
                return_list += (self.name + "\n")
            return_list += (str(self.show_sort_directory_alphabetically()) + "\n")
            return_list += ("-----\n")
        for elt in self.children:
            return_list += elt.total_list()
        return return_list

    def partial_list(self, r: int)-> list[str]:
        """
        partial_list method:
            returns the list of the biggest r elements (in file size) in directories at path.
        """
        return_list = ""
        if self.children != []:
            if os.path.isdir(self.path):
                return_list += (self.name + "\n")    
            return_list += (str(self.show_sort_directory_by_size()[:int(r)]) + "\n")
            return_list += ("-----\n")
        for elt in self.children:
            return_list += elt.partial_list(r)
        return return_list
            
    def show_sort_directory_by_size(self)-> list[str]:
        """
        show_sort_directory_by_size method :
            returns the list of all directories and their contents at path sorted by file size.
        """
        size_list = []
        sorted_list = []
        for i in range(len(self.children)):
            size_list.append((os.path.getsize(self.children[i].path), self.children[i].path))
        size_list.sort(key = lambda x: x[0])
        for elt in size_list:
            sorted_list.append(elt[1])
        return sorted_list
        
    def show_maxi(self, m: int)-> str:
        """
        show_maxi method :
            returns the architecture of the directory at path for every file bigger than m (in byte).
        
        Parameters:
            m(int) : The byte value representing the minimum size for a file to be saved in the string.
        """
        return_list = ""
        for elt in self.children:
            str_construct = ""
            if os.path.isdir(elt.path) or os.path.getsize(elt.path) >= m:
                for i in range(elt.depth-1):
                    str_construct += "   "
                if os.path.isdir(elt.path):
                    str_construct += ">>>"
                str_construct += (elt.name + "\n")
                return_list += str_construct
            return_list += elt.show_maxi(m)
        return return_list

    def show_sort_directory_alphabetically(self)-> list[str]:
        """
        show_sort_directory_alphabetically method:
            sorts a list of directories and files alphabetically and returns the list.
        """
        sorted_list = []
        for elt in self.children:
            sorted_list.append(elt.name)
        sorted_list.sort(key=str.lower)
        return sorted_list
    
    def store_files_sizes(self)-> list[(str, int)]:
        """
        store_files_sizes method:
            returns a list of tuples (str(path of file), int(size of tile))
        """
        store_list = []
        for elt in self.children:
            if os.path.isdir(elt.path) == False:
                store_list.append((elt.path, os.path.getsize(elt.path)))
            elif os.path.isdir(elt.path) == True:
                store_list.append(elt.store_files())
        return store_list

    def detect_duplicates(self, sizes_tuples: list)-> list[str]:
        """
        detect_duplicates method:
            returns the list of duplicate files in sizes_list, if any.
        """
        duplicate_list = []
        return_list = []
        for i in range(len(sizes_tuples)-1):
            mine = sizes_tuples[i][1]
            for j in range(len(sizes_tuples)):
                if i!=j and sizes_tuples[i][1] == sizes_tuples[j][1]:
                    duplicate_list.append((sizes_tuples[i][0], sizes_tuples[j][0]))
                    


        for elt in duplicate_list:
            with open(elt[0], 'rb') as f1:
                with open(elt[1], 'rb') as f2:
                    if f1.read(3) == f2.read(3):
                        if self.CRC32_from_file(elt[0]) == self.CRC32_from_file(elt[1]):
                            return_list.append((elt[0] + " et " + elt[1] + " sont des duplicatas"))
        
        return return_list

    def detect_duplicates_between_two_dirs(self, sizes_tuples_dir_one: list, sizes_tuples_dir_two: list)-> list[str]:
        """
        detect_duplicates_between_two_dirs method:
            returns duplicate files between two directories.
        """
        duplicate_list = []
        return_list = []
        for i in range(len(sizes_tuples_dir_one)-1):
            for j in range(len(sizes_tuples_dir_two)):
                if i!=j and sizes_tuples_dir_one[i][1] == sizes_tuples_dir_two[j][1]:
                    duplicate_list.append((sizes_tuples_dir_one[i][0], sizes_tuples_dir_two[j][0]))



        for elt in duplicate_list:
            with open(elt[0], 'rb') as f1:
                with open(elt[1], 'rb') as f2:
                    if f1.read(3) == f2.read(3):
                        if self.CRC32_from_file(elt[0]) == self.CRC32_from_file(elt[1]):
                            if elt[1] not in return_list:
                                return_list.append(elt[1])

        return return_list



