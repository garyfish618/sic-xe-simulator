import sys
import re

class Instruction:

    def __init__(self, label, name, args, address, line_num):
        self.label = label
        self.name = name
        self.args = args 
        self.address = address #Interpreter will assign addresses later
        self.line_num = line_num

    def setLabel(self, label):
        return self.label

    def setName(self, name):
        return self.name

    def setArgs(self, args):
        return self.args


def read_file(file):
    instruction_list = []
    line_num = 0
    input_list = ''
    try:
        with open(file) as f:
            content = f.readlines()
            for line in content:
                args_array = []
                line_num += 1
                if line.isspace() or line[0] == '.':
                    continue
                if "C'" in line:
                    substring = line.split("'")[1]
                    input_list = re.split(",|\s+|'",line)
                    args_array.append(input_list[2])
                    args_array.append(substring)

                else:
                    input_list = re.split(",|\s+",line) #TODO Needs fix
                #|C'.+?'
    
                #Need to always put arguments in array regardless of one or two.
                    for i in range(2, len(input_list)): 
                        args_array.append(input_list[i])
                instruction_obj = Instruction(input_list[0], input_list[1], args_array, None, line_num) #instantiate an instruction object
                instruction_list.append(instruction_obj)
        return instruction_list
    except IOError:
        print('File not found')
        return
