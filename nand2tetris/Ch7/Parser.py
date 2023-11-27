# Author: Stefan A. Law
# Date: 11/25/2023
# Description:

class Parser:
    """

    """

    def __init__(self, input_filename):
        """

        """
        with open(input_filename, 'r') as file:
            for count, line in enumerate(file):  # determine number of lines
                pass

        self._input_file = open(input_filename, 'r')  # open input file to be parsed

        self._line_count = count
        self._line_index = 0

        self._current_command = ''

    def hasMoreLines(self):
        """

        """
        if self._line_index <= self._line_count:
            return True
        else:
            self._input_file.close()
            return False

    def advance(self):
        """

        """
        self._current_command = self._input_file.readline()
        self._line_index += 1  # advance head

        if "//" in self._current_command:
            self._current_command = self._current_command[:self._current_command.find('//')]  # remove comments

        self._current_command = self._current_command.strip()  # remove whitespace

    def commandType(self):
        """

        """
        command = self._current_command.split()[0]
        arithmetic_operators = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']

        if command in arithmetic_operators:
            return 'C_ARITHMETIC'
        elif command == 'push':
            return 'C_PUSH'
        elif command == 'pop':
            return 'C_POP'
        # TODO
        """Implement return criteria for label, goto, if, function, return, and call"""

    def arg1(self):
        """"""
        return self._current_command.split()[1]

    def arg2(self):
        """"""
        return int(self._current_command.split()[2])

    def get_command(self):
        """
        :return:
        """
        return self._current_command
