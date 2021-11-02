// file:MemoryAccess\BasicTest\BasicTest.vm
// vm cmd:push constant 10
@10
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:pop local 0
@LCL
D=M
@0
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
// vm cmd:push constant 21
@21
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push constant 22
@22
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:pop argument 2
@ARG
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
// vm cmd:pop argument 1
@ARG
D=M
@1
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
// vm cmd:push constant 36
@36
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:pop this 6
@THIS
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
// vm cmd:push constant 42
@42
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push constant 45
@45
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:pop that 5
@THAT
D=M
@5
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
// vm cmd:pop that 2
@THAT
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
// vm cmd:push constant 510
@510
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:pop temp 6
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@R11
M=D
// vm cmd:push local 0
@LCL
D=M
@0
A=D+A
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push that 5
@THAT
D=M
@5
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
// vm cmd:push argument 1
@ARG
D=M
@1
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
// vm cmd:push this 6
@THIS
D=M
@6
A=D+A
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push this 6
@THIS
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
// vm cmd:push temp 6
@R11
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
