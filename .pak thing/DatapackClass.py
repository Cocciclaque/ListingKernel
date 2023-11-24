import os
import sys

class Datapack():

    def __init__(self, filename, numFile, files_to_encode: list[str]):

        self.t = filename
        self.nf = len(files_to_encode)
        self.files_to_encode = files_to_encode
        self.positions = [0]*len(files_to_encode)
        self.sizes = []

    def makeheader(self):
        with open((str(self.t)+".pak"), "w") as f:
            name = self.encode_file(str(self.t), 32)
            f.write(name)

            nbfiles = self.encode_file(str(self.nf), 16)

            if len(nbfiles)>16:
                print("Error2 : FileAmount too long.")

            nbfiles = self.encode_file(self.nf, 16)
            f.write(nbfiles)

    def givebinary(self, text):
        return ''.join(format(i, '08b') for i in bytearray(str(text), encoding ='utf-8'))
    
    def makefile(self):
        self.makeheader()
        self.writefilesmetadata()
        self.set_positions()
        self.writefilescontents()

    def fill_text(self, text, length):
        texte = text
        if len(text)<length:
            texte = "0"*(length-len(text)) + text
        return texte

    def encode_file(self, text, length):
        return self.fill_text(self.givebinary(text), length)

    def writefilesmetadata(self):
        with open((str(self.t)+".pak"), "a") as f:
            f.seek(6*8)
            for i in range(len(self.files_to_encode)):
                filename = self.encode_file(self.files_to_encode[i], 320)
                if len(filename)>320:
                    print("Error2 : You tried to pack a file with a name too big.")
                f.write(filename)

                offset = self.encode_file(str(6+(i+1*48)), 32)
                f.write(offset)

                if len(offset)>32:
                    print("Error3 : file offset too high")
                size_file = self.encode_file(str(os.path.getsize(self.files_to_encode[i])), 32)

                if len(size_file)>32:
                    print("Error4 : File is too big !")

                f.write(size_file)




    def read_byte(self, file, byte):
        with open(file, "r") as f:
            f.seek(8*byte)
            data = f.read(8)
        return data
    
    def read_multiple_bytes(self, file, byte_start, byte_finish):
        data = ""
        with open(file, "r") as f:
            for i in range(byte_start, byte_finish+1):
                f.seek(8*(i))
                data += f.read(8) 
        return data        

    def read_header(self):
        return (".pak title is " + self.read_word(self.t+".pak", 0, 3) + ", amount of files is "  + self.read_word(self.t+".pak", 4, 5))
    
    def read_line_info(self, line):
        return (self.read_word(self.t+".pak", 6+(line*48), 45+(line*48)).replace('\x00', ""), self.read_word(self.t+".pak", 46+(line*48), 49+(line*48)).replace('\x00', ""), self.read_word(self.t+".pak", 50+(line*48), 53+(line*48)).replace('\x00', "")) 
    
    def read_lines(self):
        for i in range(len(self.files_to_encode)):
            # print(self.read_line_info(i))

    def read_word(self, file, byte_start, byte_finish):
        return str(self.bin_to_str(self.read_multiple_bytes(str(self.t)+".pak",byte_start, byte_finish)))
        

    def bin_to_str(self, textbin):
        my_int = my_int = int(textbin, base=2)
        my_str = my_int.to_bytes((my_int.bit_length() + 7)//8, 'big').decode()
        return my_str


    def set_positions(self):
        self.positions[0] = 6+(len(self.files_to_encode)*48)
        for i in range(1, len(self.files_to_encode)):
            self.positions[i] = self.positions[i-1]+os.path.getsize(self.files_to_encode[i-1])


    def writefilescontents(self):
        with open(self.t+".pak", "a") as f:
            for i in range(len(self.files_to_encode)):
                with open(self.files_to_encode[i], "r") as d:
                    f.seek(self.positions[i])
                    f.write(self.givebinary(d.read(int(self.read_line_info(i)[2]))))


    def read_contents(self):
        contents = []
        with open(self.t+".pak", "r") as f:
            for i in range(len(self.positions)):
                if i != len(self.positions)-1:
                    contents.append(self.read_word(self.t+".pak", self.positions[i], self.positions[i+1]-1))
                else:
                    contents.append(self.read_word(self.t+".pak", self.positions[i], len(f.read())))
        return contents
    
file = Datapack("MNS", 1, [r".pak thing\Sample.txt", r".pak thing\Sample2.txt", r".pak thing\Sample3.txt"])

file.makefile()



