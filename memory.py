class Memory: 
    # isSimple = True    #False = SIC/XE
    def __init__(self, isSimple):
        self.isSimple = isSimple
        if isSimple:
            self.memory = [None] * 4000      #size in bytes
            for i in range(4000):
                self.memory[i] = "00"
        else:
            self.memory = [None] * 128000    #size in bytes
            for i in range(128000):
                self.memory[i] = "00"

    def get_memory(self, address):
        dec = hex2int(address,16)

        if self.isSimple:
            if dec < 0 or dec > 4000:
                return False
            return self.memory[dec]

    def set_memory(self, address, byte):
        dec = hex2int(address, 16)
        if self.isSimple:
            if dec < 0 or dec > 4000:
                return False
        else:
            if dec < 0 or dec > 128000:
                return False
        
        self.memory[dec] = byte
        return  True

    def print_mem_line(self,address):
        #Prints a line of 10 bytes in memory from a specified address
        output = address + ":\t"
        index = hex2int(address, 16)

        for i in range(10):
            output = output + self.memory[index]

        print(output)          

    def dump_memory(self):
        output = []
        for byte in self.memory:
            output.append(byte)
            if len(output) % 16 == 0: #print memory in groups of 8 bytes
                print(output)
                output = []
        if len(output) > 0:
            print(output)

class Registery:
    def __init__(self, isSimple):
        if isSimple:
            #5 registers 24 bits in length 
            self.registers = {  
                'A' : "000000",    #Accumulator
                'X' : "000000",    #Index register
                'L' : "000000",    #Linkage register (JSUB)
                'PC': "000000",    #Program counter
            }
        else:
            #3 additional registers, 24 bit length + 1 register 48 bit length
            self.registers = {  
                'A' : "000000",    #Accumulator
                'X' : "000000",    #Index register
                'L' : "000000",    #Linkage register (JSUB)
                'PC': "000000",    #Program counter
                'B' : "000000",    #Base register; used for addressing
                'S' : "000000",    #General working register
                'T' : "000000",    #General working register
                'F' : "000000"     #Floating-point accumulator (48 bits)
            }

    def get_register(self, reg):
        if reg in self.registers.keys():
            return self.registers.get(reg)

    def set_register(self, reg, val):
        if reg in self.registers.keys():
            if len(val) != 6:
                val_length = 6 - len(val)
                register = self.registers[reg]
                new_val = ""

                for i in range(val_length): # Part of register that we are keeping
                    new_val += register[i]

                for i in range(len(val)): # Right-most values to change
                    new_val += val[i]
                self.registers[reg] = new_val
                return True
            
            self.registers[reg] = val
            return True
        return False

    def view_registers(self):
        for register in self.registers:
            print(register)


def hex2int(hex_val, bits):
    value = int(hex_val,16)
    if (int(hex_val,16) & (1 << (bits - 1))) != 0:
        value = int(hex_val,16) - (1 << bits)
    return value

def int2hex(number, bits):
    if number < 0:
        return hex((1 << bits) + number)[2:]
    else:
        return hex(number)[2:].upper()