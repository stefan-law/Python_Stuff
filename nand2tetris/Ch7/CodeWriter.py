# Author: Stefan A. Law
# Date: 11/25/2023
# Description:

class CodeWriter:
    """"""

    def __init__(self, input_filename, parser):
        """"""
        self._output_filename = input_filename[:-2] + 'asm'
        self._output_file = open(self._output_filename, 'w')
        self._parser = parser
        self._label_count = 0



    def writeArithmetic(self, operator):
        """"""
        label = str(self._label_count)
        self._output_file.write("// " + self._parser.get_command() + '\n')  # comment for debugging
        self._output_file.write("\t@SP\n\tM=M-1\n\t@SP\n\tA=M\n\tD=M")
        operations = {'add': '\n\t@SP\n\tM=M-1\n\t@SP\n\tA=M\n\tD=D+M',
                      'sub': '\n\tD=-D\n\t@SP\n\tM=M-1\n\t@SP\n\tA=M\n\tD=D+M',
                      'neg': '\n\tD=-D',
                      'eq': '\n\t@SP\n\tM=M-1\n\t@SP\n\tA=M\n\tD=D-M\n\t@CHECK' + label + 'TRUE\n\tD;JEQ\n\tD=-1\n(CHECK' + label + 'TRUE)\n\tD=!D\n\t@SP\n\tA=M',
                      'gt': '\n\t@SP\n\tM=M-1\n\t@SP\n\tA=M\n\tD=D-M\n\t@CHECK' + label + 'TRUE\n\tD;JLT\n\tD=0\n\t@CHECK' + label + 'FALSE\n\t0;JMP\n(CHECK' + label + 'TRUE)\n\tD=-1\n(CHECK' + label + 'FALSE)\n\t@SP\n\tA=M',
                      'lt': '\n\t@SP\n\tM=M-1\n\t@SP\n\tA=M\n\tD=D-M\n\t@CHECK' + label + 'TRUE\n\tD;JGT\n\tD=0\n\t@CHECK' + label + 'FALSE\n\t0;JMP\n(CHECK' + label + 'TRUE)\n\tD=-1\n(CHECK' + label + 'FALSE)\n\t@SP\n\tA=M',
                      'and': '\n\t@SP\n\tM=M-1\n\t@SP\n\tA=M\n\tD=D&M',
                      'not': '\n\tD=!D',
                      'or': '\n\t@SP\n\tM=M-1\n\t@SP\n\tA=M\n\tD=D|M'
                      }
        self._output_file.write(operations.get(operator))
        self._output_file.write('\n\tM=D\n\t@SP\n\tM=M+1\n')
        if operator == 'eq' or 'gt' or 'lt':
            self._label_count += 1

    def writePushPop(self, command, segment, index):
        """
        command is C_PUSH or C_POP constant
        segment(string)
        index(int)
        """
        this_that = 'THIS'
        if index == 1:
            this_that = 'THAT'

        push_segments = {'constant': '\t@' + str(index) + '\n\tD=A\n\t@SP\n\tA=M\n\tM=D\n\t@SP\n\tM=M+1\n',
                         'local': '\t@' + str(
                             index) + '\n\tD=A\n\t@LCL\n\tA=M+D\n\tD=M\n\t@SP\n\tA=M\n\tM=D\n\t@SP\n\tM=M+1\n',
                         'argument': '\t@' + str(
                             index) + '\n\tD=A\n\t@ARG\n\tA=M+D\n\tD=M\n\t@SP\n\tA=M\n\tM=D\n\t@SP\n\tM=M+1\n',
                         'this': '\t@' + str(
                             index) + '\n\tD=A\n\t@THIS\n\tA=M+D\n\tD=M\n\t@SP\n\tA=M\n\tM=D\n\t@SP\n\tM=M+1\n',
                         'that': '\t@' + str(
                             index) + '\n\tD=A\n\t@THAT\n\tA=M+D\n\tD=M\n\t@SP\n\tA=M\n\tM=D\n\t@SP\n\tM=M+1\n',
                         'temp': '\t@' + str(
                             index) + '\n\tD=A\n\t@TEMP\n\tA=M+D\n\tD=M\n\t@SP\n\tA=M\n\tM=D\n\t@SP\n\tM=M+1\n',
                         'pointer': '\t@' + this_that + '\n\tD=M\n\t@SP\n\tA=M\n\tM=D\n\t@SP\n\tM=M+1\n',
                         'static': '\t@'+self._output_filename[:-3]+str(index)+'\n\tD=M\n\t@SP\n\tA=M\n\tM=D\n\t@SP\n\tM=M+1\n'}

        pop_segments = {'local': '\t@' + str(
            index) + '\n\tD=A\n\t@LCL\n\tM=M+D\n\t@SP\n\tM=M-1\n\tA=M\n\tD=M\n\t@LCL\n\tA=M\n\tM=D\n\t@' + str(
            index) + '\n\tD=A\n\t@LCL\n\tM=M-D\n',
                        'argument': '\t@' + str(
                            index) + '\n\tD=A\n\t@ARG\n\tM=M+D\n\t@SP\n\tM=M-1\n\tA=M\n\tD=M\n\t@ARG\n\tA=M\n\tM=D\n\t@' + str(
                            index) + '\n\tD=A\n\t@ARG\n\tM=M-D\n',
                        'this': '\t@' + str(
                            index) + '\n\tD=A\n\t@THIS\n\tM=M+D\n\t@SP\n\tM=M-1\n\tA=M\n\tD=M\n\t@THIS\n\tA=M\n\tM=D\n\t@' + str(
                            index) + '\n\tD=A\n\t@THIS\n\tM=M-D\n',
                        'that': '\t@' + str(
                            index) + '\n\tD=A\n\t@THAT\n\tM=M+D\n\t@SP\n\tM=M-1\n\tA=M\n\tD=M\n\t@THAT\n\tA=M\n\tM=D\n\t@' + str(
                            index) + '\n\tD=A\n\t@THAT\n\tM=M-D\n',
                        'temp': '\t@' + str(
                            index) + '\n\tD=A\n\t@TEMP\n\tM=M+D\n\t@SP\n\tM=M-1\n\tA=M\n\tD=M\n\t@TEMP\n\tA=M\n\tM=D\n\t@' + str(
                            index) + '\n\tD=A\n\t@TEMP\n\tM=M-D\n',
                        'pointer': '\t@SP\n\tM=M-1\n\tA=M\n\tD=M\n\t@' + this_that + '\n\tM=D\n',
                        'static': '\t@SP\n\tM=M-1\n\tA=M\n\tD=M\n\t@'+self._output_filename[:-3]+str(index)+'\n\tM=D\n'
                        }

        self._output_file.write("// " + self._parser.get_command() + '\n')  # comment for debugging

        if command == 'C_PUSH':
            self._output_file.write(push_segments.get(segment))
        else:
            self._output_file.write(pop_segments.get(segment))

    def close(self):
        """"""
        self.write_end_loop()
        self._output_file.close()

    def write_end_loop(self):
        """"""
        self._output_file.write('(END)\n')
        self._output_file.write('\t@END\n')
        self._output_file.write('\t0;JMP\n')
