// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
// 本例地址用途:
// R0=屏幕最后一个字地址之后
// R1=屏幕当前写入索引
// 流程：
// 按下任意键时：如果R1>=R0不作处理，否则RAM[R1]=-1，R1++
//（-1补码正好是0xffff，我是没想到，网上查的。。另外A指令因为只有15位可用，就不行，得用C指令直接写值）
// 没有按下键时：如果R1<=SCREEN不作处理，否则R1--,RAM[R1]=0

// 初始化R0\R1
@SCREEN
D=A
@8192               // 每行32个字，一共256行
D=D+A
@R0
M=D                 // R0=SCREEN+8192
@SCREEN
D=A
@R1
M=D                 // R1=SCREEN

(LOOP)
@KBD
D=M                 // 获取键盘输入

@FILL
D;JNE

// 清屏
@SCREEN
D=A
@R1
D=D-M               // SCREEN-R1
@LOOP
D;JGE
@R1
M=M-1               // R1--
A=M
M=0                 // 清除一个字
@LOOP
0;JMP

// 填充
(FILL)
@R0
D=M
@R1
D=D-M               // R0-R1
@LOOP
D;JLE
@R1
A=M
M=-1                // 写入一个字
@R1
M=M+1               // R1++
@LOOP
0;JMP

@LOOP
0;JMP
