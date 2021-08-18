# <center>计算机系统要素-练习</center>

----------

### 官方网站  
[https://www.nand2tetris.org/](https://www.nand2tetris.org/)  
### 使用说明  
运行工具前安装最新的java运行环境，我遇到了在较低版本有乱码情况。  

### 第一章  
需要逻辑代数基本知识，并结合书中布尔代数一节的规范表示法来推导：  
例如：  
<img src="https://latex.codecogs.com/svg.latex?dmux=(in*\overline{sel},in*sel)" />  
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

### 第二章  
最重要是注意附录A对HDL语法的说明，A.5.2和A.5.3。其中说明的输入管脚也可以是常量true或false,并且可以x[i..j]=true的方式批量对多位赋值。  
ALU的逻辑实现比想像中简单，因为书里给出的ALU已经是精心设计过的，每一种输入信号的组合和对应的功能都已经列清楚了。  
有两个心得：  
1、逻辑门不存在高层逻辑中if那种跳过分支的效果，需要同时计算if的所有分支，然后用Mux选择其中一个输出。  
2、判断一个16位数是否为0和是否是负数，我是采用了对其加另一个适当的数，然后用其进位来做选择。因此我还修改了Add16.hdl的输出定义，增加了carry输出。不知道是否有更好的办法。(看到网上资料采用的Or16Way，不过第一章并未实现这个芯片)  

### 第三章  
在网上资料看到了一个被调用芯片的输出管脚可以同时连接内部管脚和输出管脚，这是我没想到的。  
例如`DFF(in=in,out=loop,out=out);`，DFF的out同时连到了一个内部管脚loop和输出管脚out。如果直接用输出管脚去连接到其它调用芯片的输入管脚是会报错的。前面的章节因为我不知道这个，还绕了些弯去解决。  
RAM8思路：用DMux8Way把load信号分解成8路信号，用来控制8个Register读写，然后用Mux8Way16选择Register的8路输出其中一路。  
RAM16思路：address是6位，高3位用在RAM16本身，用于分解load信号到8路，控制8个RAM8读写；低3位传入RAM8用于RAM8的内部选择逻辑。   
PC芯片确实有点复杂，思路是：Register在reset\load\inc时，都是需要读入数据的，并且我们应结合控制位为它构造合适的数据。reset优先级最高，其次是!reset&load，再次是!reset&!load&inc，最低是!reset&!load&!inc 