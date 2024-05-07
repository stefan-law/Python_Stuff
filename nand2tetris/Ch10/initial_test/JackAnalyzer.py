import os
import sys

import compilationEngine, tokenizer

def main():
    """"""
    input_filename = sys.argv[1]
    tokenizer_list = []
    engine_list = []
    path = os.getcwd() + '/' + input_filename


    if ".jack" in input_filename:
        output_filename = input_filename[:input_filename.find(".jack")] + "T.xml"
        output_file = open(output_filename, 'w')
        tokenizer_list.append((tokenizer.Tokenizer(path), output_file))
        # engine_list.append(compilationEngine.CompilationEngine(input_filename, output_file))
    else:
        for filename in os.listdir(path):
            if ".jack" in filename:
                output_filename = filename[:filename.find(".jack")] + "T.xml"
                output_file = open(output_filename, 'w')
                tokenizer_list.append((tokenizer.Tokenizer(path + '/' + filename), output_file))
               # engine_list.append(compilationEngine.CompilationEngine())

    for reader in tokenizer_list:
        tokens = reader[0]
        file = reader[1]
        file.write("<tokens>\n")
        tokens.advance()
        while reader[0].has_more_tokens():
            file.write("<" + tokens.token_type() + "> " + tokens.get_token() + " </" + tokens.token_type() +
                              ">\n")
        file.write("</tokens>\n")


if __name__ == "main":
    main()
