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

## 开发进度
1. 大协同的网页登陆只要再完成校验码的图片获取，就可以完成功能
2. 定位平台同理
3. 连接sql server读取存储过程，pymssql直接用指针的callproc方法调用存储过程，就可以返回值。已经实现并返回值

## 待做列表
1. 验证码的问题，尝试改为chrome的headless模式，然后在验证码右键图片另存为，保存图片下来，然后再ocr，再填回去
2. 校验码的ocr的正确度问题。还是有待提高。
3. 貌似可以用wypython来做 连接mstsc以后的操作。但是操作后的取值?
4. 页面连接是否正常的判断，也需要

## 待思考处理项
1. 定位系统的某些元素获取失败，修改为分析抓包，然后使用requests获取。