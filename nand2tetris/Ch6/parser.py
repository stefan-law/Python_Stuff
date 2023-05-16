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
    
    if (line[:2] == ('//' or '')): #test for comment or whitespace
        line = advance()
    
    return line

def instructionType(line):
    #check if ampersand present or if in symbol table, 
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
    #TODO Add L_INSTRUCTION LOGIC

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
#    with open(output_filename, 'w') as machine_file:

    while(line != ''): #EOF ends loop
        line = advance()
        print(line)
        
        instruction_type = instructionType(line)
        print(instruction_type)
        
        if(instruction_type == ('A_INSTRUCTION' or 'L_INSTRUCTION')):
            s = symbol(line, instruction_type)

        else:
            d = dest(line)
            c = comp(line)
            j = jump(line)





    

