import parser
from memory import Memory, Registery

directives = ["RESW", "RESB", "BYTE", "WORD","START"]

class Interpreter:

    def __init__(self, instruction_array, memory, registers ):
        self.instructions = instruction_array
        self.is_simple = True
        self.instruction_pointer = 0
        self.memory_set = memory
        self.registers = registers
        self.next_address = "0000"

    def assign_address(self):
       

        for instruction in self.instructions:
            if instruction.name == "START":
                self.next_address = instruction.args[0]
                continue

            instruction.address = self.next_address

            print("DEBUG: " + "Instruction: " + instruction.name + " Address: " + instruction.address)

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
                    
                    if len(value) % 2 != 0:
                        value = value.zfill(len(value) + 1)

                    for i in range(0,len(value),2):
                        byte_to_set = value[i] + value[i+1]
                        self.memory_set.set_memory(self.next_address, byte_to_set)
                        self.next_address = add_hex(self.next_address, "0001").upper().zfill(4)

                elif instruction.name == "RESW":
                    value = 3 *  int (instruction.args[0])
                    self.next_address = add_hex(self.next_address, int2hex(value,16).zfill(4)).zfill(4)

                elif instruction.name == "RESB":
                    value = int (instruction.args[0])
                    self.next_address = add_hex(self.next_address, int2hex(value,16).zfill(4)).zfill(4)

                elif instruction.name == "WORD":
                    value = int2hex(int (instruction.args[0]), 16)
                    value = value.zfill(6)
                    for i in range(0,6,2):
                        self.memory_set.set_memory(self.next_address, value[i] + value[i+1])
                        self.next_address = add_hex(self.next_address, "0001").upper().zfill(4)

            else:
                # Convert to hex -> Strip 0x off front -> Capitalize all characters -> Fill with 0's so string is 4
                # characters

                self.next_address = hex(int(self.next_address, 16) + 3).strip("0x").upper().zfill(4)

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

        self.token_utilizer(instruction_token, arguments, label, instruction_name)

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

    def token_utilizer(self, instruction_token, arguments, label, name):

        if (self.is_simple):

            if instruction_token == 1: #ADD

                instr_line = self.__getinstruction__(arguments[0])
                size_of_val = self.__determinesize__(instr_line)

                #ADD method if there is register X involved
                if arguments[1] == 'X':
                    value_of_X = self.registers.get_register('X')
                    address = add_hex(value_of_X, instr_line.address.zfill(6)).zfill(4)

                    memory_string_hex = ""
                    for i in range(size_of_val):
                        memory_string_hex = memory_string_hex + self.memory_set.get_memory(address)
                        address = add_hex(address, "0001").zfill(4)

                    memory_string_int = hex2int(memory_string_hex, 16)

                    value_of_A_hex = self.registers.get_register('A')
                    value_of_A_int = hex2int(value_of_A_hex, 16)
                    value_of_A_int = memory_string_int + value_of_A_int
                    self.registers.set_register('A', int2hex(value_of_A_int, 16).zfill(6))

                #ADDs if there is only A register
                else:
                    address = instr_line.address
                    memory_string_hex = ""
                    for i in range(size_of_val):
                        memory_string_hex = memory_string_hex + self.memory_set.get_memory(address)
                        address = add_hex(address, "0001").zfill(4)
                        
                    memory_string_int = hex2int(memory_string_hex, 16)
                    
                    value_of_A_hex = self.registers.get_register('A')
                    value_of_A_int = hex2int(value_of_A_hex, 16)
                    value_of_A_int = memory_string_int + value_of_A_int
                    self.registers.set_register('A', int2hex(value_of_A_int, 16).zfill(6))
        
            elif instruction_token == 2: #AND
                pass
            elif instruction_token == 3: #COMP
                pass
            elif instruction_token == 4: #DIV
                
                instr_line = self.__getinstruction__(arguments[0])
                size_of_val = self.__determinesize__(instr_line)
                #DIV method if there is register X involved
                if arguments[1] == 'X':
                    value_of_X = self.registers.get_register('X')
                    address = add_hex(value_of_X, instr_line.address.zfill(6)).zfill(4)

                    memory_string_hex = ""
                    for i in range(size_of_val):
                        memory_string_hex = memory_string_hex + self.memory_set.get_memory(address)
                        address = add_hex(address, "0001").zfill(4)

                    memory_string_int = hex2int(memory_string_hex, 16)

                    value_of_A_hex = self.registers.get_register('A')
                    value_of_A_int = hex2int(value_of_A_hex, 16)
                    value_of_A_int = int(value_of_A_int / memory_string_int)
                    self.registers.set_register('A', int2hex(value_of_A_int, 16).zfill(6))

                #DIVs if there is only A register
                else:
                    address = instr_line.address
                    memory_string_hex = ""
                    for i in range(size_of_val):
                        memory_string_hex = memory_string_hex + self.memory_set.get_memory(address)
                        address = add_hex(address, "0001").zfill(4)
                        
                    memory_string_int = hex2int(memory_string_hex, 16)
                    
                    value_of_A_hex = self.registers.get_register('A')
                    value_of_A_int = hex2int(value_of_A_hex, 16)
                    value_of_A_int = int(value_of_A_int / memory_string_int)
                    self.registers.set_register('A', int2hex(value_of_A_int, 16).zfill(6))
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

            elif (instruction_token == 10 or instruction_token == 12 or instruction_token == 13 ): #LDA, LDX, LDL Instructions
                target_instr = self.__getinstruction__(arguments[0])
                size_of_val = self.__determinesize__(target_instr)
                value = ""
                address = target_instr.address
                
                for i in range(size_of_val):
                    value = value + self.memory_set.get_memory(address)
                    address = int2hex(hex2int(address,16) + 1, 16)
                self.registers.set_register(name[2], value)

            elif instruction_token == 11: #LDCH
                target_instr = self.__getinstruction__(arguments[0])
                size_of_val = self.__determinesize__(instr_line)
                value = "" 
                
                #LDCH method if there is register X involved
                if arguments[1] == 'X':
                    value_of_X = self.registers.get_register('X')
                    address = add_hex(value_of_X, instr_line.address.zfill(6)).zfill(4)

                    value = value + self.memory_set.get_memory(address)
                    address = int2hex(hex2int(address,16) + 1, 16)
                    self.registers.set_register(name[2], value)

                #LDCH if only A register
                else:
                    address = target_instr.address
                    value = value + self.memory_set.get_memory(address)
                    address = int2hex(hex2int(address,16) + 1, 16)
                    self.registers.set_register(name[2], value)
                
            elif instruction_token == 14: #MUL
                instr_line = self.__getinstruction__(arguments[0])
                size_of_val = self.__determinesize__(instr_line)

                #MUL method if there is register X involved
                if arguments[1] == 'X':
                    value_of_X = self.registers.get_register('X')
                    address = add_hex(value_of_X, instr_line.address.zfill(6)).zfill(4)

                    memory_string_hex = ""
                    for i in range(size_of_val):
                        memory_string_hex = memory_string_hex + self.memory_set.get_memory(address)
                        address = add_hex(address, "0001").zfill(4)

                    memory_string_int = hex2int(memory_string_hex, 16)

                    value_of_A_hex = self.registers.get_register('A')
                    value_of_A_int = hex2int(value_of_A_hex, 16)
                    value_of_A_int = memory_string_int * value_of_A_int
                    self.registers.set_register('A', int2hex(value_of_A_int, 16).zfill(6))

                #MULs if there is only A register
                else:
                    address = instr_line.address
                    memory_string_hex = ""
                    for i in range(size_of_val):
                        memory_string_hex = memory_string_hex + self.memory_set.get_memory(address)
                        address = add_hex(address, "0001").zfill(4)
                        
                    memory_string_int = hex2int(memory_string_hex, 16)
                    
                    value_of_A_hex = self.registers.get_register('A')
                    value_of_A_int = hex2int(value_of_A_hex, 16)
                    value_of_A_int = memory_string_int * value_of_A_int
                    self.registers.set_register('A', int2hex(value_of_A_int, 16).zfill(6))

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
                instr_line = self.__getinstruction__(arguments[0])
                size_of_val = self.__determinesize__(instr_line)

                #SUB method if there is register X involved
                if arguments[1] == 'X':
                    value_of_X = self.registers.get_register('X')
                    address = add_hex(value_of_X, instr_line.address.zfill(6)).zfill(4)

                    memory_string_hex = ""
                    for i in range(size_of_val):
                        memory_string_hex = memory_string_hex + self.memory_set.get_memory(address)
                        address = add_hex(address, "0001").zfill(4)

                    memory_string_int = hex2int(memory_string_hex, 16)

                    value_of_A_hex = self.registers.get_register('A')
                    value_of_A_int = hex2int(value_of_A_hex, 16)
                    value_of_A_int = value_of_A_int - memory_string_int
                    self.registers.set_register('A', int2hex(value_of_A_int, 16).zfill(6))

                #SUBs if there is only A register
                else:
                    address = instr_line.address
                    memory_string_hex = ""
                    for i in range(size_of_val):
                        memory_string_hex = memory_string_hex + self.memory_set.get_memory(address)
                        address = add_hex(address, "0001").zfill(4)
                        
                    memory_string_int = hex2int(memory_string_hex, 16)
                    
                    value_of_A_hex = self.registers.get_register('A')
                    value_of_A_int = hex2int(value_of_A_hex, 16)
                    value_of_A_int = value_of_A_int - memory_string_int
                    self.registers.set_register('A', int2hex(value_of_A_int, 16).zfill(6))
                    
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
        if instr.name == directives[0]:
            for i in range(int(instr.args[0])):
                size += 3
        
        elif instr.name == directives[1]:
            for i in range(int(instr.args[0])):
                size += 1
        
        elif instr.name == directives[2]:
            if instr.args[0][0] == 'C':
                char_array = instr.args[0].split("'")
                for ch in char_array:
                    size += 1
            else:
                size = 1
            

        elif instr.name == directives[3]:
            size = 3

        return size
                
        
#------Helper Methods------#


    
#converts from hex to 2's comp signed int
def hex2int(hexstr,bits): 
    value = int(hexstr,16)
    if value & (1 << (bits-1)):
        value -= 1 << bits
    return value

def int2hex(number, bits):
    if number < 0:
        return hex((1 << bits) + number)[2:].upper()
    else:
        return hex(number)[2:].upper()

def ascii2hex(val):
    return hex(val)[2:]

def add_hex(x, y):
    #Adds two hex numbers - NOTE both numbers must have same number of bits 
    size = 0
    if len(x) != len(y):
        raise Exception("Illegal add_hex")
    return int2hex(hex2int(x, len(x) * 4) + hex2int(y, len(y) * 4),len(x) * 4)
