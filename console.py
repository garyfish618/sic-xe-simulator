import sys

def clear_console():
    print("\n" * 100)

def get_input():
    print('>', end =" ")
    return input()

def help():
    print("hi")



class Console:

    def __init__(self):
        self.isExtended = True # HARD CODE TODO: REMOVE IN ARCHITECTURE INTEGRATION

    def command_handler(self, command = "NA"):
        commands = ["help", "credits", "parse", "viewmem", "viewreg", "start", "next", "changereg", "changemem", "stop", "exit"]
        line = command.split(' ')

        if line[0] in commands:
            getattr(Console(), line[0])(line)

        else:
            print("Invalid command")

    def help(self, args):
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
    
    def credits(self, args):
        print("Rolling Credits")
        print(args)

    def parse(self, args):
        print("Starting parser")

    def viewmem(self, args):

        if len(args) != 2:
            print("Usage: viewmem [address]")
            return
        
        address = args[1]
        
        if self.isExtended and len(address) == 5:
            print("Printing memory on extended address")
        
        elif not self.isExtended and len(address) == 4:
            print("Printing memory on simple address")

        else:
            print("Please provide an address in the correct format")     

    def viewreg(self, args):
        print("hi")

    def start(self, args):
        print("Starting interpreter")

    def next(self, args):
        print("Next line")

    def changereg(self, args):
        print("hi")

    def changemem(self, args):
        print("hi")

    def stop(self, args):
        print("Stopping interpreter")

    def exit(self, args):
        sys.exit()



def Main():
    print("SIC/XE Simulator 1.0.0")
    print("Type \"help\" for more information")

    prompt = Console()
    
    

    while True:
        prompt.command_handler(get_input())


Main()