import time

import cv2
from pytesseract import image_to_string, pytesseract
from selenium import webdriver
from PIL import Image, ImageEnhance
from Setting import Setting

setting = Setting()


def login_action(driver):
    driver.save_screenshot('tmp/tmp.png')  # 截图，为后面的获取校验码准备

    # 获取校验码区域，并计算出四个值，后面用这些值，裁剪截图，得到校验码，用于ocr
    source_image = driver.find_element_by_xpath('//*[@id="imgLoginCode"]')
    img_left = int(source_image.location['x'])
    img_top = int(source_image.location['y'])
    img_right = int(source_image.location['x'] + source_image.size['width'])
    img_bottom = int(source_image.location['y'] + source_image.size['height'])

    # 裁剪区域，得到验证码的部分，用于后面ocr
    im = Image.open('tmp/tmp.png')
    im = im.crop((img_left + 1, img_top + 1, img_right - 1, img_bottom - 1))
    # im = im.convert('L')  # 提高亮度和黑白话，在一定程度上，提高了识别度
    im = ImageEnhance.Brightness(im).enhance(1.8)  # 提高图片的亮度，取出掉背景的杂图，只留下文字内容
    im.save('tmp/jiaoyanma.png')

    img = cv2.imread('tmp/jiaoyanma.png')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度化
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 1)  # 二值化

    # 去噪声处理

    # 线降噪
    h, w = img.shape[:2]
    for y in range(1, w - 1):
        for x in range(1, h - 1):
            count = 0
            if img[x, y - 1] > 245:
                count = count + 1
            if img[x, y + 1] > 245:
                count = count + 1
            if img[x - 1, y] > 245:
                count = count + 1
            if img[x + 1, y] > 245:
                count = count + 1
            if count > 2:
                img[x, y] = 255

    # 点降噪
    cur_pixel = img[x, y]  # 当前像素点的值
    height, width = img.shape[:2]

    for y in range(0, width - 1):
        for x in range(0, height - 1):
            if y == 0:  # 第一行
                if x == 0:  # 左上顶点,4邻域
                    # 中心点旁边3个点
                    sum = int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x + 1, y]) \
                          + int(img[x + 1, y + 1])
                    if sum <= 2 * 245:
                        img[x, y] = 0
                elif x == height - 1:  # 右上顶点
                    sum = int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x - 1, y]) \
                          + int(img[x - 1, y + 1])
                    if sum <= 2 * 245:
                        img[x, y] = 0
                else:  # 最上非顶点,6邻域
                    sum = int(img[x - 1, y]) \
                          + int(img[x - 1, y + 1]) \
                          + int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x + 1, y]) \
                          + int(img[x + 1, y + 1])
                    if sum <= 3 * 245:
                        img[x, y] = 0
            elif y == width - 1:  # 最下面一行
                if x == 0:  # 左下顶点
                    # 中心点旁边3个点
                    sum = int(cur_pixel) \
                          + int(img[x + 1, y]) \
                          + int(img[x + 1, y - 1]) \
                          + int(img[x, y - 1])
                    if sum <= 2 * 245:
                        img[x, y] = 0
                elif x == height - 1:  # 右下顶点
                    sum = int(cur_pixel) \
                          + int(img[x, y - 1]) \
                          + int(img[x - 1, y]) \
                          + int(img[x - 1, y - 1])

                    if sum <= 2 * 245:
                        img[x, y] = 0
                else:  # 最下非顶点,6邻域
                    sum = int(cur_pixel) \
                          + int(img[x - 1, y]) \
                          + int(img[x + 1, y]) \
                          + int(img[x, y - 1]) \
                          + int(img[x - 1, y - 1]) \
                          + int(img[x + 1, y - 1])
                    if sum <= 3 * 245:
                        img[x, y] = 0
            else:  # y不在边界
                if x == 0:  # 左边非顶点
                    sum = int(img[x, y - 1]) \
                          + int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x + 1, y - 1]) \
                          + int(img[x + 1, y]) \
                          + int(img[x + 1, y + 1])

                    if sum <= 3 * 245:
                        img[x, y] = 0
                elif x == height - 1:  # 右边非顶点
                    sum = int(img[x, y - 1]) \
                          + int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x - 1, y - 1]) \
                          + int(img[x - 1, y]) \
                          + int(img[x - 1, y + 1])

                    if sum <= 3 * 245:
                        img[x, y] = 0
                else:  # 具备9领域条件的
                    sum = int(img[x - 1, y - 1]) \
                          + int(img[x - 1, y]) \
                          + int(img[x - 1, y + 1]) \
                          + int(img[x, y - 1]) \
                          + int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x + 1, y - 1]) \
                          + int(img[x + 1, y]) \
                          + int(img[x + 1, y + 1])
                    if sum <= 4 * 245:
                        img[x, y] = 0

    cv2.imwrite('tmp/jiaoyanma2.png', img)

    '''
    ocr识别功能可用，但是，需要访问的站点的校验码图片需要先做处理
    校验码的ocr功能可用，但准确率还有待提高，目前的误差还很大
    '''
    image = Image.open('tmp/jiaoyanma2.png')

    check_code = image_to_string(image).strip()
    print('未修正校验码识别:', check_code)
    # 一份修整表
    rep = {'><': 'x', '_': '', '|': '1', '‘': '', '}': '7', '|': '1',
           '\\': '', 'G': '6', 'fi': '5', "1'": 'f', '*': '', ' ': ''}
    for r in rep:
        check_code = check_code.replace(r, rep[r])

    print('修正后的校验码识别:', check_code)

    username = setting.xietong_username
    password = setting.xietong_password

    driver.find_element_by_xpath('//*[@id="txtUserName"]').clear()  # 先清空输入框
    driver.find_element_by_xpath('//*[@id="txtUserName"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="txtUserPWD"]').clear()  # 先清空输入框
    driver.find_element_by_xpath('//*[@id="txtUserPWD"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="txtLoginCode"]').clear()  # 先清空输入框
    driver.find_element_by_xpath('//*[@id="txtLoginCode"]').send_keys(check_code)
    driver.find_element_by_xpath('//*[@id="lbtnLogin"]/img').click()

def startup():
    pytesseract.tesseract_cmd = setting.tesseract_cmd_path  # 需要导入安装的tesseract-ocr的安装地址，否则会报错

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


    login_action(driver)

    current_url = driver.current_url
    time.sleep(2)

    while 'Login.aspx' in current_url:
        login_action(driver)
        current_url = driver.current_url
        time.sleep(2)
        if current_url == setting.xietong_url2:
            break

    driver.get(setting.xietong_url3)
    driver.find_element_by_xpath('//*[@id="urtrackerTd"]/table/tbody/tr[1]/td/a/img').click()
    driver.find_element_by_xpath('//*[@id="Siteheader1_lnkConfig"]').click()

    print(driver.find_element_by_xpath('//*[@id="CP1_CP1_lblSmsState"]').text)

    driver.quit()


if __name__ == '__main__':
    startup()
