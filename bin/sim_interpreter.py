import parser, floats
from memory import Memory, Registery

directives = ["RESW", "RESB", "BYTE", "WORD","START"] # And END, however END is a special case
conditions = ["LT", "GT", "EQ"]

class Interpreter:

    def __init__(self, instruction_array, memory, registers, is_extended ):
        self.instructions = instruction_array
        self.is_extended = is_extended
        self.instruction_pointer = -1
        self.previous_pointer = -1
        self.memory_set = memory
        self.registers = registers
        self.next_address = "0000" if is_extended else "00000"
        self.condition_word = ""
        self.address_length = 4

    def assign_address(self):

        if self.instructions is None or len(self.instructions) == 0:
            print("Please load a file") 
            return
        
        self.instruction_pointer = 0

        for instruction in self.instructions:
            if instruction.name == "START":
                if (len(instruction.args[0]) != self.address_length):
                    raise Exception("Invalid address at line: " + str(instruction.line_num))
                self.next_address = instruction.args[0]
                continue
            if instruction.name == "END":
                continue

            instruction.address = self.next_address

            print("DEBUG: " + "Instruction: " + instruction.name + " Address: " + instruction.address)

            #If directive - Leave directive assignment to directives module
            if instruction.name in directives:

                if instruction.name == "BYTE":
                    stringname = ""
                    value = []
                    if instruction.args[0] == "C":
                        #TODO Logic doesnt look right here, need to test
                        stringname = instruction.args[1]
                        for i in range(len(stringname)):
                            value.append(ascii2hex(stringname[i]))
                    else:
                        value = instruction.args[0].split("X")[1].split("'")[1].split(' ')
                    
                    for item in value:
                        self.memory_set.set_memory(self.next_address, item)
                        self.next_address = add_hex(self.next_address, "1".zfill(self.address_length)).upper().zfill(self.address_length)

                elif instruction.name == "RESW":
                    value = 3 *  int (instruction.args[0])
                    self.next_address = add_hex(self.next_address, int2hex(value,16).zfill(self.address_length)).zfill(self.address_length)

                elif instruction.name == "RESB":
                    value = int (instruction.args[0])
                    self.next_address = add_hex(self.next_address, int2hex(value,16).zfill(self.address_length)).zfill(self.address_length)

                elif instruction.name == "WORD":

                    if float(instruction.args[0]).is_integer():
                        value = int2hex(int (instruction.args[0]), 16)
                        if (int(instruction.args[0]) < 0):
                            value = value.rjust(6, 'F')
                                
                        else:
                            value = value.zfill(6)

                        for i in range(0,6,2):
                            self.memory_set.set_memory(self.next_address, value[i] + value[i+1])
                            self.next_address = add_hex(self.next_address, "1".zfill(self.address_length)).upper().zfill(self.address_length)
                    else:
                        value = floats.float_to_hex(float(instruction.args[0])) 

                        for i in range(0,12,2):
                            self.memory_set.set_memory(self.next_address, value[i] + value[i+1])
                            self.next_address = add_hex(self.next_address, "1".zfill(self.address_length)).upper().zfill(self.address_length)

            elif self.determine_instruction(instruction.name) == -1:
                print("ERROR: Invalid instruction name on line " + str(instruction.line_num))
                print("Exiting interpreter")
                self.instruction_pointer = -1
                return

            elif instruction.name[0] == '+':
                self.next_address = add_hex(self.next_address, "4".zfill(self.address_length)).zfill(self.address_length)

            else:
                self.next_address = add_hex(self.next_address, "3".zfill(self.address_length)).zfill(self.address_length)

    def execute_next_instruction(self):
        if(self.instruction_pointer) == -1:
            print('No file loaded please parse then start')
            return False

        if self.instruction_pointer == len(self.instructions):
            print("End of file")
            self.instruction_pointer = -1
            return False

        if self.instructions[self.instruction_pointer].name == "END":
            print("End of file")
            self.instruction_pointer = -1
            return False

        #Move past directive
        while self.instructions[self.instruction_pointer].name in directives:
            self.instruction_pointer += 1
            #If reaching end of instruction array and no return/jump instruction has been called, exit
            if(self.instruction_pointer == len(self.instructions)):
                print("End of file")
                self.instruction_pointer = -1
                return False
        

        instruction_line = self.instructions[self.instruction_pointer]
        self.instruction_pointer += 1
        instruction_name = instruction_line.name
        label = instruction_line.label
        arguments = instruction_line.args
        line_num = instruction_line.line_num

        print("Executing instruction: " + instruction_line.name)

        instruction_token = self.determine_instruction(instruction_name)
        if instruction_token == 27 or instruction_token == 28 or instruction_token == 30 or instruction_token == 32 or instruction_token == 38 or instruction_token == 39 or instruction_token == 45 or instruction_token == 46:
            size_of_target = 0
            target_instruction = None
        elif len(arguments) != 0 and arguments[0][0] != "X" and arguments[0][0] != "#": #If not immediate
                if(arguments[0][0] == '@'):
                    target_instruction = self.__getinstruction__(arguments[0][1:])

                else:
                    target_instruction = self.__getinstruction__(arguments[0])

                #Size of value at target
                
                size_of_target = self.__determinesize__(target_instruction)
        else:
                target_instruction = None
                size_of_target = 0

        #Starting address of target data
        address = self.__resolveaddress__(None if target_instruction is None else target_instruction.address, arguments)

        self.token_utilizer(instruction_token, instruction_name, address, size_of_target, arguments, instruction_line.line_num)

        #Find next instruction and set PC to its address
        next_instruction_pointer = self.instruction_pointer + 1
        while ((next_instruction_pointer < len(self.instructions)) and (self.instructions[next_instruction_pointer].name in directives)):
            next_instruction_pointer += 1

        if(next_instruction_pointer < len(self.instructions)):
            self.registers.set_register('PC', self.instructions[next_instruction_pointer].address)

    def determine_instruction(self, instruction_name):
        if instruction_name[0] == '+':
            instr = instruction_name[1:]
        
        else:
            instr = instruction_name

        instruction_set = {}
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
            "STX":21,
            "SUB":22,
            "TD":23,
            "TIX":24,
            "WD":25,
            "ADDF":26,
            "ADDR":27,
            "CLEAR":28,
            "COMMPF":29,
            "COMPR":30,
            "DIVF":31,
            "DIVR":32,
            "LDB":33,
            "LDF":34,
            "LDS":35,
            "LDT":36,
            "MULF":37,
            "MULR":38,
            "RMO":39,
            "STB":40,
            "STF":41,
            "STS":42,
            "STT":43,
            "SUBF":44,
            "SUBR":45,
            "TIXR":46,
            "END":47
        }

        return instruction_set.get(instr, -1)  # Returns -1 if instruction was not found

        

    def token_utilizer(self, instruction_token, name, start_address, size_of_target, arguments, line_num):

        if start_address == -1:
            if arguments[0][0] == "#":
                val = arguments[0][1:]
                #if float(val).is_integer():
                    #hex_data = hex(val).lstrip("0x")
                    #if len(hex_data) % 2 != 0:
                        #hex_data.zfill(len(hex_data) + 1)
                #else:
                if "." in val:
                    hex_data = floats.float_to_hex(float(val))
                
                else:
                    hex_data = hex(int(val)).lstrip("0x").upper()
                    if len(hex_data) % 2 != 0:
                        hex_data.zfill(len(hex_data) + 1)
            else:
                hex_data = arguments[0][1:].split("'")[1]


        else:
            hex_data = self.__get_data__(start_address, size_of_target)

        if instruction_token == 1: #ADD
            memory_string_int = hex2int(hex_data)
            value_of_A_int = hex2int(self.registers.get_register('A'))
            value_of_A_int = memory_string_int + value_of_A_int

            new_hex = fill_value(value_of_A_int, int2hex(value_of_A_int, 16), size_of_target)
            self.registers.set_register('A', new_hex)

    
        elif instruction_token == 2: #AND
            int_val_of_A = hex2int(self.registers.get_register('A'))
            int_val_of_mem = hex2int(hex_data)
            int_val_of_A = int_val_of_A & int_val_of_mem

            new_hex = fill_value(int_val_of_A, int2hex(int_val_of_A, 16), size_of_target)
            self.registers.set_register('A', new_hex)

        elif instruction_token == 3: #COMP               
            memory_string_hex = hex_data
            self.condition_word = conditions[comp(self.registers.get_register('A'), memory_string_hex)]
            
        elif instruction_token == 4: #DIV       
            memory_string_int = hex2int(hex_data)
            value_of_A_int = hex2int(self.registers.get_register('A'))
            value_of_A_int = int(value_of_A_int / memory_string_int)
            new_hex = fill_value(value_of_A_int, int2hex(value_of_A_int, 16), size_of_target)
    

            self.registers.set_register('A', new_hex)


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
            if self.condition_word == conditions[1]:
                new_index = self.__getindex__(arguments[0])
            
                if new_index == -1:
                    print("ERROR: Illegal jump to label on line " + str(line_num))
                    print("Exiting interpreter")
                    self.instruction_pointer = -1
                    return
                self.instruction_pointer = new_index

        elif instruction_token == 8: #JLT
            if self.condition_word == conditions[0]:
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


        elif (instruction_token == 10 or instruction_token == 12 or instruction_token == 13 or instruction_token == 33\
           or instruction_token == 34 or instruction_token == 35 or instruction_token == 36):
            #LDA, LDX, LDL, LDB, LDF, LDS, LDT Instructions
            value = hex_data
            load_instructions = {10: 'A', 13: 'X', 12: 'L', 33:'B', 34: 'F', 35:'S', 36:'T'}
            self.registers.set_register(load_instructions.get(instruction_token), value)

        elif instruction_token == 11: #LDCH
            value = hex_data[0] + hex_data[1]
            self.registers.set_register('A', value)
            
        elif instruction_token == 14: #MUL
            memory_string_int = hex2int(self.__get_data__(start_address, size_of_target))
            value_of_A_int = hex2int(self.registers.get_register('A'))
            value_of_A_int = memory_string_int * value_of_A_int
            new_hex = fill_value(value_of_A_int, int2hex(value_of_A_int, 16), size_of_target)
            
            self.registers.set_register('A', new_hex)

        elif instruction_token == 15: #OR
            int_val_of_A = hex2int(self.registers.get_register('A'))
            int_val_of_mem = hex2int(self.__get_data__(start_address, size_of_target))
            int_val_of_A = int_val_of_A | int_val_of_mem
            new_hex = fill_value(int_val_of_A, int2hex(int_val_of_A, 16), size_of_target)

            self.registers.set_register('A', new_hex)

        elif instruction_token == 16: #RD
            if (self.condition_word != "LT"):
                return
            device_id = self.memory_set.get_memory(start_address)
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

        elif instruction_token == 18 or instruction_token == 20 or instruction_token == 21 \
            or instruction_token == 40 or instruction_token == 41 or instruction_token == 42 or instruction_token == 43:
            #STA, STL, STX, STB, STT, STT, STF
            #M = Register
            value = self.registers.get_register(name[2])
            address = start_address
            for byte in bytesplit(value):
                self.memory_set.set_memory(address, byte)
                address = int2hex(hex2int(address) + 1, 16).zfill(4)

        elif instruction_token == 19: #STCH
            #M[RMB] = A[RMB]
            aRMB = self.registers.get_register('A')[-2] + self.registers.get_register('A')[-1]
            self.memory_set.set_memory(start_address, aRMB)

        elif instruction_token == 22: #SUB
            memory_string_int = hex2int( self.__get_data__(start_address, size_of_target))
            value_of_A_int = hex2int(self.registers.get_register('A'))
            value_of_A_int = value_of_A_int - memory_string_int
            new_hex = fill_value(value_of_A_int, int2hex(value_of_A_int, 16), size_of_target)

            self.registers.set_register('A', new_hex)

        elif instruction_token == 23: #TD
            device_id = self.memory_set.get_memory(start_address)
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

        elif instruction_token == 24: #TIX
            int_val_of_X = hex2int(self.registers.get_register('X'))
            int_val_of_X += 1 
            int_val_of_mem = hex2int(self.__get_data__(start_address, size_of_target))

            if (int_val_of_X < int_val_of_mem):
                self.condition_word = conditions[0]
                val_X = int2hex(int_val_of_X, 16)
                self.registers.set_register('X', val_X)
            elif (int_val_of_X > int_val_of_mem):
                self.condition_word = conditions[1]
                val_X = int2hex(int_val_of_X, 16)
                self.registers.set_register('X', val_X)
            else:
                self.condition_word = conditions[2]
                val_X = int2hex(int_val_of_X, 16)
                self.registers.set_register('X', val_X)
                
        elif instruction_token == 25: #WD
            if (self.condition_word != "LT"):
                return

            device_id = self.memory_set.get_memory(start_address)
            reg_A = self.registers.get_register("A")
            print("Device " + device_id + " OUTPUT:" + reg_A[-2:])

        elif instruction_token == 26: #ADDF
            float_in_F = floats.hex_to_float(self.registers.get_register('F'))
            float_val = floats.hex_to_float(hex_data)

            result = float_in_F + float_val

            self.registers.set_register('F',floats.float_to_hex(result))

        elif instruction_token == 27: #ADDR
            reg_1_val = hex2int(self.registers.get_register(arguments[0]))
            reg_2_val = hex2int(self.registers.get_register(arguments[1]))
            reg_2_val = reg_1_val + reg_2_val
            new_hex = fill_value(reg_2_val, int2hex(reg_2_val, 16), 3)
            self.registers.set_register(arguments[1],new_hex)
        elif instruction_token == 28: #CLEAR
            if arguments[0] == "F":
                #Float register is 48 bits 
                self.registers.set_register('F', "000000000000")
            else:
                self.registers.set_register(arguments[0], "000000")
        elif instruction_token == 29: #COMPF
            pass
        elif instruction_token == 30: #COMPR
            self.condition_word = conditions[comp(self.registers.get_register(arguments[0]), self.registers.get_register(arguments[1]))]
            
        elif instruction_token == 31: #DIVF
            float_in_F = floats.hex_to_float(self.registers.get_register('F'))
            float_val = floats.hex_to_float(hex_data)

            result = float_in_F / float_val

            self.registers.set_register('F',floats.float_to_hex(result))

    
        elif instruction_token == 32: #DIVR
            reg_1_val = hex2int(self.registers.get_register(arguments[0]))
            reg_2_val = hex2int(self.registers.get_register(arguments[1]))
            reg_2_val = int(reg_2_val / reg_1_val)
            new_hex = fill_value(reg_2_val, int2hex(reg_2_val, 16), 3)
            self.registers.set_register(arguments[1],new_hex)
        elif instruction_token == 37: #MULF
            float_in_F = floats.hex_to_float(self.registers.get_register('F'))
            float_val = floats.hex_to_float(hex_data)

            result = float_in_F * float_val

            self.registers.set_register('F',floats.float_to_hex(result))
        elif instruction_token == 38: #MULR
            reg_1_val = hex2int(self.registers.get_register(arguments[0]))
            reg_2_val = hex2int(self.registers.get_register(arguments[1]))
            reg_2_val = reg_1_val * reg_2_val
            new_hex = fill_value(reg_2_val, int2hex(reg_2_val, 16), 3)
            self.registers.set_register(arguments[1],new_hex)
        elif instruction_token == 39: #RMO
            reg_val = self.registers.get_register(arguments[0])
            self.registers.set_register(arguments[1],reg_val)
        elif instruction_token == 40: #STB
            pass
        elif instruction_token == 44: #SUBF
            float_in_F = floats.hex_to_float(self.registers.get_register('F'))
            float_val = floats.hex_to_float(hex_data)

            result = float_in_F - float_val

            self.registers.set_register('F',floats.float_to_hex(result))

        elif instruction_token == 45: #SUBR
           r2 = self.registers.get_register(arguments[1])
           r1 = self.registers.get_register(arguments[0])
           self.registers.set_register(arguments[1], sub_hex(r2, r1))
        elif instruction_token == 46: #TIXR
            int_val_of_X = hex2int(self.registers.get_register('X'))
            int_val_of_X += 1 
            new_hex = fill_value(int_val_of_X, int2hex(int_val_of_X, 16), 3)
            self.registers.set_register('X', new_hex)
            self.condition_word = conditions[comp(self.registers.get_register('X'), self.registers.get_register(arguments[0]))]


        

    def __getinstruction__(self, label):
        #Returns an instruction object given a label
        for instr in self.instructions:
            if instr.label == label:
                return instr
        raise Exception("ERROR: The label - '" + label + "' could not be resolved" )

    def __resolveaddress__(self, start_address, arguments):
        #Indexed addressing
        if(len(arguments) == 2 and arguments[1] == 'X'):
            value_of_X = self.registers.get_register('X')
            address = add_hex(value_of_X, start_address.zfill(6)).zfill(4)
            return address

        #Immediate Operand
        if(len(arguments) != 0 and arguments[0][0] == '#'):
            return -1 # Indicates no address - use immediate operand
        
        #Indirect Addressing
        if(len(arguments) != 0 and arguments[0][0] == '@'):
            instruction = self.__getinstruction__(arguments[0][1:])
            address = self.memory_set.get_memory(instruction.address) + self.memory_set.get_memory(add_hex(instruction.address, "1".zfill(self.address_length)))
            return address

        return start_address

    def __getindex__(self, label):
        #Returns position of instruction in instruction array - useful for jump instructions
        for i in range(len(self.instructions)):
            if self.instructions[i].label == label:
                return i
        return -1

    def __determinesize__(self, instr):
        #Returns the amount of bytes a directive has allocated
        size = 0

        if instr.name == directives[0] or instr.name == directives[3]:
            size = 3
        
        elif instr.name == directives[1] or instr.name == directives[2]:
            size = 1

        return size

    #Gets values in memory given a range (size)
    def __get_data__(self, start_address, size):
        address = start_address
        memory_string_hex = ""
        for i in range(size):
            memory_string_hex = memory_string_hex + self.memory_set.get_memory(address)
            address = add_hex(address, "1".zfill(self.address_length)).zfill(4)
        
        return memory_string_hex
        
                
        
#------Helper Methods------#

def fill_value(value, hex_value, size):
    new_hex = hex_value
    if(value >= 0):
        new_hex = new_hex.zfill(size * 2)

    else:
        new_hex = new_hex.rjust(size * 2, 'F')

    return new_hex

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
            return hex((1 << bits) + number)[2:].upper()
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

