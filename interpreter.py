import parser, memory


class Interpreter:

    def __init__(self, instruction_array, isSimple):
        self.instructions = instruction_array
        self.is_simple = isSimple
        self.instruction_pointer = 0
        self.memory_set = memory()

        self.assign_addresses(instruction_array)

    def assign_address(self, instruction_array):
        next_address = "0000"

        for instruction in instruction_array:
            if instruction.name == "START":
                next_address = instruction.args[0]
                instruction.address = next_address
            
            if is_simple:
                #Convert to hex -> Strip 0x off front -> Capitalize all characters -> Fill with 0's so string is 4 characters
                next_address = hex(int(next_address, 16) + 3).strip("0x").upper().zfill(4) 
                print(next_address)

    def execute_next_instruction(self):
        next_line = self.instructions[self.instruction_pointer]
        self.instruction_pointer += 1
        instruction_name = next_line.name
        label = next_line.label
        arguments = next_line.args

        instruction_token = determine_instruction(instruction_name)

        if instruction_token == -1: 
            raise Exception("Invalid instruction name on line") #TODO provide line number once implemented in parser

        token_utilizer(instruction_name, arguments, label)

    def determine_instruction(self, instruction_name):
        instruction_set = {}
         
        if (self.is_simple):
            instruction_set = {
                1: "ADD",
                2: "AND",
                3: "COMP",
                4: "DIV",
                5: "J",
                6: "JEQ",
                7: "JGT",
                8: "JLT",
                9: "JSUB",
                10: "LDA",
                11: "LDCH",
                12: "LDL",
                13: "LDX",
                14: "MUL",
                15: "OR",
                16: "RD",
                17: "RSUB",
                18: "STA",
                19: "STCH",
                20: "STL",
                21: "STSW",
                22: "STX",
                23: "SUB",
                24: "TD",
                25: "TIX",
                26: "WD"
            }

        else:
            instruction_set = {}

        return instruction_set.get(instruction_name, -1) #Returns -1 if instruction was not found
    
    #def token_utilizer(self, instruction_token, arguments, label):

        # if (self.isSimple):
        #     if instruction_token == 1: #ADD
        #         print("Do ADD")
            
        #     elif instruction_token == 2: #AND
                
        #     elif instruction_token == 3: #COMP
        #         #Do a SUB between m1 and m2
        #         #Store that value in register
        #         result = 

        #     elif instruction_token == 4: #DIV

        #     elif instruction_token == 5: #J

                

        #     elif instruction_token == 1: #ADD

        #     elif instruction_token == 1: #ADD

        #     elif instruction_token == 1: #ADD

        #     elif instruction_token == 1: #ADD
            
        #     elif instruction_token == 1: #ADD
            
        #     elif instruction_token == 1: #ADD


#Helper methods

def hex2int(val, bits):
    if (val & (1 << (bits - 1))) != 0: 
        val = val - (1 << bits)
    return val

def int2hex(number, bits):
    if number < 0:
        return hex((1 << bits) + number)[2:]
    else:
        return hex(number)[2:]             

def add_hex(x, y):
    return int2hex(hex2int(x, len(x) * 4) + hex2int(y, len(y) * 4))

def sub_hex(x, y):
    return int2hex(hex2int(x, len(x) * 4) - hex2int(y, len(y) * 4))


