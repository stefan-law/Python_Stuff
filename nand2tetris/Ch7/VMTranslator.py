# Author: Stefan A. Law
# Date: 11/25/2023
# Description:

import sys
from Parser import Parser
from CodeWriter import CodeWriter

class VMTranslator:
    """

    """

    def __init__(self):
        """

        """
        self._input_filename = sys.argv[1]
        self._parser = Parser(self._input_filename)
        self._codewriter = CodeWriter(sys.argv[1], self._parser)

    def translate(self):
        """"""
        while self._parser.hasMoreLines():
            self._parser.advance()

            if self._parser.get_command() == '':
                continue

            if self._parser.commandType() == 'C_ARITHMETIC':
                self._codewriter.writeArithmetic(self._parser.get_command())
            elif self._parser.commandType() == 'C_POP' or 'C_PUSH':
                self._codewriter.writePushPop(self._parser.commandType(), self._parser.arg1(), self._parser.arg2())

        self._codewriter.close()

translator = VMTranslator()
translator.translate()
