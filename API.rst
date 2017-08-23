==============
LogService 接口文档 version 0.8.21
==============


.. contents::

**Copyright(c) __10.com__. All rights reserved.**



识别用户
-------

详细说明
~~~~~~~

**URL**

::

         http://:8081/api/open/v1/identify


**返回数据格式**

::

         JSON

**HTTP 请求方式**

::

         GET | POST


**参数说明**

=======================  =======================  =======================  =======================
**参数**                  **类型**                 **必选**                  **说明**
=======================  =======================  =======================  =======================
app_key                  string                   是                       应用的AppKey
device_id                string                   是                       手机唯一标识符
user_id                  string                   是                       用户唯一标识符
platform                 string                   是                       平台
user_property            jsonstring               是                       用户属性信息（例如：{"avatar": "http://tp4.sinaimg.cn/5716173917/1", "name": "张三", "gender":"男", "等级": 90}）
device_info              jsonstring               是                       设备信息（例如：{"device_md5": "cbd007fe06818d2029f68c4ae01f6986","device_type": "直立式","l": 1080,"h": 1920,"device_brand": "samsung","device_model": "Galaxy Note3","resolution": "480dip","imei": "358584050352583/02","mac": "F0:25:B7:2C:6A:D1","is_prison_break": 0,"is_crack": 0,"language": "简体中文","timezone": "GMT+08:00 中国标准时间"}）
=======================  =======================  =======================  =======================



**返回说明**

* 1. ls_id : logservice生成的用户id

- 正常返回如下:

::

        {
          "status": 200,
          "data": {
            "Identify": {
              "ls_id": 7
            }
          },
          "msg": "success"
        }

- 错误返回如下:

::

        {
          "msg": "您还没有注册此应用",
          "status": 1002,
          "data": {
            "Identify": {}
          }
        }

**示例代码**

::

         curl -X POST http://:8081/api/open/v1/identify
         -d"app_key=$app_key 。。。"




自定义事件
-------

详细说明
~~~~~~~

**URL**

::

         http://:8081/api/open/v1/track


**返回数据格式**

::

         JSON

**HTTP 请求方式**

::

         GET | POST


**参数说明**

=======================  =======================  =======================  =======================
**参数**                  **类型**                 **必选**                  **说明**
=======================  =======================  =======================  =======================
app_key                  string                   是                       应用的AppKey
device_id                string                   是                       手机唯一标识符
user_id                  string                   是                       用户唯一标识符
platform                 string                   是                       平台
event_info               string                   是                       用户属性信息（例如：{ 	"event_name": "购买10000", 	"begin_date": 1456664356, 	"begin_day_id": 20170818, 	"platform": 1, 	"network": 1, 	"mccmnc": 46002, 	"useragent": "香港代理服务器", 	"channel": "百度", 	"ip": 192168001001, 	"duration": 20, 	"utc_date": 1456664356,    	"app_version": "v1.3.0", 	"os": "Android", 	"ov": 6.0,  	"website": "https://www.10.com", 	"current_url": "https://www.10.com/index.html", 	"referrer_url": "https://www.10.com", 	"bs": "google", 	"bv": 4.3, 	"utm_source": "百度推广", 	"utm_medium": "腾讯自媒体", 	"utm_campaign": "banner 推广", 	"utm_content": "十全十美网络有限公司", 	"utm_term": "十全十美 10.com"  }）
event_attr               string                   是                       事件属性（例如：{ 	"分类": "手机~", 	"名称": "iPhone6 plus 64g 国行" }）
device_info              string                   是                       设备信息（例如：{ 	"device_md5": "cbd007fe06818d2029f68c4ae01f6986", 	"platform": 1, 	"device_type": "直立式", 	"l": 1080, 	"h": 1920, 	"device_brand": "samsung", 	"device_model": "Galaxy Note3", 	"resolution": "480dip", 	"imei": "358584050352583/02", 	"mac": "F0:25:B7:2C:6A:D1", 	"is_prison_break": 0, 	"is_crack": 0, 	"language": "简体中文", 	"timezone": "GMT+08:00 中国标准时间" }）
=======================  =======================  =======================  =======================



