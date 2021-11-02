// file:StackArithmetic\StackTest\StackTest.vm
// vm cmd:push constant 17
@17
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push constant 17
@17
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:eq
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@SP
A=M
A=A-1
D=M-D                              // eq
@LABEL_AUTO_IF_TRUE_27
D;JEQ
D=0
@LABEL_AUTO_IF_END_28
0;JMP
(LABEL_AUTO_IF_TRUE_27)
D=-1
(LABEL_AUTO_IF_END_28)
@SP
M=M-1
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push constant 17
@17
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push constant 16
@16
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:eq
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@SP
A=M
A=A-1
D=M-D                              // eq
@LABEL_AUTO_IF_TRUE_62
D;JEQ
D=0
@LABEL_AUTO_IF_END_63
0;JMP
(LABEL_AUTO_IF_TRUE_62)
D=-1
(LABEL_AUTO_IF_END_63)
@SP
M=M-1
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push constant 16
@16
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push constant 17
@17
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:eq
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@SP
A=M
A=A-1
D=M-D                              // eq
@LABEL_AUTO_IF_TRUE_97
D;JEQ
D=0
@LABEL_AUTO_IF_END_98
0;JMP
(LABEL_AUTO_IF_TRUE_97)
D=-1
(LABEL_AUTO_IF_END_98)
@SP
M=M-1
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push constant 892
@892
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push constant 891
@891
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:lt
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@SP
A=M
A=A-1
D=M-D                              // lt
@LABEL_AUTO_IF_TRUE_132
D;JLT
D=0
@LABEL_AUTO_IF_END_133
0;JMP
(LABEL_AUTO_IF_TRUE_132)
D=-1
(LABEL_AUTO_IF_END_133)
@SP
M=M-1
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push constant 891
@891
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push constant 892
@892
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:lt
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@SP
A=M
A=A-1
D=M-D                              // lt
@LABEL_AUTO_IF_TRUE_167
D;JLT
D=0
@LABEL_AUTO_IF_END_168
0;JMP
(LABEL_AUTO_IF_TRUE_167)
D=-1
(LABEL_AUTO_IF_END_168)
@SP
M=M-1
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push constant 891
@891
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push constant 891
@891
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:lt
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@SP
A=M
A=A-1
D=M-D                              // lt
@LABEL_AUTO_IF_TRUE_202
D;JLT
D=0
@LABEL_AUTO_IF_END_203
0;JMP
(LABEL_AUTO_IF_TRUE_202)
D=-1
(LABEL_AUTO_IF_END_203)
@SP
M=M-1
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push constant 32767
@32767
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push constant 32766
@32766
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:gt
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@SP
A=M
A=A-1
D=M-D                              // gt
@LABEL_AUTO_IF_TRUE_237
D;JGT
D=0
@LABEL_AUTO_IF_END_238
0;JMP
(LABEL_AUTO_IF_TRUE_237)
D=-1
(LABEL_AUTO_IF_END_238)
@SP
M=M-1
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push constant 32766
@32766
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push constant 32767
@32767
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:gt
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@SP
A=M
A=A-1
D=M-D                              // gt
@LABEL_AUTO_IF_TRUE_272
D;JGT
D=0
@LABEL_AUTO_IF_END_273
0;JMP
(LABEL_AUTO_IF_TRUE_272)
D=-1
(LABEL_AUTO_IF_END_273)
@SP
M=M-1
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push constant 32766
@32766
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push constant 32766
@32766
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:gt
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@SP
A=M
A=A-1
D=M-D                              // gt
@LABEL_AUTO_IF_TRUE_307
D;JGT
D=0
@LABEL_AUTO_IF_END_308
0;JMP
(LABEL_AUTO_IF_TRUE_307)
D=-1
(LABEL_AUTO_IF_END_308)
@SP
M=M-1
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push constant 57
@57
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push constant 31
@31
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push constant 53
@53
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
// vm cmd:push constant 112
@112
D=A
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
// vm cmd:neg
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
D=-D                               // neg
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:and
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@SP
A=M
A=A-1
D=D&M                              // and
@SP
M=M-1
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push constant 82
@82
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:or
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@SP
A=M
A=A-1
D=D|M                              // or
@SP
M=M-1
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:not
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
D=!D                               // not
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
