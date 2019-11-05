import sys
import re

class Instruction:

    def __init__(self, label, name, args, address):
        self.label = label
        self.name = name
        self.args = args 
        self.address = address #Interpreter will assign addresses later

    def setLabel(self, label):
        return self.label

    def setName(self, name):
        return self.name

    def setArgs(self, args):
        return self.args

def read_file(file):
    instruction_list = []
    try:
        with open(file) as f:
            content = f.readlines()
            for line in content:
                if line.isspace():
                    continue
                input_list = re.split(',|\s+',line) 
                #Need to always put arguments in array regardless of one or two.
                args_array = []
                for i in range(2, len(input_list)): 
                    args_array.append(input_list[i])
                instruction_obj = Instruction(input_list[0], input_list[1], args_array, None) #instantiate an instruction object
                instruction_list.append(instruction_obj)
        return instruction_list
    except IOError:
        print('File not found')
        return
