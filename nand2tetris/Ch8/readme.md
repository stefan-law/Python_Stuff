

#if-goto label; if top of stack is not zero, jump to label
@SP
A=M-1 //look at top of stack
D=M // save stack value in D register
@SP // need to decrement pointer before we go since "base case check" not needed anymore
//and should be passed to repeat loop via arg
M=M-1
@label //jump address
D;JNE //jump if true, i.e. jump if not zero/false