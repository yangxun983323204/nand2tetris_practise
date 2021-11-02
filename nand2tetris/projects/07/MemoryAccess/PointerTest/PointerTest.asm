// file:MemoryAccess\PointerTest\PointerTest.vm
// vm cmd:push constant 3030
@3030
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:pop pointer 0
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@R3
M=D
// vm cmd:push constant 3040
@3040
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:pop pointer 1
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@R4
M=D
// vm cmd:push constant 32
@32
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:pop this 2
@THIS
D=M
@2
D=D+A
@R13
M=D
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@R13
A=M
M=D
// vm cmd:push constant 46
@46
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:pop that 6
@THAT
D=M
@6
D=D+A
@R13
M=D
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@R13
A=M
M=D
// vm cmd:push pointer 0
@R3
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push pointer 1
@R4
D=M
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
// vm cmd:push this 2
@THIS
D=M
@2
A=D+A
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:sub
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@SP
A=M
A=A-1
D=M-D                              // sub
@SP
M=M-1
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push that 6
@THAT
D=M
@6
A=D+A
D=M
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
