# <center>计算机系统要素-练习</center>

----------

### 官方网站  
[https://www.nand2tetris.org/](https://www.nand2tetris.org/)  
### 使用说明  
运行工具前安装最新的java运行环境，我遇到了在较低版本有乱码情况。  

### 第一章  
需要逻辑代数基本知识，并结合书中布尔代数一节的规范表示法来推导：  
例如：`$dmux=(in*\overline{sel},in*sel)$`  
因此它的代码是：  
``` hdl  
CHIP DMux {
    IN in, sel;
    OUT a, b;

    PARTS:
    // Put your code here:
    Not(in=sel,out=nsel);
    And(a=in,b=nsel,out=a);
    And(a=in,b=sel,out=b);
}
```  

注意在硬件模拟器中，数组是低位在前，例如：  
`值0x001,在数组中是[1][0][0]`

![逻辑运算法则](./img/bool_op.png)  
![逻辑运算基本定理](./img/bool_law.png)  