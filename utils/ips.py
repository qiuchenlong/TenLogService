# -*- coding: utf-8 -*-
'''
Create on 2017年08月22日 11:43

@author: 邱晨龙
@email: Cyndi@10.com
@QQ: 601976246
@phone: 13950209512

Copyright(c) __10.com__. All rights reserved.
'''


import requests


class IP():

    @staticmethod
    def checkip(ip):
        URL = 'http://ip.taobao.com/service/getIpInfo.php'
        try:
            r = requests.get(URL, params=ip, timeout=3)
        except requests.RequestException as e:
            print(e)
        else:
            json_data = r.json()
            if json_data[u'code'] == 0:
                # print('所在国家： ' + json_data[u'data'][u'country'])
                #
                # print('所在地区： ' + json_data[u'data'][u'area'])
                #
                # print('所在省份： ' + json_data[u'data'][u'region'])
                #
                # print('所在城市： ' + json_data[u'data'][u'city'])
                #
                # print('所属运营商：' + json_data[u'data'][u'isp'])

                return (json_data[u'data'][u'country'], json_data[u'data'][u'area'], json_data[u'data'][u'region'], json_data[u'data'][u'city'], json_data[u'data'][u'isp'])
            else:
                print('查询失败,请稍后再试！')



# ip = {'ip': '202.102.193.68'}
# checkip(ip)