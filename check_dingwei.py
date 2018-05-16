import time
from pytesseract import image_to_string, pytesseract
from selenium import webdriver
from PIL import Image, ImageEnhance
from selenium.webdriver.support.select import Select


# 登陆操作
def login_action(config, driver):
    driver.save_screenshot('tmp/dingwei.png')  # 截图，方便后面ocr
    src_img = driver.find_element_by_xpath('//*[@id="img"]')

    img_left = int(src_img.location['x'])
    img_top = int(src_img.location['y'])
    img_right = int(src_img.location['x'] + src_img.size['width'])
    img_bottom = int(src_img.location['y'] + src_img.size['height'])

    img = Image.open('tmp/dingwei.png')
    img = img.crop((img_left + 1, img_top + 1, img_right - 1, img_bottom - 1))  # 分别去掉一个像素的边框，提高识别度
    # img = img.convert('L')
    img = ImageEnhance.Brightness(img).enhance(1.8)  # 提高图片的亮度，取出掉背景的杂图，只留下文字内容
    img.save('tmp/validateimg.png')

    image = Image.open('tmp/validateimg.png')
    # 在另外一台机上运行，需要使用下面注释的两行才能运行正常
    # tessdata_dir_config = '--tessdata-dir '+config.get('global', 'tessdata_path')
    # validate_num = image_to_string(image, config=tessdata_dir_config)
    validate_num = image_to_string(image)
    print('校验码识别:', image_to_string(image))
    # 一份修整表,把一些识别错误的内容给修正过来
    rep = {'><': 'x', '_': '', '|': '1', '‘': '', '}': '7', '(': 't', 'D': '0', 'Z': '2', 'S': '5',
           '\\': '', 'G': '6', '*': '', ' ': ''}
    for r in rep:
        validate_num = validate_num.replace(r, rep[r])

    print('修正后：', validate_num)
    #
    driver.find_element_by_xpath('//*[@id="username_"]').send_keys(config.get('dingwei', 'dingwei_username'))  # 用户名
    driver.find_element_by_xpath('//*[@id="password_"]').send_keys(config.get('dingwei', 'dingwei_password'))  # 密码
    driver.find_element_by_xpath('//*[@id="validateCode"]').send_keys(validate_num)  # 校验码
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div[1]/div[3]/div/div/div/a').click()  # 提交按钮


def startup(config, driver):
    # pytesseract.tesseract_cmd = config.get('global', 'tesseract_cmd_path')  # 需要导入安装的tesseract-ocr的安装地址，否则会报错

    driver.get(config.get('dingwei', 'dingwei_url'))  # 网址
    driver.save_screenshot('tmp/dingwei.png')

    login_action(config, driver)

    current_url = driver.current_url  # 获取网站，判断是否登录成功
    # print(current_url)

    # 判断网站是否登录成功，如果跳转到的网址里面包含login.action的话，表示登陆失败，需要重新执行登陆的操作
    while 'login.action' in current_url:
        login_action(config, driver)
        current_url = driver.current_url

    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="menuTab2"]').click()
    driver.switch_to.frame('mainFrame')

    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="child_menu3"]').click()

    time.sleep(2)
    driver.switch_to.frame('rightFrame')

    # 需要自动获取今天和昨天两个日期。

    now = time.time()
    before = now - 24 * 3600  # 可以改变n 的值计算n天前的
    today = time.strftime("%Y%m%d", time.localtime(now))
    yestoday = time.strftime("%Y%m%d", time.localtime(before))

    driver.find_element_by_xpath('//*[@id="startDate"]').click()
    driver.find_element_by_xpath('//*[@id="startDate"]').send_keys(yestoday)
    driver.find_element_by_xpath('//*[@id="endDate"]').click()
    driver.find_element_by_xpath('//*[@id="endDate"]').send_keys(today)
    time.sleep(2)

    position_type = Select(driver.find_element_by_xpath('//*[@id="source"]'))
    position_type.select_by_visible_text('LBMP定位')
    driver.find_element_by_xpath('//*[@id="msisdn"]').click()

    driver.find_element_by_xpath('//*[@id="searchBut"]').click()
    time.sleep(2)
    trs = driver.find_elements_by_xpath('//*[@id="searchForm"]/table[3]/tbody/tr')
    for tr in trs[:-1]:  # 最后一行不要，是页码行
        print(tr.text)
    # driver.quit()


if __name__ == '__main__':
    import configparser
    config = configparser.ConfigParser()
    config.read_file(open('config.ini', 'r'))

    driver = webdriver.Chrome(executable_path=config.get('global','chromedriver_path'))
    driver.set_window_size(1366, 768)
    driver.set_page_load_timeout(30)

    startup(config, driver)

    driver.quit()
