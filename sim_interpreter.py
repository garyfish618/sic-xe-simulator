import parser
from memory import Memory, Registery

directives = ["RESW", "RESB", "BYTE", "WORD"]

class Interpreter:

    def __init__(self, instruction_array, memory, registers ):
        self.instructions = instruction_array
        self.is_simple = True
        self.instruction_pointer = 0
        self.memory_set = memory
        self.registers = registers

    def assign_address(self):
        next_address = "0000"
       

        for instruction in self.instructions:
            if instruction.name == "START":
                next_address = instruction.args[0]
                continue

            #If directive - Leave directive assignment to directives module
            if instruction.name in directives:
                if instruction.name == "BYTE":
                    value = ""
                    str = ""
                    if instruction.args[0][0] =='C':
                        str = instruction.args[0].split("'")[1]
                        for ch in str:
                            value = value + ascii2hex(ch)
                    else:
                        value = instruction.args[0].split("'")[1]
                    
                    if value % 2 != 0:
                        value = value.zfill(len(value) + 1)

                    for i in range(len(value),2):
                        byte_to_set = value[i] + value[i+1]
                        self.memory_set.set_memory(next_address, byte_to_set)
                        next_address = int2hex(hex2int(next_address, 16) + 1)

                        





            instruction.address = next_address

            print("DEBUG: " + "Instruction: " + instruction.name + " Address: " + instruction.address)

            if self.is_simple:
                # Convert to hex -> Strip 0x off front -> Capitalize all characters -> Fill with 0's so string is 4
                # characters

                next_address = hex(int(next_address, 16) + 3).strip("0x").upper().zfill(4)

    def execute_next_instruction(self):
        
        #Move past directive
        while self.instructions[self.instruction_pointer].name in directives:
            self.instruction_pointer += 1

        next_line = self.instructions[self.instruction_pointer]
        self.instruction_pointer += 1
        instruction_name = next_line.name
        label = next_line.label
        arguments = next_line.args

        instruction_token = self.determine_instruction(instruction_name)

        if instruction_token == -1:
            raise Exception("Invalid instruction name on line")  # TODO provide line number once implemented in parser

        self.token_utilizer(instruction_token, arguments, label)

    def determine_instruction(self, instruction_name):
        instruction_set = {}

        if (self.is_simple):
            instruction_set = {
                "ADD": 1,
                "AND":2,
                "COMP":3,
                "DIV":4,
                "J":5,
                "JEQ":6,
                "JGT":7,
                "JLT":8,
                "JSUB":9,
                "LDA":10,
                "LDCH":11,
                "LDL":12,
                "LDX":13,
                "MUL":14,
                "OR":15,
                "RD":16,
                "RSUB":17,
                "STA":18,
                "STCH":19,
                "STL":20,
                "STSW":21,
                "STX":22,
                "SUB":23,
                "TD":24,
                "TIX":25,
                "WD":26
            }

        else:
            instruction_set = {}

        return instruction_set.get(instruction_name, -1)  # Returns -1 if instruction was not found

    def token_utilizer(self, instruction_token, arguments, label):

        if (self.is_simple):

            if instruction_token == 1: #ADD
                print("Do ADD")

                instr_line = self.__getinstruction__(arguments[0])
                size_of_val = self.__determinesize__(instr_line)

                #ADD method if there is register X involved
                if arguments[1] == 'X':
                    value_of_X = self.registers.get_register('X')
                    address = add_hex(value_of_X, instr_line.address)
                    
                    memory_string = ""
                    for i in range(size_of_val):
                        memory_string = memory_string + self.memory_set.get_memory(address)

                    memory_string.zfill(6)
                    value_of_A = self.registers.get_register('A')
                    value_of_A = add_hex(value_of_A, memory_string)
                    self.registers.set_register('A', value_of_A)

                #ADDs if there is only A register
                else:
                    address = instr_line.address
                    memory_string = ""
                    for i in range(size_of_val):
                        memory_string = memory_string + self.memory_set.get_memory(address)

                    memory_string.zfill(6)
                    value_of_A = self.registers.get_register('A')
                    value_of_A = add_hex(memory_string, value_of_A)
                    self.registers.set_register('A', value_of_A)
        
            elif instruction_token == 2: #AND
                pass
            elif instruction_token == 3: #COMP
                pass
            elif instruction_token == 4: #DIV
                pass
            elif instruction_token == 5: #J
                pass
            elif instruction_token == 6: #JEQ
                pass
            elif instruction_token == 7: #JGT
                pass
            elif instruction_token == 8: #JLT
                pass
            elif instruction_token == 9: #JSUB
                pass

            elif instruction_token == 10: #LDA
                target_instr = self.__getinstruction__(arguments[0])
                size_of_val = self.__determinesize__(target_instr)

                value = ""
                for i in range(size_of_val):
                    address = target_instr.address
                    value = value + self.memory_set.get_memory(address)

                    
                value.zfill(6)
                self.registers.set_register('A', value)
                print(self.registers.get_register('A'))

            elif instruction_token == 11: #LDCH
                pass
            elif instruction_token == 12: #LDL
                pass
            elif instruction_token == 13: #LDX
                pass
            elif instruction_token == 14: #MUL
                pass
            elif instruction_token == 15: #OR
                pass
            elif instruction_token == 16: #RD
                pass
            elif instruction_token == 17: #RSUB
                pass
            elif instruction_token == 18: #STA
                pass
            elif instruction_token == 19: #STCH
                pass
            elif instruction_token == 20: #STL
                pass
            elif instruction_token == 21: #STSW
                pass
            elif instruction_token == 22: #STX
                pass
            elif instruction_token == 23: #SUB
                pass
            elif instruction_token == 24: #TD
                pass
            elif instruction_token == 25: #TIX
                pass
            elif instruction_token == 26: #WD
                pass
    def __getinstruction__(self, label):
        #Returns an instruction object given a label
        for instr in self.instructions:
            if instr.label == label:
                return instr

    def __determinesize__(self, instr):
        #Returns the amount of bytes a directive has allocated
        size = 0
        if instr.label == directives[0]:
            for i in range(int(instr.args[0])):
                size += 3
        
        elif instr.label == directives[1]:
            for i in range(int(instr.args[0])):
                size += 1
        
        elif instr.label == directives[2]:
            if instr.args[0][0] == 'C':
                char_array = instr.args[0].split("'")
                for ch in char_array:
                    size += 1
            else:
                size = 1

        elif instr.label == directives[3]:
            size = 3

        return size
                
        
#------Helper Methods------#


def hex2int(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val

def int2hex(number, bits):
    if number < 0:
        return hex((1 << bits) + number)[2:]
    else:
        return hex(number)[2:]

def ascii2hex(val):
    return hex(val)[2:]

def add_hex(x, y):
    return int2hex(hex2int(x, len(x) * 4) + hex2int(y, len(y) * 4))


def sub_hex(x, y):
    return int2hex(hex2int(x, len(x) * 4) - hex2int(y, len(y) * 4))
