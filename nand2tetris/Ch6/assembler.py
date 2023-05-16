import sys
import parser
import code

###Move while loop and file access over to here

#INITIALIZE, move to symbolTable and code
symbol_table = {'R0':'0','R1':'1', 'R2':'2', 'R3':'3',
                'R4':'4', 'R5':'5','R6':'6', 'R7':'7',
                'R8':'8', 'R9':'9', 'R10':'10', 'R11':'11',
                'R12':'12', 'R13':'13', 'R14':'14',
                'R15':'15', 'SP':'0', 'LCL':'1',
                'ARG':'2', 'THIS':'3', 'THAT':'4',
                'SCREEN': '16384','KBD':'24576',}

ram_counter = 16

comp_table = {'0':'0101010',
              '1':'0111111',
              '-1':'0111010',
              'D':'0001100',
              'A':'0110000',
              'M':'1110000',
              '!D':'0001101',
              '!A':}

