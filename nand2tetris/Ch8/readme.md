

#if-goto label; if top of stack is not zero, jump to label
@SP
A=M-1 //look at top of stack
D=M // save stack value in D register
@SP // need to decrement pointer before we go since "base case check" not needed anymore
//and should be passed to repeat loop via arg
M=M-1
@label //jump address
D;JNE //jump if true, i.e. jump if not zero/false


(#call f nArgs)
//push return address
//return address will be sorted out by assembler during it's first
//pass so we need only address the label that will be inserted
@label //label = file_name.function_name$ret.i (i= label index, one for each call of a function)
D=A //store address of label
@SP
A=M
M=D //store return address in stack
@SP
M=M+1 // increase SP