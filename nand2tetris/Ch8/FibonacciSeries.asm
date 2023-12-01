// push argument 1
	@1
	D=A
	@ARG
	A=D+M
	D=M
	@SP
	A=M
	M=D
	@SP
	M=M+1
// pop pointer 1
	@SP
	M=M-1
	A=M
	D=M
	@THAT
	M=D
// push constant 0
	@0
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1
// pop that 0
	@0
	D=A
	@THAT
	M=D+M
	@SP
	M=M-1
	A=M
	D=M
	@THAT
	A=M
	M=D
	@0
	D=A
	@THAT
	M=M-D
// push constant 1
	@1
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1
// pop that 1
	@1
	D=A
	@THAT
	M=D+M
	@SP
	M=M-1
	A=M
	D=M
	@THAT
	A=M
	M=D
	@1
	D=A
	@THAT
	M=M-D
// push argument 0
	@0
	D=A
	@ARG
	A=D+M
	D=M
	@SP
	A=M
	M=D
	@SP
	M=M+1
// push constant 2
	@2
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1
// sub
	@SP
	M=M-1
	@SP
	A=M
	D=M
	D=-D
	@SP
	M=M-1
	@SP
	A=M
	D=D+M
	M=D
	@SP
	M=M+1
// pop argument 0
	@0
	D=A
	@ARG
	M=D+M
	@SP
	M=M-1
	A=M
	D=M
	@ARG
	A=M
	M=D
	@0
	D=A
	@ARG
	M=M-D
// label LOOP
(LOOP)
// push argument 0
	@0
	D=A
	@ARG
	A=D+M
	D=M
	@SP
	A=M
	M=D
	@SP
	M=M+1
// if-goto COMPUTE_ELEMENT
	@SP
	A=M-1
	D=M
	@SP
	M=M-1
	@COMPUTE_ELEMENT
	D;JNE
// goto END
@END
0;JMP
// label COMPUTE_ELEMENT
(COMPUTE_ELEMENT)
// push that 0
	@0
	D=A
	@THAT
	A=D+M
	D=M
	@SP
	A=M
	M=D
	@SP
	M=M+1
// push that 1
	@1
	D=A
	@THAT
	A=D+M
	D=M
	@SP
	A=M
	M=D
	@SP
	M=M+1
// add
	@SP
	M=M-1
	@SP
	A=M
	D=M
	@SP
	M=M-1
	@SP
	A=M
	D=D+M
	M=D
	@SP
	M=M+1
// pop that 2
	@2
	D=A
	@THAT
	M=D+M
	@SP
	M=M-1
	A=M
	D=M
	@THAT
	A=M
	M=D
	@2
	D=A
	@THAT
	M=M-D
// push pointer 1
	@THAT
	D=M
	@SP
	A=M
	M=D
	@SP
	M=M+1
// push constant 1
	@1
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1
// add
	@SP
	M=M-1
	@SP
	A=M
	D=M
	@SP
	M=M-1
	@SP
	A=M
	D=D+M
	M=D
	@SP
	M=M+1
// pop pointer 1
	@SP
	M=M-1
	A=M
	D=M
	@THAT
	M=D
// push argument 0
	@0
	D=A
	@ARG
	A=D+M
	D=M
	@SP
	A=M
	M=D
	@SP
	M=M+1
// push constant 1
	@1
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1
// sub
	@SP
	M=M-1
	@SP
	A=M
	D=M
	D=-D
	@SP
	M=M-1
	@SP
	A=M
	D=D+M
	M=D
	@SP
	M=M+1
// pop argument 0
	@0
	D=A
	@ARG
	M=D+M
	@SP
	M=M-1
	A=M
	D=M
	@ARG
	A=M
	M=D
	@0
	D=A
	@ARG
	M=M-D
// goto LOOP
@LOOP
0;JMP
// label END
(END)
(END)
	@END
	0;JMP
