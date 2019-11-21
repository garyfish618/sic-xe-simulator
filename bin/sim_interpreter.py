import parser
from memory import Memory, Registery

directives = ["RESW", "RESB", "BYTE", "WORD","START"] # And END, however END is a special case
conditions = ["LT", "GT", "EQ"]

class Interpreter:

    def __init__(self, instruction_array, memory, registers ):
        self.instructions = instruction_array
        self.is_simple = True
        self.instruction_pointer = -1
        self.previous_pointer = -1
        self.memory_set = memory
        self.registers = registers
        self.next_address = "0000"
        self.condition_word = ""

    def assign_address(self):

        if self.instructions is None or len(self.instructions) == 0:
            print("Please load a file") 
            return
        
        self.instruction_pointer = 0

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

            elif self.determine_instruction(instruction.name) == -1:
                print("ERROR: Invalid instruction name on line " + str(instruction.line_num))
                print("Exiting interpreter")
                self.instruction_pointer = -1

                # Convert to hex -> Strip 0x off front -> Capitalize all characters -> Fill with 0's so string is 4
                # characters
            else:
                self.next_address = hex(int(self.next_address, 16) + 3).strip("0x").upper().zfill(4)

    def execute_next_instruction(self):
        if(self.instruction_pointer) == -1:
            print('No file loaded please parse then start')
            return


        if self.instructions[self.instruction_pointer].name == "END":
            print("End of file")
            self.instruction_pointer = -1
            return

        #Move past directive
        while self.instructions[self.instruction_pointer].name in directives:
            self.instruction_pointer += 1
            #If reaching end of instruction array and no return/jump instruction has been called, exit
            if(self.instruction_pointer == len(self.instructions)):
                print("End of file")
                self.instruction_pointer = -1
                return

        #Find next instruction and set PC to its address
        next_instruction_pointer = self.instruction_pointer + 1
        while ((next_instruction_pointer < len(self.instructions)) and (self.instructions[next_instruction_pointer].name in directives)):
            next_instruction_pointer += 1

        if(next_instruction_pointer < len(self.instructions)):
            self.registers.set_register('PC', self.instructions[next_instruction_pointer].address)
        

        instruction_line = self.instructions[self.instruction_pointer]
        self.instruction_pointer += 1
        instruction_name = instruction_line.name
        label = instruction_line.label
        arguments = instruction_line.args
        line_num = instruction_line.line_num

        print("Executing instruction: " + instruction_line.name)

        instruction_token = self.determine_instruction(instruction_name)
        self.token_utilizer(instruction_token, arguments, label, instruction_name, line_num)

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
                "WD":26,
                "END":27
            }

        else:
            instruction_set = {}

        return instruction_set.get(instruction_name, -1)  # Returns -1 if instruction was not found

    def token_utilizer(self, instruction_token, arguments, label, name, line_num):

        if (self.is_simple):

            if instruction_token == 1: #ADD

                instr_line = self.__getinstruction__(arguments[0])
                size_of_val = self.__determinesize__(instr_line)

                address = instr_line.address
                #If using indexed addressing mode
                if arguments[1] == 'X':
                    address = self.__getoffseaddress__(address)

                memory_string_hex = ""
                for i in range(size_of_val):
                    memory_string_hex = memory_string_hex + self.memory_set.get_memory(address)
                    address = add_hex(address, "0001").zfill(4)

                memory_string_int = hex2int(memory_string_hex)
                print(memory_string_int)
                value_of_A_hex = self.registers.get_register('A')
                value_of_A_int = hex2int(value_of_A_hex)
                value_of_A_int = memory_string_int + value_of_A_int
                self.registers.set_register('A', int2hex(value_of_A_int, 16).zfill(6))

        
            elif instruction_token == 2: #AND
                instr_line = self.__getinstruction__(arguments[0])
                size_of_val = self.__determinesize__(instr_line)
                address = instr_line.address

                if arguments[1] == 'X':
                    address = self.__getoffseaddress__(address)

                memory_string_hex = ""
                
                for i in range(size_of_val):
                    memory_string_hex = memory_string_hex + self.memory_set.get_memory(address)
                    address = add_hex(address, "0001").zfill(4)
                
                int_val_of_A = hex2int(self.registers.get_register('A'),16)
                int_val_of_mem = hex2int(memory_string_hex,16)
                
                result = int2hex(int_val_of_A & int_val_of_mem,16)
                self.registers.set_register('A', result)
                

            elif instruction_token == 3: #COMP
                size_of_val = self.__determinesize__(instr_line)                
                address = instr_line.address
                memory_string_hex = ""
                for i in range(size_of_val):
                    memory_string_hex = memory_string_hex + self.memory_set.get_memory(address)
                    address = add_hex(address, "0001").zfill(4)

                self.condition_word = conditions[comp(self.registers.get_register('A'), memory_string_hex)]
                

            elif instruction_token == 4: #DIV
                
                instr_line = self.__getinstruction__(arguments[0])
                size_of_val = self.__determinesize__(instr_line)
                address = instr_line.address

                #If using indexed addressing mode
                if arguments[1] == 'X':
                    address = self.__getoffseaddress__(address)

                memory_string_hex = ""
                for i in range(size_of_val):
                    memory_string_hex = memory_string_hex + self.memory_set.get_memory(address)
                    address = add_hex(address, "0001").zfill(4)
                    
                memory_string_int = hex2int(memory_string_hex, 16)
                value_of_A_hex = self.registers.get_register('A')
                value_of_A_int = hex2int(value_of_A_hex, 16)
                value_of_A_int = value_of_A_int / memory_string_int
                self.registers.set_register('A', int2hex(value_of_A_int, 16).zfill(6))

            elif instruction_token == 5: #J
                new_index = self.__getindex__(arguments[0])
                
                if new_index == -1:
                    print("ERROR: Illegal jump to label on line " + str(line_num))
                    print("Exiting interpreter")
                    self.instruction_pointer = -1
                    return

                self.instruction_pointer = new_index

                
            elif instruction_token == 6: #JEQ
                if self.condition_word == conditions[2]:
                    new_index = self.__getindex__(arguments[0])
                
                    if new_index == -1:
                        print("ERROR: Illegal jump to label on line " + str(line_num))
                        print("Exiting interpreter")
                        self.instruction_pointer = -1
                        return

                    
                    self.instruction_pointer = new_index


            elif instruction_token == 7: #JGT
                if self.condition_word == conditions[2]:
                    new_index = self.__getindex__(arguments[0])
                
                    if new_index == -1:
                        print("ERROR: Illegal jump to label on line " + str(line_num))
                        print("Exiting interpreter")
                        self.instruction_pointer = -1
                        return
                    self.instruction_pointer = new_index

            elif instruction_token == 8: #JLT
                if self.condition_word == conditions[2]:
                    new_index = self.__getindex__(arguments[0])
                
                    if new_index == -1:
                        print("ERROR: Illegal jump to label on line " + str(line_num))
                        print("Exiting interpreter")
                        self.instruction_pointer = -1
                        return

                    self.instruction_pointer = new_index

            elif instruction_token == 9: #JSUB
                new_index = self.__getindex__(arguments[0])
                self.registers.set_register('L', self.registers.get_register('PC'))
                self.registers.set_register('PC', self.__getinstruction__(arguments[0]).address)
                self.previous_pointer = self.instruction_pointer
                self.instruction_pointer = new_index

                if new_index == -1:
                        print("ERROR: Illegal jump to label on line " + str(line_num))
                        print("Exiting interpreter")
                        self.instruction_pointer = -1
                        return


            elif (instruction_token == 10 or instruction_token == 12 or instruction_token == 13 ): #LDA, LDX, LDL Instructions

                target_instr = self.__getinstruction__(arguments[0])
                size_of_val = self.__determinesize__(target_instr)
                address = target_instr.address
                value = ""

                #If using index based addressing
                if arguments[1] == 'X':
                    address = self.__getoffseaddress__(address)

                for i in range(size_of_val):
                    value = value + self.memory_set.get_memory(address)
                    address = int2hex(hex2int(address) + 1, 16)
                self.registers.set_register(name[2], value)

            elif instruction_token == 11: #LDCH
                target_instr = self.__getinstruction__(arguments[0])
                size_of_val = self.__determinesize__(target_instr)
                address = target_instr.address
                
                #If using index based addressing
                if arguments[1] == 'X':
                    address = self.__getoffseaddress__(address)

                value = self.memory_set.get_memory(address)
                self.registers.set_register('A', value)
                
            elif instruction_token == 14: #MUL
                instr_line = self.__getinstruction__(arguments[0])
                size_of_val = self.__determinesize__(instr_line)
                address = target_instr.address

                #If using index based addressing
                if arguments[1] == 'X':
                    address = self.__getoffseaddress__(address)

                memory_string_hex = ""
                for i in range(size_of_val):
                    memory_string_hex = memory_string_hex + self.memory_set.get_memory(address)
                    address = add_hex(address, "0001").zfill(4)

                memory_string_int = hex2int(memory_string_hex)
                value_of_A_hex = self.registers.get_register('A')
                value_of_A_int = hex2int(value_of_A_hex)
                value_of_A_int = memory_string_int * value_of_A_int
                self.registers.set_register('A', int2hex(value_of_A_int, 16).zfill(6))

            elif instruction_token == 15: #OR
                instr_line = self.__getinstruction__(arguments[0])
                size_of_val = self.__determinesize__(instr_line)
                address = instr_line.address

                if arguments[1] == 'X':
                    address = self.__getoffseaddress__(address)

                memory_string_hex = ""
                for i in range(size_of_val):
                    memory_string_hex = memory_string_hex + self.memory_set.get_memory(address)
                    address = add_hex(address, "0001").zfill(4)

                int_val_of_A = hex2int(self.registers.get_register('A'))
                int_val_of_mem = hex2int(memory_string_hex)

                result = int2hex(int_val_of_A | int_val_of_mem)
                self.registers.set_register('A', result) 

            elif instruction_token == 16: #RD
                instr_line = self.__getinstruction__(arguments[0])
                device_id = self.memory_set.get_memory(instr_line.address)
                print("Device " + device_id + " INPUT:" )
                print("Please enter in one byte of data (Hex) :")
                self.userin = input().upper()
                self.userin = self.userin[0:2]
                self.registers.set_register('A', self.userin)

            elif instruction_token == 17: #RSUB

                #PC = L
                self.registers.set_register('PC', self.registers.get_register('L'))

                if self.previous_pointer == -1:
                        print("ERROR: Illegal return on line " + str(line_num))
                        print("Exiting interpreter")
                        self.instruction_pointer = -1
                        return

                self.instruction_pointer = self.previous_pointer

            elif instruction_token == 18: #STA
                #M = A
                target_instr = self.__getinstruction__(arguments[0])
                value = self.registers.get_register('A')
                address = target_instr.address
                for byte in bytesplit(value):
                    self.memory_set.set_memory(address, byte)
                    address = int2hex(hex2int(address,16) + 1)
            elif instruction_token == 19: #STCH
                #M[RMB] = A[RMB]
                target_instr = self.__getinstruction__(arguments[0])
                address = target_instr.address
                aRMB = self.registers.get_register('A')[-2] + self.registers.get_register('A')[-1]
                self.memory_set.set_memory(address, aRMB)
            elif instruction_token == 20: #STL
                #M = L
                target_instr = self.__getinstruction__(arguments[0])
                value = self.registers.get_register('L')
                address = target_instr.address
                for byte in bytesplit(value):
                    self.memory_set.set_memory(address, byte)
                    address = int2hex(hex2int(address) + 1, 16)
            elif instruction_token == 21: #STSW
                pass
            elif instruction_token == 22: #STX
                #M = X
                target_instr = self.__getinstruction__(arguments[0])
                value = self.registers.get_register('X')
                address = target_instr.address
                for byte in bytesplit(value):
                    self.memory_set.set_memory(address, byte)
                    address = int2hex(hex2int(address) + 1, 16)
                pass
            elif instruction_token == 23: #SUB
                instr_line = self.__getinstruction__(arguments[0])
                size_of_val = self.__determinesize__(instr_line)
                address = target_instr.address

                #If using index based addressing
                if arguments[1] == 'X':
                    address = self.__getoffseaddress__(address)

                memory_string_hex = ""
                for i in range(size_of_val):
                    memory_string_hex = memory_string_hex + self.memory_set.get_memory(address)
                    address = add_hex(address, "0001").zfill(4)

                memory_string_int = hex2int(memory_string_hex)

                value_of_A_hex = self.registers.get_register('A')
                value_of_A_int = hex2int(value_of_A_hex)
                value_of_A_int = value_of_A_int - memory_string_int
                self.registers.set_register('A', int2hex(value_of_A_int, 16).zfill(6))
                    
            elif instruction_token == 24: #TD
                instr_line = self.__getinstruction__(arguments[0])
                device_id = self.memory_set.get_memory(instr_line.address)

                while(True):
                    print("Is device " + device_id + " ready? (y/n):")
                    decision = input().lower()

                    if decision == 'y':
                        self.condition_word = conditions[0]
                        break

                    elif decision == 'n':
                        self.condition_word = conditions[2]
                        break
                    
                    else:
                        print("Invalid decision")

            elif instruction_token == 25: #TIX
                instr_line = self.__getinstruction__(arguments[0])
                size_of_val = self.__determinesize__(instr_line)
                address = instr_line.address
                memory_string_hex = ""

                for i in range(size_of_val):
                    memory_string_hex = memory_string_hex + self.memory_set.get_memory(address)
                    address = add_hex(address, "0001").zfill(4)

                int_val_of_X = hext2int(self.registers.get_register('X'), 16)
                int_val_of_X += 1
                int_val_of_mem = hex2int(memory_string_hex)

                if (int_val_of_X < int_val_of_mem):
                    self.condition_word = conditions[1]
                elif (int_val_of_X > int_val_of_mem):
                    self.condition_word = conditions[2]
                else:
                    self.condition_word = conditions[3]
                    
            elif instruction_token == 26: #WD
                instr_line = self.__getinstruction__(arguments[0])
                device_id = self.memory_set.get_memory(instr_line.address)
                reg_A = self.registers.get_register("A")
                print("Device " + device_id + " OUTPUT:" + reg_A[-2:])
                
    def __getinstruction__(self, label):
        #Returns an instruction object given a label
        for instr in self.instructions:
            if instr.label == label:
                return instr
        raise Exception("ERROR: The label - '" + label + "' could not be resolved" )

    def __getoffseaddress__(self, start_address):
        #Returns an offset address when an instruction is using indexed addressing
        value_of_X = self.registers.get_register('X')
        address = add_hex(value_of_X, start_address.zfill(6)).zfill(4)
        return address
        

    def __getindex__(self, label):
        #Returns position of instruction in instruction array - useful for jump instructions
        for i in range(len(self.instructions)):
            if self.instructions[i].label == label:
                return i
        return -1

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
def hex2int(hexstr): 
    try:
        bits = len(hexstr) * 4
        value = int(hexstr,16)
        if value & (1 << (bits-1)):
            value -= 1 << bits
        return value
    except:
        return None

def int2hex(number, bits):
    try:
        if number < 0:
            return hex((1 << bits) + number)[2:]
        else:
            return hex(number)[2:].upper()
    except: 
        return None

def ascii2hex(val):
    return hex(ord(val))[2:].upper()

def add_hex(x, y):
    #Adds two hex numbers - NOTE both numbers must have same number of bits 
    size = 0
    if len(x) != len(y):
        raise Exception("Illegal add_hex")
    return int2hex(hex2int(x) + hex2int(y),len(x) * 4)

def sub_hex(x, y):
    size = 0
    if len(x) != len(y):
        raise Exception("Illegal sub_hex")

    return int2hex(hex2int(x) - hex2int(y),len(x) * 4)

def comp(x, y):
    x = hex2int(x)
    y = hex2int(y)
    if x == y:
        return 2
    elif x > y:
        return 1
    elif x < y :
        return 0
def bytesplit(hexString):
    data = hexString
    byteList = [data[i:i+2] for i in range(0, len(data), 2)]
    return byteList