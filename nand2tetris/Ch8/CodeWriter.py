# Author: Stefan A. Law
# Date: 11/25/2023
# Description:

class CodeWriter:
    """
    See readme for documentation of assembly segments
    Has capabilites for writing arithmetic/logical commands and push/pop commands
    Has method for adding infinite loop at end of file and closing it when translation complete
    """

    def __init__(self, input_filename, parser):
        """
        Takes input filename (string) and parser (object) as arguments
        """
        self._output_filename = input_filename[:-2] + 'asm'  # create the output filename
        self._output_file = open(self._output_filename, 'w')  # create the output file and open in write mode
        self._parser = parser  # reference to parser object
        self._label_count = 0  # allows us to write an arbitrary number of labels and will be iterated



    def writeArithmetic(self, operator):
        """
        Accepts operator argument (string)
        Writes arithmetic command in Hack machine language
        """
        label = str(self._label_count)
        # this may be added to commands if eq/gt/lt as these ops require label for branching

        self._output_file.write("// " + self._parser.get_command() + '\n')  # comment for debugging

        self._output_file.write("\t@SP\n\tM=M-1\n\t@SP\n\tA=M\n\tD=M")  # common code that all ops need for getting first arg
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
        self._output_file.write(operations.get(operator))  # reference above dictionary to obtain needed code
        self._output_file.write('\n\tM=D\n\t@SP\n\tM=M+1\n') # common code to store result and increment SP
        if operator == 'eq' or 'gt' or 'lt':  # increase label count for next needed label
            self._label_count += 1

    def writePushPop(self, command, segment, index):
        """
        command is C_PUSH or C_POP constant
        segment(string)
        index(int)
        Writes a push or pop command in Hack machine language
        """
        this_that = 'THIS'  # index is 0 (only relevant for this/that)
        if index == 1:
            this_that = 'THAT'

        push_segments = {'constant': '\t@' + str(index) + '\n\tD=A\n\t@SP\n\tA=M\n\tM=D\n\t@SP\n\tM=M+1\n',
                         'local': '\t@' + str(
                             index) + '\n\tD=A\n\t@LCL\n\tA=D+M\n\tD=M\n\t@SP\n\tA=M\n\tM=D\n\t@SP\n\tM=M+1\n',
                         'argument': '\t@' + str(
                             index) + '\n\tD=A\n\t@ARG\n\tA=D+M\n\tD=M\n\t@SP\n\tA=M\n\tM=D\n\t@SP\n\tM=M+1\n',
                         'this': '\t@' + str(
                             index) + '\n\tD=A\n\t@THIS\n\tA=D+M\n\tD=M\n\t@SP\n\tA=M\n\tM=D\n\t@SP\n\tM=M+1\n',
                         'that': '\t@' + str(
                             index) + '\n\tD=A\n\t@THAT\n\tA=D+M\n\tD=M\n\t@SP\n\tA=M\n\tM=D\n\t@SP\n\tM=M+1\n',
                         'temp': '\t@' + str(
                             index) + '\n\tD=A\n\t@TEMP\n\tA=D+M\n\tD=M\n\t@SP\n\tA=M\n\tM=D\n\t@SP\n\tM=M+1\n',
                         'pointer': '\t@' + this_that + '\n\tD=M\n\t@SP\n\tA=M\n\tM=D\n\t@SP\n\tM=M+1\n',
                         'static': '\t@'+self._output_filename[:-3]+str(index)+'\n\tD=M\n\t@SP\n\tA=M\n\tM=D\n\t@SP\n\tM=M+1\n'}

        pop_segments = {'local': '\t@' + str(
                            index) + '\n\tD=A\n\t@LCL\n\tM=D+M\n\t@SP\n\tM=M-1\n\tA=M\n\tD=M\n\t@LCL\n\tA=M\n\tM=D\n\t@' + str(
                            index) + '\n\tD=A\n\t@LCL\n\tM=M-D\n',
                        'argument': '\t@' + str(
                            index) + '\n\tD=A\n\t@ARG\n\tM=D+M\n\t@SP\n\tM=M-1\n\tA=M\n\tD=M\n\t@ARG\n\tA=M\n\tM=D\n\t@' + str(
                            index) + '\n\tD=A\n\t@ARG\n\tM=M-D\n',
                        'this': '\t@' + str(
                            index) + '\n\tD=A\n\t@THIS\n\tM=D+M\n\t@SP\n\tM=M-1\n\tA=M\n\tD=M\n\t@THIS\n\tA=M\n\tM=D\n\t@' + str(
                            index) + '\n\tD=A\n\t@THIS\n\tM=M-D\n',
                        'that': '\t@' + str(
                            index) + '\n\tD=A\n\t@THAT\n\tM=D+M\n\t@SP\n\tM=M-1\n\tA=M\n\tD=M\n\t@THAT\n\tA=M\n\tM=D\n\t@' + str(
                            index) + '\n\tD=A\n\t@THAT\n\tM=M-D\n',
                        'temp': '\t@' + str(
                            index) + '\n\tD=A\n\t@TEMP\n\tM=D+M\n\t@SP\n\tM=M-1\n\tA=M\n\tD=M\n\t@TEMP\n\tA=M\n\tM=D\n\t@' + str(
                            index) + '\n\tD=A\n\t@TEMP\n\tM=M-D\n',
                        'pointer': '\t@SP\n\tM=M-1\n\tA=M\n\tD=M\n\t@' + this_that + '\n\tM=D\n',
                        'static': '\t@SP\n\tM=M-1\n\tA=M\n\tD=M\n\t@'+self._output_filename[:-3]+str(index)+'\n\tM=D\n'
                        }

        self._output_file.write("// " + self._parser.get_command() + '\n')  # comment for debugging

        if command == 'C_PUSH':  # determine if push or pop and write relevant code from above dicts
            self._output_file.write(push_segments.get(segment))
        elif command == 'C_POP':
            self._output_file.write(pop_segments.get(segment))

    def writeLabel(self, label):
        """
        label (string)
        """
        self._output_file.write("// " + self._parser.get_command() + '\n')  # comment for debugging
        self._output_file.write('('+label+')\n')

    def writeGoto(self, label):
        """
        label (string)
        """
        self._output_file.write("// " + self._parser.get_command() + '\n')  # comment for debugging
        self._output_file.write('@'+label)
        self._output_file.write('0;JMP')

    def writeIf(self, label):
        """

        :param label: string
        :return:
        """
        self._output_file.write("// " + self._parser.get_command() + '\n')  # comment for debugging

        self._output_file.write('\t@SP\n')
        self._output_file.write('\tA=M-1\n')
        self._output_file.write('\tD=M\n')
        self._output_file.write('\t@SP\n')
        self._output_file.write('\tM=M-1\n')
        self._output_file.write('\t@'+label+'\n')
        self._output_file.write('\tD;JNE\n')


    def writeFunction(self, function_name, n_vars):
        """

        :param function_name: string
        :param n_vars: int
        :return:
        """
        pass

    def writeCall(self, function_name, n_args):
        """

        :param function_name: string
        :param n_args: int
        :return:
        """
        pass

    def writeReturn(self):
        """

        :return:
        """
        pass

    def setFileName(self, file_name):
        """
        file_name (string)
        Informs that the translation of a new VM file has started (called by the VMTranslator)
        """
        pass

    def close(self):
        """"""
        self.write_end_loop()  # write an infinite loop at end of code to protect memory intrusion
        self._output_file.close()  # close file

    def write_end_loop(self):
        """"""
        self._output_file.write('(END)\n')
        self._output_file.write('\t@END\n')
        self._output_file.write('\t0;JMP\n')
