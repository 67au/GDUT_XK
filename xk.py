#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#使用统一认证密码登录
#from LoginCommonAuthserver import LoginCommon

#使用教务系统验证码登录
from LoginCommonClassic import LoginCommon

import json
import time

class xk(LoginCommon):
    
    getAdd = 'xsxklist!getAdd.action'
    URL_JXFW = 'http://jxfw.gdut.edu.cn/'

    def __getadd(self):
        with open('config-tmp-'+str(self.sessionID),'r') as f:
            post_data = json.load(f)
        r = self._session.post(self.URL_JXFW+self.getAdd, data=post_data, headers=self.HEADER_POST)
        return r.text

    def status(self):
        tmp = self.__getadd()
        if '选课成功' in tmp or '已经选了该门课程' in tmp:
            print('选课结束')
            return 0
        print(tmp)
        return 1

if __name__ == "__main__":
    xx = xk('xk')
    s=xx.status()
    while(s):
        s = xx.status()
        time.sleep(1)
