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
// file:FunctionCalls\FibonacciElement\Main.vm
// vm cmd:funcion Main.fibonacci 0
(Main.fibonacci)
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
// vm cmd:push constant 2
@2
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
@LABEL_AUTO_IF_TRUE_81
D;JLT
D=0
@LABEL_AUTO_IF_END_82
0;JMP
(LABEL_AUTO_IF_TRUE_81)
D=-1
(LABEL_AUTO_IF_END_82)
@SP
M=M-1
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:if-goto IF_TRUE
@SP                                // [begin]:pop stack to D
M=M-1
A=M
D=M                                // [end]:pop stack to D
@Main.fibonacci$IF_TRUE
D;JNE
// vm cmd:goto IF_FALSE
@Main.fibonacci$IF_FALSE
0;JMP
// vm cmd:label IF_TRUE
(Main.fibonacci$IF_TRUE)
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
// vm cmd:label IF_FALSE
(Main.fibonacci$IF_FALSE)
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
// vm cmd:push constant 2
@2
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
// vm cmd:call Main.fibonacci 1
@LABEL_AUTO_Main.fibonacci_CALL_Main.fibonacci_RETURN_245
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
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(LABEL_AUTO_Main.fibonacci_CALL_Main.fibonacci_RETURN_245)
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
// vm cmd:push constant 1
@1
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
// vm cmd:call Main.fibonacci 1
@LABEL_AUTO_Main.fibonacci_CALL_Main.fibonacci_RETURN_326
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
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(LABEL_AUTO_Main.fibonacci_CALL_Main.fibonacci_RETURN_326)
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
// file:FunctionCalls\FibonacciElement\Sys.vm
// vm cmd:funcion Sys.init 0
(Sys.init)
// vm cmd:push constant 4
@4
D=A
@SP                                // [begin]:push D to stack
A=M
M=D
@SP
M=M+1                              // [end]:push D to stack
// vm cmd:call Main.fibonacci 1
@LABEL_AUTO_Sys.init_CALL_Main.fibonacci_RETURN_454
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
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(LABEL_AUTO_Sys.init_CALL_Main.fibonacci_RETURN_454)
// vm cmd:label WHILE
(Sys.init$WHILE)
// vm cmd:goto WHILE
@Sys.init$WHILE
0;JMP
