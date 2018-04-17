from pytesseract import image_to_string
from selenium import webdriver
from PIL import Image, ImageEnhance

from Setting import Setting
setting = Setting()

# 浏览器头的内容
userAgent = (
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
cap = webdriver.DesiredCapabilities.PHANTOMJS
cap["phantomjs.page.settings.resourceTimeout"] = 100
cap["phantomjs.page.settings.userAgent"] = userAgent
cap["phantomjs.page.customHeaders.User-Agent"] = userAgent

# 无GUI的浏览器phantomjs
# driver = webdriver.PhantomJS(executable_path="./lib/phantomjs.exe", desired_capabilities=cap)
driver = webdriver.Chrome(executable_path=setting.chromedriver_path)
driver.set_window_size(1366, 768)
# driver.set_page_load_timeout(30)
driver.get(setting.xietong_url1)
driver.save_screenshot('tmp.png')  # 截图，为后面的获取校验码准备

# 获取校验码区域，并计算出四个值，后面用这些值，裁剪截图，得到校验码，用于ocr
source_image = driver.find_element_by_xpath('//*[@id="imgLoginCode"]')
img_left = int(source_image.location['x'])
img_top = int(source_image.location['y'])
img_right = int(source_image.location['x'] + source_image.size['width'])
img_bottom = int(source_image.location['y'] + source_image.size['height'])

# 裁剪区域，得到验证码的部分，用于后面ocr
im = Image.open('tmp.png')
im = im.crop((img_left, img_top, img_right, img_bottom))
im = im.convert('L')  # 提高亮度和黑白话，在一定程度上，提高了识别度
im = ImageEnhance.Brightness(im).enhance(1.8)  # 提高图片的亮度，取出掉背景的杂图，只留下文字内容
im.save('jiaoyanma.png')

'''
ocr识别功能可用，但是，需要访问的站点的校验码图片需要先做处理
校验码的ocr功能可用，但准确率还有待提高，目前的误差还很大
'''
image = Image.open('jiaoyanma.png')

print('校验码识别:', image_to_string(image).strip())
check_code = image_to_string(image).strip()
username = setting.xietong_username
password = setting.xietong_password
print(username,password)
if len(check_code) == 5:
    driver.find_element_by_xpath('//*[@id="txtUserName"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="txtUserPWD"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="txtLoginCode"]').send_keys(check_code)
    driver.find_element_by_xpath('//*[@id="lbtnLogin"]/img').click()
else:
    check_code = check_code.replace('’', '').replace('.', '')
    driver.find_element_by_xpath('//*[@id="txtUserName"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="txtUserPWD"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="txtLoginCode"]').send_keys(check_code)
    driver.find_element_by_xpath('//*[@id="lbtnLogin"]/img').click()

if driver.current_url == setting.xietong_url2:
    driver.get(setting.xietong_url3)
    driver.find_element_by_xpath('//*[@id="urtrackerTd"]/table/tbody/tr[1]/td/a/img').click()
    driver.find_element_by_xpath('//*[@id="Siteheader1_lnkConfig"]').click()

    print(driver.find_element_by_xpath('//*[@id="CP1_CP1_lblSmsState"]').text)

driver.quit()
# if __name__ == '__main__':
#     pass
