python Assembler.py add\add.asm
python Assembler.py max\max.asm
python Assembler.py max\maxL.asm
python Assembler.py pong\pong.asm
python Assembler.py pong\pongL.asm
python Assembler.py rect\rect.asm
python Assembler.py rect\rectL.asm
echo off
echo 比较生成文件
echo add\add.asm
fc add\add.hack add\add_yx.hack >nul
if %errorlevel%==0 (echo 完全相同) else (echo 不相同)
echo max\max.asm
fc max\max.hack max\max_yx.hack >nul
if %errorlevel%==0 (echo 完全相同) else (echo 不相同)
echo max\maxL.asm
fc max\maxL.hack max\maxL_yx.hack >nul
if %errorlevel%==0 (echo 完全相同) else (echo 不相同)
echo pong\pong.asm
fc pong\pong.hack pong\pong_yx.hack >nul
if %errorlevel%==0 (echo 完全相同) else (echo 不相同)
echo pong\pongL.asm
fc pong\pong.hack pong\pong_yx.hack >nul
if %errorlevel%==0 (echo 完全相同) else (echo 不相同)
echo rect\rect.asm
fc rect\rect.hack rect\rect_yx.hack >nul
if %errorlevel%==0 (echo 完全相同) else (echo 不相同)
echo rect\rectL.asm
fc rect\rectL.hack rect\rectL_yx.hack >nul
if %errorlevel%==0 (echo 完全相同) else (echo 不相同)