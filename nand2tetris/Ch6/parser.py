import sys

#Take second argument (input filename) from CLI ands open file in read mode
input_filename = sys.argv[1]
output_filename = input_filename[:-3] + "hack"

line = ' '

def advance():
    #Take next line in file, check for EOF,strip whitespace, 
    # skip if empty whitespace or comment (//)
    line = assembly_file.readline()
    
    if line == '': #EOF, terminate function
        return line
        
    line = line.strip()
    
    if ((line == '') or (line[:2] == '//')): #test for comment or whitespace
        line = advance()
    
    return line

def instructionType(line):
    #check if ampersand present for a-instruct
    #  or left parenthesis for label, 
    # otherwise is a c-instruction
    if line[0] == '@':
        return 'A_INSTRUCTION'
    elif line[0] == '(':
       return 'L_INSTRUCTION'
    else:
        return 'C_INSTRUCTION'

def symbol(line, instruction_type):
    if instruction_type == 'A_INSTRUCTION':
        return line[1:]
    else:
        #Is a label
        return line[1:line.find(')')]

def dest(line):
    if '=' in line:
        index = line.find('=')
        return line[:index]
    else:
        return 'null'

def jump(line):
    if ';' in line:
        index = line.find(';')
        return line[index:]
    else:
        return 'null'

def comp(line):
    start = 0
    if '=' in line:
        start = line.find('=') + 1

    end = len(line)
    if ';' in line:
        end = line.find(';')
    
    return line[start:end]

    

with open(input_filename, 'r') as assembly_file:


    while(line != ''): #EOF ends loop (TODO change to flag)
        line = advance()
        print(line)
        
        instruction_type = instructionType(line)
        print(instruction_type)
        
        if(instruction_type == ('A_INSTRUCTION' or 'L_INSTRUCTION')):
            s = symbol(line, instruction_type)
            #TODO lookup s in symbol table and convert to number if present
            #TODO convert s to 15-bit binary and prepend 0, then convert to string

        else:
            d = dest(line)
            #dbin = code.dest(d) Convert symbol to binary
            c = comp(line)
            #cbin = code.comp(c) Convert symbol to binary
            j = jump(line)
            #jbin =code.jump(j) Convert symbol to binary
            #TODO link 111 + c + d + j, then convert back to string
        
        #TODO Write binary line to file
        #    with open(output_filename, 'a') as machine_file:
        #           line += '\n'
        #           machine_file.write(line)





    

