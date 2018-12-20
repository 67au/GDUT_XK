# GDUT_XK

一个被垃圾通知气出来的垃圾脚本。(处于勉强能用阶段)

## 使用说明

使用 Generator.py 生成需要抢的科目的配置和登录用的cookies
```bash
python3 Generator.py
```
使用 xk.py 开始发送抢课请求，Ctrl+C停止运行（在使用过程之中出现问题的时候，大概就会开发多线程的版本）
```bash
python3 Generator.py
```
在开始抢课前5分钟先生成配置，在开始抢课前1分钟发送请求抢课，这样效果最好。默认使用教务系统的带验证码的登录方式，修改上面提及的文件开头可以使用被教务系统隐藏的统一认证登录方式，以便在无法查看验证码照片的设备使用。

## 所需依赖
```bash
pip3 install bs4
pip3 install lxml
pip3 install requests
pip3 install pycrypto
```
