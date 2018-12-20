#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
import bs4
import json
import getpass
import os
import sys

class LoginCommon:

    URL_JXFW_JSON = 'http://jxfw.gdut.edu.cn/xsgrkbcx!getDataList.action'
    URL_JXFW_JUMP = 'http://jxfw.gdut.edu.cn/new/ssoLogin'
    URL_AUTHSERVER = 'http://authserver.gdut.edu.cn/authserver/login?service=http%3A%2F%2Fjxfw.gdut.edu.cn%2Fnew%2FssoLogin'

    HEADER_GET = {
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
    HEADER_POST = {
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8'
        }
    LOGIN_POST = {
        'username':'',
        'password':'',
        'lt':'',
        'dllt':'',
        'execution':'',
        '_eventId':'',
        'rmShown':''
        }
    
    def __init__(self, sessionID):
        self.sessionID = sessionID
        self._session = requests.session()
        self.__init_session()
    
    def __data_merge(self, html):
        soup1 = bs4.BeautifulSoup(html, 'lxml')
        for i in self.LOGIN_POST:
            self.LOGIN_POST[i] = soup1.find('input',attrs={'name':i})['value']
        print('正在尝试统一认证中心密码登录......')
        self.LOGIN_POST['username'] = input('请输入你的学号:\n')
        self.LOGIN_POST['password'] = getpass.getpass('请输入你的登录密码:\n')
        return self.LOGIN_POST
    
    def __init_session(self):
        if os.path.isfile('cookies-tmp-'+str(self.sessionID)) is True:
            print('尝试使用缓存的cookies登录......')
            try:
                with open('cookies-tmp-'+str(self.sessionID),'r') as f:
                    requests.utils.add_dict_to_cookiejar(self._session.cookies, json.load(f))
            except:
                os.remove('cookies-tmp-'+str(self.sessionID))
                return self.__login()
            if self.__login_status_check() is False:
                print('Cookies登录失败，请使用帐号密码登录')
                os.remove('cookies-tmp-'+str(self.sessionID))
                self._session.cookies.clear()
                return self.__login()
            return self._session
        else:
            return self.__login()

    def __save_cookies(self,save_session): #传入参数为requests.session()
        save_session.cookies.set('__jsluid',None)
        if os.path.isfile('cookies-tmp-'+str(self.sessionID)) is not True:
            with open('cookies-tmp-'+str(self.sessionID),'x') as f:
                json.dump(dict(save_session.cookies),f)
        else:
            with open('cookies-tmp-'+str(self.sessionID),'w') as f:
                f.truncate()
                json.dump(dict(save_session.cookies),f)

    def __login_status_check(self):
        try:
            soup2 = bs4.BeautifulSoup(self._session.get('http://jxfw.gdut.edu.cn/login!welcome.action',headers=self.HEADER_GET).text,'lxml')
            return str(soup2.title) == '<title>教学管理系统</title>'
        except:
            print('An error occurred during the logcheck!')

    def __login(self):
        try:
            r = self._session.get(self.URL_JXFW_JUMP, headers=self.HEADER_GET)
            post_status = self._session.post(self.URL_AUTHSERVER,headers=self.HEADER_POST,data=self.__data_merge(r.text))
            if post_status.status_code == 500:
                raise requests.HTTPError('You may be banned by the site')
            if self.__login_status_check() is False:
                raise Exception('Your username or password may be wrong!')
            self.__save_cookies(self._session)
            return self._session
        except requests.HTTPError as e:
            print(e)
            sys.exit()
        except Exception as e:
            print(e)
            print('遇到网络异常，已退出程序......')
            sys.exit()
