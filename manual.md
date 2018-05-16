## 开发及使用手册

* 需要另外安装tesseract-ocr才可以使用ocr的功能,下载地址：<br/>http://jaist.dl.sourceforge.net/project/tesseract-ocr-alt/tesseract-ocr-setup-3.02.02.exe
* 需要使用到phantomjs
* 需要pytesseract库，pillow库，opencv库
* pytesseract需要修改里面的tesseract_cmd='tesseract'修改为tesseract-ocr的安装路径，
也可以直接将这个路径配置在脚本中，添加pytesseract.tesseract_cmd = 'tesseract-ocr的安装路径'，同样可以达到效果，
这里采用的是第二种中办法。
* selenium的版本不能高于3.9，超过3.9的版本将不再支持phantomjs，改用chrome的headless模式，需要chrome版本60或以上
* pymssql的库用于连接 sql server
* requirements.txt文件里面为必须的外部库

## 当前版本
目前此版本为beta版。

## 所需外部库
> Pillow==5.0.0<br/>
> pymssql==2.1.3<br/>
> pytesseract==0.2.0<br/>
> selenium==3.9.0<br/>
> numpy==1.14.3<br/>
> opencv-python==3.4.0.12<br/>


有访问网络的权限情况下，也可以通过下面的命令直接安装
```
pip install -r requirements.txt
```

## 整体文件夹结构
* lib文件夹 存放webdriver的外部插件，这里后续也可能添加其他的外部运行库
* tmp文件夹 存储需要校验的验证码的临时文件夹，网页的截图和裁剪后验证码，就是存放在这个文件夹里面
* data文件夹 存储收集后的状态的文件夹
* log文件夹 日志文件的文件夹（待定）
* CheckMain.py 主程序入口（未完成）
* check_xietong.py 检查大协同的脚本
* check_dingwei.py 检查定位系统的脚本
* sql_service_check.py 检查sql server的脚本
* setting.py 配置文件
* requitements.txt 本项目所需的外部库文档
* manual.md 本文件，本应用的说明文档和开发记录文档

## 开发进度
1. 大协同的网页登陆完成校验码的图片获取，完成功能，但是ocr的准确度不高，
做一个循环，只要是登陆失败，就重复登陆的动作，包括重新获取校验码，直到登陆成功。
2. 定位平台同理，定位平台的校验码相对比较好处理，不需要和大协同一样使用opencv做较复杂的处理，
直接使用了pillow将图片的亮度提高，就得到了正确率很高的结果。
3. 连接sql server读取存储过程，pymssql直接用指针的callproc方法调用存储过程，
就可以返回值。已经实现并返回值

## 待做列表
1. 使用正则表达式来检验验证码的位数，和处理掉多余的符号
2. tesseract-ocr能否使用免安装版，方便到时一起打包

## 待思考处理项
1. 定位系统的某些元素获取失败，修改为分析抓包，然后使用requests获取。
2. 将结果汇总成邮件发出？
3. 添加网页打开的状态码？如果返回200才继续后面的内容，否则就间隔数秒重试N次，N次后还是返回非200的状态码，就说明网站访问有问题。保存此次访问记录
4. 添加运行日志。方便排查错误。
5. 配置还是使用配置文件比较合理，不要写在一个py文件中，使用configparse库，这样的条理比较清晰
6. 改为部署在docker里面？因为移植程序的确有点小问题

## 更新历史
