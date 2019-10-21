class Memory: 
    # isSimple = True    #False = SIC/XE
    def __init__(self, isSimple):
        if isSimple:
            self.memory = [None] * 4000      #size in bytes
        else:
            self.memory = [None] * 128000    #size in bytes

    def getmemory(self):
        return self.memory

    def setMemory(self):
        pass  #TODO

    def viewmemory(self):
        output = []
        for byte in self.memory:
            output.append(byte)
            if len(output) % 8 == 0: #print memory in groups of 8 bytes
                print(output)
                output = []
        if len(output) > 0:
            print(output)

class Registery:
    def __init__(self, isSimple):
        if isSimple:
            #5 registers 24 bits in length 
            self.registers = {  
                'A' : 0,    #Accumulator
                'X' : 0,    #Index register
                'L' : 0,    #Linkage register (JSUB)
                'PC': 0,    #Program counter
                'SW': 0     #Status word (Condition Code)
            }
        else:
            #3 additional registers, 24 bit length + 1 register 48 bit length
            self.registers = {  
                'A' : 0,    #Accumulator
                'X' : 0,    #Index register
                'L' : 0,    #Linkage register (JSUB)
                'PC': 0,    #Program counter
                'SW': 0,    #Status word (Condition Code)
                'B' : 0,    #Base register; used for addressing
                'S' : 0,    #General working register
                'T' : 0,    #General working register
                'F' : 0     #Floating-point accumulator (48 bits)
            }

    def getRegisters(self):
        return self.registers

    def setRegister(self):
        pass #TODO

    def viewRegisters(self):
        for register in self.registers:
            print(register)
x = Registery(True)
x.viewRegisters()
