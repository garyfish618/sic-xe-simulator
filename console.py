import sys

def clear_console():
    print("\n" * 100)

def get_input():
    print('>', end =" ")
    return input()

def help():
    print("hi")



class Console:
    def command_handler(self, command = "NA"):
        commands = ["help", "credits", "parse", "viewmem", "viewreg", "start", "next", "changereg", "changemem", "stop", "exit"]

        if command in commands:
            getattr(Console(), command)()

        else:
            print("Invalid command")

    def help(self):
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
    
    def credits(self):
        print("hi")

    def parse(self):
        print("hi")

    def viewmem(self):
        print("hi")

    def viewreg(self):
        print("hi")

    def start(self):
        print("hi")

    def next(self):
        print("hi")

    def changereg(self):
        print("hi")

    def changemem(self):
        print("hi")

    def stop(self):
        print("hi")

    def exit(self):
        sys.exit()



def Main():
    print("SIC/XE Simulator 1.0.0")
    print("Type \"help\" for more information")

    prompt = Console()
    
    

    while True:
        prompt.command_handler(get_input())


Main()