#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#使用统一认证密码登录
#from LoginCommonAuthserver import LoginCommon

#使用教务系统验证码登录
from LoginCommonClassic import LoginCommon 

import sys
import os
import json

class xk_config_generator(LoginCommon):

    URL_GET_LIST = 'xsxklist!getDataList.action'
    URL_JXFW = 'http://jxfw.gdut.edu.cn/'
    POST_DATA = {
        "page" : 1,
        "rows" : 50,
        "sort" : "kcrwdm",
        "order" : "asc"
    }

    def __save_json(self,tmp): 
        if os.path.isfile('config-tmp-'+str(self.sessionID)) is not True:
            print('抢课缓存已经生成......')
            with open('config-tmp-'+str(self.sessionID),'x',encoding='utf-8') as f:
                f.write(json.dumps(tmp, indent=4, separators=(',', ':'), ensure_ascii=False))
        else:
            print('抢课缓存已被刷新......')
            with open('config-tmp-'+str(self.sessionID),'w',encoding='utf-8') as f:
                f.truncate()
                f.write(json.dumps(tmp, indent=4, separators=(',', ':'), ensure_ascii=False))

    def generator(self):
        try:
            r = self._session.post(self.URL_JXFW + self.URL_GET_LIST, headers=self.HEADER_POST, data=self.POST_DATA)
        except:
            sys.exit()
        data_list = r.json()['rows']
        filter_list = [("{} {} {}").format(str(num),n['xmmc'],n['teaxm']) for num,n in enumerate(data_list) ]
        print("\n下面是你可以选择的课程:")
        print(('\n').join(filter_list))
        getstr = input("请输入你要需要抢课的序号：\n")
        try:
            getnum = int(getstr)
            if getnum>=len(data_list) or getnum<0 :
                raise ValueError
        except:
            print("输入课程序号有误")
            sys.exit()
        tmp_dict = {key:value for key,value in data_list[getnum].items() if key=='kcrwdm' or key=='kcmc'}
        self.__save_json(tmp_dict)
        
if __name__ == "__main__":
    xk_config_generator('xk').generator()