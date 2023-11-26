# Assembler for Ch6 nand2tetris project, which takes a ".asm"
# hack assembly source file and translates it into binary code.

import sys


class Parser:
    """
    creates Parser object
    """

    def __init__(self, symbol_table):
        """

        """
        self._command_list = []  # initialize a list that will hold each line
        self._input_file = sys.argv[1]  # second CLI arg is input file
        self._symbol_table = symbol_table
        self._command = ''  # will hold currently parsed command

        with open(self._input_file, 'r') as file:  # add each line to list
            for line in file:
                self._command_list.append(line)

        for count, line in enumerate(self._command_list):  # find and delete comments
            if "//" in line:
                deletion_index = line.find("//")
                self._command_list[count] = line[:deletion_index]

        self._command_list = [line.strip() for line in self._command_list]  # remove white space
        self._command_list = [line for line in self._command_list if line != '']  # remove empty strings

        self._label_count = 0  # this helps account for labels as they are deleted

        for count, line in enumerate(self._command_list):  # find and add labels to symbol table
            if self.instruction_type(line) == 'L_INSTRUCTION':
                self._symbol_table.add_entry(self.symbol('L_INSTRUCTION', line), count - self._label_count)
                self._label_count += 1

        # first pass is essentially completed at this point

        self._command_list = [line for line in self._command_list if line[0] != '(']  # remove labels

        self._command_list_length = len(self._command_list)  # stats on command list
        self._command_list_index = 0

        self._output_filename = self._input_file[:-3] + "hack"  # name and create blank output file
        self.output_file = open(self._output_filename, 'x')
        self.output_file.close()

    def hasMoreCommands(self):
        """
        Checks command list to see if any more commands are available
        """
        if self._command_list_index < self._command_list_length:
            return True
        else:
            return False

    def advance(self):
        """
        Advances to next line in command_list and makes active command
        """
        self._command = self._command_list[self._command_list_index]

        self._command_list_index += 1

    def instruction_type(self, line=''):
        """
        Returns type of current command line
        """
        if line == '':
            position_1_character = self._command[0]

        if line != '':
            position_1_character = line[0]

        if position_1_character == '@':
            return 'A_INSTRUCTION'
        elif position_1_character == '(':
            return 'L_INSTRUCTION'
        else:
            return 'C_INSTRUCTION'

    def symbol(self, instruction_type, l_label=''):
        """
        formats and returns L/A_INSTRUCTION
        """

        if instruction_type == 'A_INSTRUCTION':
            return self._command[1:]  # strip off @
        else:
            return l_label[1:-1]  # strip off () for L_INSTRUCTION

    def dest(self):
        """
        parse dest from C_COMMAND
        """

        if '=' not in self._command:  # no dest component for this instruction
            return ""
        else:
            slice_index = self._command.find('=')  # remove = before comparing to dest table
            return self._command[:slice_index]

    def comp(self):
        """
        parse comp from C_COMMAND
        """
        comp_slice = ''  # this is where parsed symbol will end up

        if '=' in self._command:
            comp_slice = self._command[self._command.find('=') + 1:]

        if ';' in self._command:
            comp_slice = self._command[:self._command.find(';')]

        return comp_slice

    def jump(self):
        """
        parse jump from C_COMMAND
        """
        if ';' not in self._command:  # no jump in this instruction
            return ""
        else:
            slice_index = self._command.find(';') + 1
            return self._command[slice_index:]

    def getFilename(self):  # get method for other classes
        return self._output_filename

    def get_command(self):
        """

        """
        return self._command

    def set_command_list_index(self, new_index):  #
        self._command_list_index = new_index


