# Author: Stefan A. Law
# Date: 11/25/2023
# Description:

import sys  # will be used for parsing arguments from CLI (i.e. filename to be translated)
from Parser import Parser
from CodeWriter import CodeWriter


class VMTranslator:
    """
    Initializes Parser and CodeWriter objects and obtains filename to be translated
    A call to translate() will translate the input file to an output file
    """

    def __init__(self):
        """
        parse input filename
        create Parser and CodeWriter objects
        """
        self._input_filename = sys.argv[1]
        self._parser = Parser(self._input_filename)
        self._codewriter = CodeWriter(sys.argv[1], self._parser)

    def translate(self):
        """
        Iterates through each line of input file
        Determines command type
        Writes command
        """
        while self._parser.hasMoreLines():  # check to see if any more lines in file
            self._parser.advance()  # go to next line in file and make active command

            if self._parser.get_command() == '':  # if empty, skip line
                continue

            if self._parser.commandType() == 'C_ARITHMETIC':  # command is an arithmetic/logic command
                self._codewriter.writeArithmetic(self._parser.get_command())
            elif self._parser.commandType() == 'C_POP' or 'C_PUSH':  # command is a pop or push command
                self._codewriter.writePushPop(self._parser.commandType(), self._parser.arg1(), self._parser.arg2())

        self._codewriter.close()  # calls method that adds infinite loop at end of file and closes it.


translator = VMTranslator()
translator.translate()
