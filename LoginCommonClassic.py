#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os
import requests
import bs4
import getpass
import sys
from Crypto.Cipher import AES
from binascii import b2a_hex


class LoginCommon:

    URL_JXFW_JSON = 'http://jxfw.gdut.edu.cn/xsgrkbcx!getDataList.action'
    URL_JXFW_ORIGIN = 'http://jxfw.gdut.edu.cn/login!welcome.action'
    URL_JXFW = 'http://jxfw.gdut.edu.cn/new/login'
    HEADER_GET = {
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
    HEADER_POST = {
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8'
        }

    def __init__(self, sessionID):
       self.sessionID = sessionID
       self._session  = requests.session()
       self.__init_session()

    def __init_session(self):
        if os.path.isfile('cookies-tmp-'+str(self.sessionID)) is True:
            print('尝试使用缓存的cookies登录......')
            try:
                with open('cookies-tmp-'+str(self.sessionID),'r') as f:
                    requests.utils.add_dict_to_cookiejar(self._session.cookies, json.load(f))
            except:
                os.remove('cookies-tmp-'+str(self.sessionID))
                return self.__login()
            print(self._session.get(self.URL_JXFW_JSON,headers=self.HEADER_GET).text)
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
            soup2 = bs4.BeautifulSoup(self._session.get(self.URL_JXFW_ORIGIN,headers=self.HEADER_GET).text,'lxml')
            return str(soup2.title) == '<title>教学管理系统</title>'
        except:
            print('An error occurred during the logcheck!')
    
    def __login(self):

        def encrypt(key,text):
            keys = key*4
            mode = AES.MODE_ECB
            bs = AES.block_size
            padding = bs - len(text) % bs
            padding_text = chr(padding) * padding
            cryptor = AES.new(keys, mode, padding_text)
            encryptcode = b2a_hex(cryptor.encrypt(text+padding_text))
            return bytes.decode(encryptcode)

        def post_data():
            print('正在使用教务系统直接登录......')
            dict_tmp = {} 
            dict_tmp['account'] = input('请输入你的学号:\n')
            pwd = getpass.getpass('请输入你的登录密码:\n')
            try:
                img = self._session.get('http://jxfw.gdut.edu.cn/yzm', headers=self.HEADER_GET)
                with open('verifycode.jpeg', 'wb+') as f:
                    f.write(img.content)
                print('verifycode.jpeg 以保存在目录中......')
                verifycode = input('请输入验证码:\n')
            except Exception as e:
                print(e)
            dict_tmp['pwd'] = encrypt(verifycode, pwd)
            dict_tmp['verifycode'] = verifycode
            return dict_tmp

        try:
            post_status = self._session.post(self.URL_JXFW, headers=self.HEADER_POST, data=post_data())
            if post_status.status_code == 500:
                raise requests.HTTPError('You may be banned by the site')
            if post_status.json()['message'] != '登录成功':
                raise requests.HTTPError('Your username or password may be wrong!')
            self.__save_cookies(self._session)
            return self._session
        except requests.HTTPError as e:
            print(e)
            sys.exit()
        except Exception as e:
            print(e)
            print('遇到异常，已退出程序......')
            sys.exit()