class Assembler:
    """
    Utilizes Parser and Code classes to run assembler loop
    """

    def __init__(self):
        """

        """


        self._symbol_table = SymbolTable()
        self._parser = Parser(self._symbol_table)  # Creates a parser object
        self._code = Code()  # Creates a Code object
        self._output_filename = self._parser.getFilename()  # bring created output filename over

        self._symbol_address = 16

    def assemble(self):  # this method is called to run the assembly loop
        """

        """
        self.first_pass()  # find labels and symbols and build out respective tables
        self.second_pass()  # parse instructions, convert to binary, and write to output file

    def first_pass(self):
        pass

    def second_pass(self):
        while self._parser.hasMoreCommands():  # loop through list of commands
            self._parser.advance()

            if self._parser.instruction_type() == 'C_INSTRUCTION':
                self.c_code_writer()
            elif self._parser.instruction_type() == 'A_INSTRUCTION':
                self.a_code_writer()

    def c_code_writer(self):
        dest = self._parser.dest()
        comp = self._parser.comp()
        jump = self._parser.jump()

        binary = '111' + self._code.comp(comp) + self._code.dest(dest) + self._code.jump(jump)

        with open(self._output_filename, 'a') as file:
            file.write(binary + '\n')

    def a_code_writer(self):
        """

        """
        symbol = self._parser.symbol('A_INSTRUCTION')

        if symbol.isnumeric():  # handle numeric addresses and write to binary
            binary = bin(int(self._parser.symbol('A_INSTRUCTION'))).replace("0b", "")
        else:  # handle labels and variables
            if self._symbol_table.contains(symbol):  # symbol already in table
                binary = bin(int(self._symbol_table.get_address(symbol))).replace("0b", "")
            else:  # symbol not in table, add to table and then create instruction
                self._symbol_table.add_entry(symbol, self._symbol_address)
                self._symbol_address += 1
                binary = bin(int(self._symbol_table.get_address(symbol))).replace("0b", "")

        padding = 16 - len(binary) # ensure 16-bit binary

        if padding > 0:
            for zero in range(padding):
                binary = '0' + binary

        with open(self._output_filename, 'a') as file:  # write binary to file
            file.write(binary + '\n')


class Code:
    """

    """

    def __init__(self):
        self._comp_table = {'0': '0101010',
                            '1': '0111111',
                            '-1': '0111010',
                            'D': '0001100',
                            'A': '0110000',
                            'M': '1110000',
                            '!D': '0001101',
                            '!A': '0110001',
                            '!M': '1110001',
                            '-D': '0001111',
                            '-A': '0110011',
                            '-M': '1110011',
                            'D+1': '0011111',
                            'A+1': '0110111',
                            'M+1': '1110111',
                            'D-1': '0001110',
                            'A-1': '0110010',
                            'M-1': '1110010',
                            'D+A': '0000010',
                            'D+M': '1000010',
                            'D-A': '0010011',
                            'D-M': '1010011',
                            'A-D': '0000111',
                            'M-D': '1000111',
                            'D&A': '0000000',
                            'D&M': '1000000',
                            'D|A': '0010101',
                            'D|M': '1010101'
                            }

        self._jump_table = {'': '000',
                            'JGT': '001',
                            'JEQ': '010',
                            'JGE': '011',
                            'JLT': '100',
                            'JNE': '101',
                            'JLE': '110',
                            'JMP': '111'
                            }

        self._dest_table = {'': '000',
                            'M': '001',
                            'D': '010',
                            'DM': '011',
                            'A': '100',
                            'AM': '101',
                            'AD': '110',
                            'ADM': '111'
                            }

    def dest(self, dest_symbol):
        return self._dest_table[dest_symbol]

    def comp(self, comp_symbol):
        return self._comp_table[comp_symbol]

    def jump(self, jump_symbol):
        return self._jump_table[jump_symbol]


class SymbolTable:
    """

    """

    def __init__(self):
        self._symbol_table = {'R0': '0',
                              'R1': '1',
                              'R2': '2',
                              'R3': '3',
                              'R4': '4',
                              'R5': '5',
                              'R6': '6',
                              'R7': '7',
                              'R8': '8',
                              'R9': '9',
                              'R10': '10',
                              'R11': '11',
                              'R12': '12',
                              'R13': '13',
                              'R14': '14',
                              'R15': '15',
                              'SP': '0',
                              'LCL': '1',
                              'ARG': '2',
                              'THIS': '3',
                              'THAT': '4',
                              'SCREEN': '16384',
                              'KBD': '24576',
                              'LOOP': '4',
                              'STOP': '18',
                              }

    def add_entry(self, symbol, address):
        """
        add symbol to symbol table with associated address
        """
        self._symbol_table[symbol] = address

    def contains(self, symbol):
        """
        check to see if symbol already contained in symbol table
        """
        if symbol in self._symbol_table:
            return True
        else:
            return False

    def get_address(self, symbol):
        """
        returns address of queried symbol in symbol table
        """
        return self._symbol_table[symbol]


assembler = Assembler()  # Create an assembler instance
assembler.assemble()  # run assembler
