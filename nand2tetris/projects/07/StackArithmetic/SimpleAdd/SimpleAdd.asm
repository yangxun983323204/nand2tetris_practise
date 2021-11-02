// file:StackArithmetic\SimpleAdd\SimpleAdd.vm
// vm cmd:push constant 7
@7
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push constant 8
@8
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:add
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@SP
A=M
A=A-1
D=D+M                              // add
@SP
M=M-1
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
