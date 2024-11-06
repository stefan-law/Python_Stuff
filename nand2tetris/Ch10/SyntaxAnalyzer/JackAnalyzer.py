import os
import sys
import compilationEngine, tokenizer

def main():
    """
    Initializes and invokes tokenizer and compilation engine
    """
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
            file.write(
                "<" + token_typer(tokens) + "> " + tokens.get_token() + " </" + token_typer(tokens) +
                ">\n")
            tokens.advance()
        file.write("</tokens>\n")
        file.close()


def token_typer(tokens) -> str:
    """
    Formats token type for XML output
    """
    match tokens.token_type():
        case 'INT_CONST':
            return 'integerConstant'
        case 'STRING_CONST':
            return 'stringConstant'
        case _:
            return tokens.token_type().lower()


if __name__ == "__main__":
    main()
