import sys
from parse import read_file
from sim_interpreter import Interpreter
from memory import Memory, Registery

SIZE_OF_BYTE = 2 #Characters
VALID_OPTIONS_SIMPLE = ["A", "X", "L", "PC"] #NOTE How should we handle a user trying to edit the PC register?
VALID_OPTIONS_EXTENDED = ["A", "X", "L", "PC","B", "S", "T", "F"] #NOTE How should we handle a user trying to edit the PC register?


def clear_console():
    print("\n" * 100)

def get_input():
    print('>', end =" ")
    return input()

class Console:

    def __init__(self):
        self.isExtended = False # HARD CODE TODO: REMOVE IN ARCHITECTURE INTEGRATION
        self.instruction_array = None
        self.memory = Memory(True)
        self.registery = Registery(True)        
        self.interpreter = None

    def command_handler(self, command = "NA"):
        commands = ["help", "credits", "parse", "viewmem", "viewreg", "start", "next", "changereg", "changemem", "stop", "exit"]
        args = command.split(' ')

        if args[0] in commands:
            if args[0] == "help":
                print("help\t\t\tView available commands\n" + 
                "credits\t\t\tView credits\n" + 
                "parse\t\t\tBegin parsing and syntax checking\n" + 
                "viewmem\t\t\tExport current memory to a text-file\n" +
                "viewreg\t\t\tView the value of a given register\n" +
                "start\t\t\tStarts the interpreter\n" +
                "next\t\t\tIncrements the interpreter by one instruction\n" +
                "changereg\t\tAlters a given register\n" +
                "changemem\t\tAlters a section of memory\n" + 
                "stop\t\t\tStops the interpreter\n" +
                "exit\t\t\tExits the simulator\n"
                )
            elif args[0] == "credits":
                clear_console()
                print("----------Credits----------")
                print("Product of Bagel Bois 2019")
                print("Gary Fishell - Console and Interpreter Architecture Design")
                print("Salim Aweys - Memory and Register management")
                print("Lauren DeLeon - Parser Design and Documentation")
                print("Kristian Bunda - Memory/Register Design and Assembler Directives management")
                print("SIC and SICXE Instruction implementation - Collective effort")
                print("---------------------------")

            elif args[0] == "parse":
                if len(args) != 2:
                    print("Usage: parse [filename]")
                    return
        
                self.instruction_array = (read_file(args[1]))
                if self.instruction_array is None:
                    print("Parsing unsuccesful")

            elif args[0] == "viewmem":
                if len(args) != 2:
                    print("Usage: viewmem [address]")
                    return
        
                address = args[1]
        
                if self.isExtended and len(address) == SIZE_OF_BYTE * 2.5:
                    print("Printing memory on extended address")
        
                elif not self.isExtended and len(address) == SIZE_OF_BYTE * 2:
                    memory = self.memory.get_memory(address)
                    if(memory == None):
                        print("Address out of bounds or invalid address")
                    
                    else:
                        print(memory)

                else:
                    print("Please provide an address in the correct format")     

            elif args[0] == "viewreg":
                if len(args) != 2:
                    print("Usage: viewreg [register]")
                    return

                reg_choice = args[1]
                if self.isExtended and reg_choice in VALID_OPTIONS_EXTENDED:
                    print("Printing register", reg_choice)
                
                elif not self.isExtended and reg_choice in VALID_OPTIONS_SIMPLE:
                    print(self.registery.get_register(reg_choice))
                    

            elif args[0] == "start":
                self.interpreter = Interpreter(self.instruction_array, self.memory, self.registery)
                self.interpreter.assign_address()

            elif args[0] == "next":
                self.interpreter.execute_next_instruction()
            

            elif args[0] == "changereg":
                if len(args) != 3:
                    print("Usage: changereg [register] [value]")
                    return
        
                reg_choice = args[1]
                value = args[2]

                if(len(value) % 2 != 0 or len(value) > 6):
                    print("Please provide a valid value")
                    return
                
                if self.isExtended and reg_choice in VALID_OPTIONS_EXTENDED:
                    print("Adjusting register", reg_choice, "to", value )
                
                elif not self.isExtended and reg_choice in VALID_OPTIONS_SIMPLE:
                    if self.registery.set_register(reg_choice, value) == False:
                        print("Invalid value - Setting register failed")

                else:
                    print("Please provide a valid register")     

            elif args[0] == "changemem":
                if len(args) != 3:
                    print("Usage: changemem [address] [bytevalue]")
                    return

                address = args[1]
                value = args[2]

                if(len(value) != SIZE_OF_BYTE):
                    print("Please provide a valid value")
                    return
                
                if self.memory.set_memory(address, value) == False:
                    print("Invalid value or address - Setting memory failed")

            elif args[0] == "stop":
                print("Stopping interpreter")

            elif args[0] == "exit":
                print("Bye :)")
                sys.exit()   

        else:
            print("Invalid command")     

def Main():
    print("SIC/XE Simulator 1.0.0")
    print("Type \"help\" for more information")

    prompt = Console()
    
    

    while True:
        prompt.command_handler(get_input())

Main()