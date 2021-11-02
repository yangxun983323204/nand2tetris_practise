// file:MemoryAccess\StaticTest\StaticTest.vm
// vm cmd:push constant 111
@111
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push constant 333
@333
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push constant 888
@888
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:pop static 8
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@StaticTest.8
M=D
// vm cmd:pop static 3
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@StaticTest.3
M=D
// vm cmd:pop static 1
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@StaticTest.1
M=D
// vm cmd:push static 3
@StaticTest.3
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push static 1
@StaticTest.1
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
// vm cmd:push static 8
@StaticTest.8
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
