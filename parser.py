import sys
class Instruction:

    def __init__(self, label, name, args):
        self.label = label
        self.name = name
        self.args = args  

    def setLabel(self, label):
        return self.label

    def setName(self, name):
        return self.name

    def setArgs(self, args):
        return self.args

def readFile(filename):
    linelist = []
    try:
        with open(filename) as f:
            content = f.readlines()
            for line in content:
                modlist = line.split(',')
                for x in modlist:
                    linelist.append(x)
        return linelist
    except IOError:
        print('File not found')
        sys.exit(1)

def makeArray(array):
    lists = []
    obj = Instruction(lists[0], lists[1], lists[2])
    for x in len(array):
        obj = lists[x]



def Main():
    print('Parser for the SIC/XE Simulator\n')
    print('Use the appropriate xfile')
    file = files
    array = []
    array = readFile(files)
    makeArray(array)
#  Begin program
if __name__ == '__main__':
    main()