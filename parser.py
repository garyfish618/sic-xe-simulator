import sys
import re
class Instruction:

    def __init__(self, label, name, args):
        self.label = label
        self.name = name
        self.args = args 

    #def __repr__(self): #allows printing a list of strings
       #return str(self.args)

    def setLabel(self, label):
        return self.label

    def setName(self, name):
        return self.name

    def setArgs(self, args):
        return self.args

def readfile(file):
    instruction_list = []
    try:
        with open(file) as f:
            content = f.readlines()
            for line in content:
                input_list = re.split(',|\s+',line) #splits at any white space and comma
                while("" in input_list) : #to remove weird space/possibly NULL terminator at end
                   input_list.remove("") 
                if len(input_list) == 4: #if the length is 4 create an args array
                    num_args = input_list[2:]
                else: 
                    num_args = input_list[2]
                instruction_obj = Instruction(input_list[0], input_list[1], num_args) #instantiate an instruction object
                instruction_list.append(instruction_obj)
        return instruction_list
    except IOError:
        print('File not found')
        sys.exit(1)

def Main():
    instruction_array = readfile("data.txt") #for now, just reads in a specific file
    #print(instruction_array)
#  Begin program
if __name__ == '__main__':
    Main()
