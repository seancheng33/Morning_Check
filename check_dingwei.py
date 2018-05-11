import time
from Setting import Setting
from pytesseract import image_to_string, pytesseract
from selenium import webdriver
from PIL import Image, ImageEnhance

setting = Setting()
pytesseract.tesseract_cmd = setting.tesseract_cmd_path  # 需要导入安装的tesseract-ocr的安装地址，否则会报错

# 无GUI的浏览器phantomjs
# driver = webdriver.PhantomJS(executable_path="./lib/phantomjs.exe", desired_capabilities=cap)
driver = webdriver.Chrome(executable_path=setting.chromedriver_path)
driver.set_window_size(1366, 768)
driver.set_page_load_timeout(30)

driver.get(setting.dingwei_url)  # 网址
driver.save_screenshot('tmp/dingwei.png')

src_img = driver.find_element_by_xpath('//*[@id="img"]')

img_left = int(src_img.location['x'])
img_top = int(src_img.location['y'])
img_right = int(src_img.location['x'] + src_img.size['width'])
img_bottom = int(src_img.location['y'] + src_img.size['height'])

img = Image.open('tmp/dingwei.png')
img = img.crop((img_left+1, img_top+1, img_right-1, img_bottom-1))#分别去掉一个像素的边框，提高识别度
# img = img.convert('L')
img = ImageEnhance.Brightness(img).enhance(1.8)  # 提高图片的亮度，取出掉背景的杂图，只留下文字内容
img.save('tmp/validateimg.png')

image = Image.open('tmp/validateimg.png')
validate_num = image_to_string(image)
print('校验码识别:', image_to_string(image))
# 一份修整表
rep = {'><': 'x', '_': '', '|': '1', '‘': '', '}': '7',
       '\\': '', 'G': '6', 'fi': '5', "1'": 'f', '*': '', ' ': ''}
for r in rep:
    validate_num = validate_num.replace(r, rep[r])

print('修正后：', validate_num)
#
driver.find_element_by_xpath('//*[@id="username_"]').send_keys(setting.dingwei_username) # 用户名
driver.find_element_by_xpath('//*[@id="password_"]').send_keys(setting.dingwei_password) # 密码
driver.find_element_by_xpath('//*[@id="validateCode"]').send_keys(validate_num) # 校验码
driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div[1]/div[3]/div/div/div/a').click() # 提交按钮
# print(setting.dingwei_username, setting.dingwei_password)

driver.find_element_by_xpath('//*[@id="menuTab2"]').click()
time.sleep(5)
driver.get(setting.dingwei_url+setting.dingwei_target_url)

driver.find_element_by_xpath('//*[@id="searchBut"]').click()



# driver.quit()

# if __name__ == '__main__':
#     pass
