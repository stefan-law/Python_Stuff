# Assembler for Ch6 nand2tetris project, which takes a ".asm"
# hack assembly source file and translates it into binary code.

import sys

class Parser:
    """
    creates Parser, Code instances
    """

    def __init__(self):
        """

        """
        self._command_list = []  # initialize a list that will hold each line
        self._input_file = sys.argv[1]  # second CLI arg is input file

        with open(self._input_file, 'r') as file:  # add each line to list
            for line in file:
                self._command_list.append(line)

        for line in self._command_list:
            line.strip()  # strip whitespace
            if "//" in line:
                deletion_index = line.find("//")
                self._command_list[line] = line[:deletion_index]  # slice out comments

        self._command_list_length = len(self._command_list)
        self._command_list_index = 0
        self._command = ''

        self._output_filename = self._input_file[:-3] + "hack"
        self.output_file = open(self._output_filename, 'x')
        self.output_file.close()

    def hasMoreCommands(self):
        """

        """
        if self._command_list_index < self._command_list_length:
            return True
        else:
            return False

    def advance(self):
        """

        """
        self._command = self._command_list[self._command_list_index]

        self._command_list_index += 1

    def instruction_type(self):
        """

        """
        position_1_character = self._command[0]

        if position_1_character == '@':
            return 'A_INSTRUCTION'
        elif position_1_character == '(':
            return 'L_INSTRUCTION'
        else:
            return 'C_INSTRUCTION'

    def symbol(self, instruction_type):
        """

        """

        if instruction_type == 'A_INSTRUCTION':
            return int(self._command[1:])  # strip off @
        else:
            return self._command[1:-1]  # strip off () for L_INSTRUCTION

    def dest(self):
        """

        """

        if '=' not in self._command:
            return ""
        else:
            slice_index = self._command.find('=')
            return self._command[:slice_index]

    def comp(self):
        """

        """
        left_slice_index = 0
        right_slice_index = 0

        if '=' in self._command:
            left_slice_index = self._command.find('=') + 1

        if ';' in self._command:
            right_slice_index = self._command.find(';')

        return self._command[left_slice_index:right_slice_index]

    def jump(self):
        """

        """
        if ';' not in self._command:
            return ""
        else:
            slice_index = self._command.find(';') + 1
            return self._command[slice_index:]

    def getFilename(self):
        return self._output_filename


class Assembler:
    """

    """

    def __init__(self):
        """

        """
        self._parser = Parser()
        self._code = Code()
        self._output_filename = self._parser.getFilename()

    def assemble(self):
        """

        """
        self.first_pass()
        self.second_pass()

    def first_pass(self):
        pass

    def second_pass(self):
        while self._parser.hasMoreCommands():
            self._parser.advance()

            if self._parser.instruction_type() == 'C_INSTRUCTION':
                self.c_code_writer()
            elif self._parser.instruction_type() == 'A_INSTRUCTION':
                self.a_code_writer()

    def c_code_writer(self):
        dest = self._parser.dest()
        comp = self._parser.comp()
        jump = self._parser.jump()

        binary = self._code.dest(dest) + self._code.comp(comp) + self._code.jump(jump)

        with open(self._output_filename, 'a') as file:
            file.write(binary + '\n')

    def a_code_writer(self):
        """

        """
        binary = bin(self._parser.symbol('A_INSTRUCTION'))

        with open(self._output_filename, 'a') as file:
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


assembler = Assembler()  # Create an assembler instance
assembler.assemble()  # run assembler
