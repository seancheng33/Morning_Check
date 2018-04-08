import time
from Setting import Setting
from pytesseract import image_to_string
from selenium import webdriver
from PIL import Image, ImageEnhance


setting = Setting()
# 无GUI的浏览器phantomjs
# driver = webdriver.PhantomJS(executable_path="./lib/phantomjs.exe", desired_capabilities=cap)
driver = webdriver.Chrome(executable_path=setting.chromedriver_path)
driver.set_window_size(1366, 768)
driver.set_page_load_timeout(30)

driver.get(setting.dingwei_url)  # 网址
driver.save_screenshot('dingwei.png')

src_img = driver.find_element_by_xpath('//*[@id="img"]')

img_left = int(src_img.location['x'])
img_top = int(src_img.location['y'])
img_right = int(src_img.location['x'] + src_img.size['width'])
img_bottom = int(src_img.location['y'] + src_img.size['height'])

img = Image.open('dingwei.png')
img = img.crop((img_left+1, img_top+1, img_right-1, img_bottom-1))#分别去掉一个像素的边框，提高识别度
# img = img.convert('L')
img = ImageEnhance.Brightness(img).enhance(1.8)  # 提高图片的亮度，取出掉背景的杂图，只留下文字内容
img.save('validateimg.png')

image = Image.open('validateimg.png')
validate_num = image_to_string(image)
print('校验码识别:', image_to_string(image))

#
driver.find_element_by_xpath('//*[@id="username_"]').send_keys(setting.dingwei_username) # 用户名
driver.find_element_by_xpath('//*[@id="password_"]').send_keys(setting.dingwei_password) # 密码
driver.find_element_by_xpath('//*[@id="validateCode"]').send_keys(validate_num) # 校验码
driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div[1]/div[3]/div/div/div/a').submit() # 提交按钮
print(setting.dingwei_username,setting.dingwei_password)

driver.find_element_by_xpath('//*[@id="menuTab2"]').click()
time.sleep(5)
# 这步点击报错，元素没有找到？
print(driver.find_element_by_xpath('//*[@id="child_menu3"]')).submit()
# 改为分析抓包，直接requests获取内容




# driver.quit()

# if __name__ == '__main__':
#     pass
