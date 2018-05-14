## 开发及使用手册

* 需要另外安装tesseract-ocr才可以使用ocr的功能,下载地址：<br/>http://jaist.dl.sourceforge.net/project/tesseract-ocr-alt/tesseract-ocr-setup-3.02.02.exe
* 需要使用到phantomjs
* 需要pytesseract库，pillow库
* pytesseract需要修改里面的tesseract_cmd='tesseract'修改为tesseract-ocr的安装路径
* selenium的版本不能高于3.9，超过3.9的版本将不再支持phantomjs，改用chrome的headless模式，需要chrome版本60或以上
* pymssql的库用于连接 sql server
* requirements.txt文件里面为必须的外部库

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


## 开发进度
1. 大协同的网页登陆完成校验码的图片获取，完成功能，但是ocr的准确度不高，
做一个循环，只要是登陆失败，就重复登陆的动作，包括重新获取校验码，直到登陆成功。
2. 定位平台同理
3. 连接sql server读取存储过程，pymssql直接用指针的callproc方法调用存储过程，
就可以返回值。已经实现并返回值

## 待做列表
1. 使用正则表达式来检验验证码的位数，和处理掉多余的符号
5. tesseract-ocr能否使用免安装版，方便到时一起打包

## 待思考处理项
1. 定位系统的某些元素获取失败，修改为分析抓包，然后使用requests获取。
2. 将结果汇总成邮件发出？