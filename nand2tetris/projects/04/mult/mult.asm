// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// summary: sum of R0+R0+R0+....+R0
@i
M=0                 // i=0
@R2
M=0                 // R2=0
// LOOP begin
(LOOP)
@i
D=M
@R1
D=D-M               // i-R1
@END
D;JGE               // if (i-R1)>=0,goto END
@R0
D=M
@R2
M=D+M               // R2=R2+R0
@i
M=M+1               // i=i+1
@LOOP
0;JMP
// LOOP end
(END)
@END
0;JMP