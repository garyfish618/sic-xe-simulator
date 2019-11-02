class directive:
    def __init__(self):
        self.directive = {
            'RESW': 0
            'RESB': 0
            'WORD': 0
            'BYTE': 0
        }
    def alloc_mem(self, direc, number):
        if direc in self.directive.keys():
            if direc is 'RESW'
                hex =  3 * hex(number)
            if direc is 'RESB'
                hex = hex(number)
            if direc is 'WORD'
                mem = 3 * number
            if direc is 'BYTE'
                mem = number

        return False
