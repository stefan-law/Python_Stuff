import sys

#Take second argument from CLI ands open file in read mode
input_filename = sys.argv[1]
output_filename = input_filename[:-3] + "hack"

line = ' '

def advance():
    #Take next line in file, check for EOF,strip whitespace, 
    # skip if empty whitespace or comment (//)
    line = assembly_file.readline()
    
    if line == '':
        print('EOF')
        return line
        
    line = line.strip()
    
    if (line[:2] == ('//' or '')):
        line = advance()
    
    return line

with open(input_filename, 'r') as assembly_file:
#    with open(output_filename, 'w') as machine_file:

    while(line != ''): #EOF ends loop
        line = advance()
        print(line)
        #instruction_type =instructionType(next_line)



    

