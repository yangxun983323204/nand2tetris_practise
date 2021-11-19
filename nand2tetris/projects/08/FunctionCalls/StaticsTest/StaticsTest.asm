// ====Init begin====
@256
D=A
@SP
M=D
// vm cmd:call Sys.init 0
@LABEL_AUTO_global_CALL_Sys.init_RETURN_51
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
@LCL
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
@ARG
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
@THIS
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
@THAT
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
@SP
D=M
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(LABEL_AUTO_global_CALL_Sys.init_RETURN_51)
// ====Init end====
// file:FunctionCalls\StaticsTest\Class1.vm
// vm cmd:funcion Class1.set 0
(Class1.set)
// vm cmd:push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:pop static 0
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@Class1.0
M=D
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
// vm cmd:pop static 1
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@Class1.1
M=D
// vm cmd:push constant 0
@0
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:return
@LCL
D=M
@R13
M=D
@5
D=D-A
A=D
D=M
@R14
M=D
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@ARG
A=M
M=D
@ARG
D=M
D=D+1
@SP
M=D
@R13
D=M
@R13
M=D-1
A=M
D=M
@THAT
M=D
@R13
D=M
@R13
M=D-1
A=M
D=M
@THIS
M=D
@R13
D=M
@R13
M=D-1
A=M
D=M
@ARG
M=D
@R13
D=M
@R13
M=D-1
A=M
D=M
@LCL
M=D
@R14
A=M
0;JMP
// vm cmd:funcion Class1.get 0
(Class1.get)
// vm cmd:push static 0
@Class1.0
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push static 1
@Class1.1
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
// vm cmd:return
@LCL
D=M
@R13
M=D
@5
D=D-A
A=D
D=M
@R14
M=D
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@ARG
A=M
M=D
@ARG
D=M
D=D+1
@SP
M=D
@R13
D=M
@R13
M=D-1
A=M
D=M
@THAT
M=D
@R13
D=M
@R13
M=D-1
A=M
D=M
@THIS
M=D
@R13
D=M
@R13
M=D-1
A=M
D=M
@ARG
M=D
@R13
D=M
@R13
M=D-1
A=M
D=M
@LCL
M=D
@R14
A=M
0;JMP
// file:FunctionCalls\StaticsTest\Class2.vm
// vm cmd:funcion Class2.set 0
(Class2.set)
// vm cmd:push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:pop static 0
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@Class2.0
M=D
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
// vm cmd:pop static 1
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@Class2.1
M=D
// vm cmd:push constant 0
@0
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:return
@LCL
D=M
@R13
M=D
@5
D=D-A
A=D
D=M
@R14
M=D
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@ARG
A=M
M=D
@ARG
D=M
D=D+1
@SP
M=D
@R13
D=M
@R13
M=D-1
A=M
D=M
@THAT
M=D
@R13
D=M
@R13
M=D-1
A=M
D=M
@THIS
M=D
@R13
D=M
@R13
M=D-1
A=M
D=M
@ARG
M=D
@R13
D=M
@R13
M=D-1
A=M
D=M
@LCL
M=D
@R14
A=M
0;JMP
// vm cmd:funcion Class2.get 0
(Class2.get)
// vm cmd:push static 0
@Class2.0
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push static 1
@Class2.1
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
// vm cmd:return
@LCL
D=M
@R13
M=D
@5
D=D-A
A=D
D=M
@R14
M=D
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@ARG
A=M
M=D
@ARG
D=M
D=D+1
@SP
M=D
@R13
D=M
@R13
M=D-1
A=M
D=M
@THAT
M=D
@R13
D=M
@R13
M=D-1
A=M
D=M
@THIS
M=D
@R13
D=M
@R13
M=D-1
A=M
D=M
@ARG
M=D
@R13
D=M
@R13
M=D-1
A=M
D=M
@LCL
M=D
@R14
A=M
0;JMP
// file:FunctionCalls\StaticsTest\Sys.vm
// vm cmd:funcion Sys.init 0
(Sys.init)
// vm cmd:push constant 6
@6
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
// vm cmd:call Class1.set 2
@LABEL_AUTO_Sys.init_CALL_Class1.set_RETURN_478
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
@LCL
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
@ARG
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
@THIS
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
@THAT
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
@SP
D=M
@2
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.set
0;JMP
(LABEL_AUTO_Sys.init_CALL_Class1.set_RETURN_478)
// vm cmd:pop temp 0
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@R5
M=D
// vm cmd:push constant 23
@23
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:push constant 15
@15
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:call Class2.set 2
@LABEL_AUTO_Sys.init_CALL_Class2.set_RETURN_547
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
@LCL
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
@ARG
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
@THIS
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
@THAT
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
@SP
D=M
@2
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.set
0;JMP
(LABEL_AUTO_Sys.init_CALL_Class2.set_RETURN_547)
// vm cmd:pop temp 0
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@R5
M=D
// vm cmd:call Class1.get 0
@LABEL_AUTO_Sys.init_CALL_Class1.get_RETURN_600
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
@LCL
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
@ARG
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
@THIS
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
@THAT
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
@SP
D=M
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.get
0;JMP
(LABEL_AUTO_Sys.init_CALL_Class1.get_RETURN_600)
// vm cmd:call Class2.get 0
@LABEL_AUTO_Sys.init_CALL_Class2.get_RETURN_647
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
@LCL
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
@ARG
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
@THIS
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
@THAT
D=M
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
@SP
D=M
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.get
0;JMP
(LABEL_AUTO_Sys.init_CALL_Class2.get_RETURN_647)
// vm cmd:label WHILE
(Sys.init$WHILE)
// vm cmd:goto WHILE
@Sys.init$WHILE
0;JMP
