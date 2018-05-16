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

    driver = webdriver.Chrome(executable_path=config.get('global','chromedriver_path'))
    driver.set_window_size(1366, 768)
    # driver.set_page_load_timeout(30)

    sql_service_check.main(config)
    check_xietong.startup(config, driver)
    check_dingwei.startup(config, driver)

    driver.quit()