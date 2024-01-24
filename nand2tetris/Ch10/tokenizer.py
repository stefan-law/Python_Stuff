import os
import sys


class Tokenizer:
    """"""

    def __init__(self, input_filename: str) -> None:
        """"""
        self._path = os.getcwd() + '/' + sys.argv[1] + '/' + input_filename
        self._file = open(self._path, 'r')
        self._line = ""
        self._token = ""
        self.advance()

    def has_more_tokens(self) -> bool:
        """"""
        if self._line != "" and self._token != '\n':  # This is not an empty line/EOF and line has more tokens
            return True
        elif self._line != "" and self._token == '\n':  # This is not an empty line/EOF and current line has no more tokens
            self.advance()
            return self.has_more_tokens()  # May need to recursively call/return has_more_tokens after advance
        else:
            return False

    def advance(self) -> None:
        """
        Advances file to next line and reads it
        Removes comments
        :return:
        """

        self._line = self._file.readline()

        if "//" in self._line:  # handle single line comment
            self._line = self._line[:self._line.find("//")] + '\n'

        if "/*" in self._line:
            if "*/" in self._line:
                comment = self._line[self._line.find("/*") : self._line.find("*/") + 2]
                self._line.replace(comment, "")
                return
            else:
                self._line = self._line[:self._line.find("/*")] + '\n'
                return

        #TODO: Handle /** API comments

        if "*/" in self._line:
            self._line = self._line[self._line.find("*/") + 2:]



    def token_type(self):
        """"""
        pass

    def keyword(self):
        """"""
        pass

    def symbol(self):
        """"""
        pass

    def identifier(self):
        """"""
        pass

    def int_val(self):
        """"""
        pass

    def string_val(self):
        """"""
        pass



