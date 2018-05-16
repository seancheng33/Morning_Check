'''
主入口
'''
import sql_service_check
import check_dingwei
import check_xietong

if __name__ == '__main__':
    sql_service_check.main()
    check_xietong.startup()
    check_dingwei.startup()
