'''
主入口
'''
from pytesseract import pytesseract
from selenium import webdriver

import sql_service_check
import check_dingwei
import check_xietong

if __name__ == '__main__':
    import configparser
    config = configparser.ConfigParser()
    config.read_file(open('config.ini', 'r'))

    pytesseract.tesseract_cmd = config.get('global', 'tesseract_cmd_path')  # 需要导入安装的tesseract-ocr的安装地址，否则会报错

    # # 浏览器头的内容
    # userAgent = (
    #     "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    # cap = webdriver.DesiredCapabilities.PHANTOMJS
    # cap["phantomjs.page.settings.resourceTimeout"] = 100
    # cap["phantomjs.page.settings.userAgent"] = userAgent
    # cap["phantomjs.page.customHeaders.User-Agent"] = userAgent

    # 无GUI的浏览器phantomjs
    # driver = webdriver.PhantomJS(executable_path="./lib/phantomjs.exe", desired_capabilities=cap)
    driver = webdriver.Chrome(executable_path=config.get('global','chromedriver_path'))
    driver.set_window_size(1366, 768)
    driver.set_page_load_timeout(30)

    sql_service_check.main(config)
    check_xietong.startup(config, driver)
    check_dingwei.startup(config, driver)

    driver.quit()