**返回说明**

- 正常返回如下:

::

        {
          "status": 200,
          "msg": "success",
          "data": {
            "track": {}
          }
        }


**示例代码**

::

         curl -X POST http://:8081/api/open/v1/track
         -d"app_key=$app_key 。。。"



事件时长统计 1
-------

开始统计 startTrack
~~~~~~~

**URL**

::

         http://:8081/api/open/v1/startTrack


**返回数据格式**

::

         JSON

**HTTP 请求方式**

::

         GET | POST


**参数说明**

* 1、event_info：不填写duration字段值

=======================  =======================  =======================  =======================
**参数**                  **类型**                 **必选**                  **说明**
=======================  =======================  =======================  =======================
app_key                  string                   是                       应用的AppKey
device_id                string                   是                       手机唯一标识符
user_id                  string                   是                       用户唯一标识符
platform                 string                   是                       平台
event_info               string                   是                       用户属性信息（例如：{ 	"event_name": "购买10000", 	"begin_date": 1456664356, 	"begin_day_id": 20170818, 	"platform": 1, 	"network": 1, 	"mccmnc": 46002, 	"useragent": "香港代理服务器", 	"channel": "百度", 	"ip": 192168001001, 	"utc_date": 1456664356,    	"app_version": "v1.3.0", 	"os": "Android", 	"ov": 6.0,  	"website": "https://www.10.com", 	"current_url": "https://www.10.com/index.html", 	"referrer_url": "https://www.10.com", 	"bs": "google", 	"bv": 4.3, 	"utm_source": "百度推广", 	"utm_medium": "腾讯自媒体", 	"utm_campaign": "banner 推广", 	"utm_content": "十全十美网络有限公司", 	"utm_term": "十全十美 10.com"  }）
event_attr               string                   是                       事件属性（例如：{ 	"分类": "手机~", 	"名称": "iPhone6 plus 64g 国行" }）
device_info              string                   是                       设备信息（例如：{ 	"device_md5": "cbd007fe06818d2029f68c4ae01f6986", 	"platform": 1, 	"device_type": "直立式", 	"l": 1080, 	"h": 1920, 	"device_brand": "samsung", 	"device_model": "Galaxy Note3", 	"resolution": "480dip", 	"imei": "358584050352583/02", 	"mac": "F0:25:B7:2C:6A:D1", 	"is_prison_break": 0, 	"is_crack": 0, 	"language": "简体中文", 	"timezone": "GMT+08:00 中国标准时间" }）
=======================  =======================  =======================  =======================



**返回说明**

- 正常返回如下:

::

        {
          "status": 200,
          "msg": "success",
          "data": {
            "startTrack": {}
          }
        }


**示例代码**

::

         curl -X POST http://:8081/api/open/v1/startTrack
         -d"app_key=$app_key 。。。"




事件时长统计 2
-------

开始统计 endTrack
~~~~~~~

**URL**

::

         http://:8081/api/open/v1/endTrack


**返回数据格式**

::

         JSON

**HTTP 请求方式**

::

         GET | POST


**参数说明**

=======================  =======================  =======================  =======================
**参数**                  **类型**                 **必选**                  **说明**
=======================  =======================  =======================  =======================
app_key                  string                   是                       应用的AppKey
user_id                  string                   是                       用户唯一标识符
event_name               string                   是                       事件名称
=======================  =======================  =======================  =======================



**返回说明**

- 正常返回如下:

::

        {
          "status": 200,
          "msg": "success",
          "data": {
            "endTrack": {}
          }
        }


**示例代码**

::

         curl -X POST http://:8081/api/open/v1/endTrack
         -d"app_key=$app_key 。。。"