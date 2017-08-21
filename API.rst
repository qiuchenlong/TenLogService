==============
LogService 接口文档 version 0.8.21
==============


.. contents::

**Copyright(c) __10.com__. All rights reserved.**



识别用户
-------

用户系统 获取验证码
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
user_property            string                   是                       用户属性信息（例如：{"avatar": "http://tp4.sinaimg.cn/5716173917/1", "name": "张三", "gender":"男", "等级": 90}
）
device_info              string                   是                       设备信息（例如：{
	"device_md5": "cbd007fe06818d2029f68c4ae01f6986",
	"device_type": "直立式",
	"l": 1080,
	"h": 1920,
	"device_brand": "samsung",
	"device_model": "Galaxy Note3",
	"resolution": "480dip",
	"imei": "358584050352583/02",
	"mac": "F0:25:B7:2C:6A:D1",
	"is_prison_break": 0,
	"is_crack": 0,
	"language": "简体中文",
	"timezone": "GMT+08:00 中国标准时间"
}）
=======================  =======================  =======================  =======================



**返回说明**

- 正常返回如下:

::

         {
           "status": 0,
           "data": {
             "getVerifyCode": {
               "verification_code": "064259"
             }
           },
           "msg": "success"
         }


**示例代码**

::

         curl -X POST http://120.24.86.73:8080/api/user/getVerifyCode
         -d"phoneNum=$phoneNum"