==============
LogService version 0.8.14
==============


.. contents::

**Copyright(c) __10.com__. All rights reserved.**



* 事件总表：b_event_all_

===============   ===============   ===============
字段          	  类型         		字段说明
ls_id             int8
device_id         int4              设备id
user_id           int4
session_id        int8              会话id
event_name		  varchar           事件名称
event_id          int4              事件类型id,事件类型id包含两个特定事件的值：-1为会话开始、-2为会话结束
begin_data        timestamp         开始时间
begin_day_id      int4              日期，开始时间的整数格式(yyyyMMdd)
platform          int2              平台，1 Android、2 iOS、3 JS
network           int2              网络，1为 2G、2 为3G、3为4G、4为WIFI
mccmnc            int4              运营商，46002、46007为中国移动，46003、46005、46011为中国电信，46001、46006为中国联通，46020为中国铁通
useragent         varchar           用户代理
website           varchar           来源网站，标识来用户自哪个网站,只限JS平台
current_url       varchar           当前URL，只限JS平台
referrer_url      varchar           来源URL，标识用户来自哪个网站的URL,只限JS平台
channel           varchar           渠道
app_version       varchar           版本，只限Android、iOS平台
ip                int8              用户IP
country           varchar           国家，基于用户IP
area              varchar           地区，基于用户IP
city              varchar           城市，基于用户IP
os                varchar           操作系统，只限Android、iOS平台
ov                int4              操作系统版本，只限Android、iOS平台
bs                varchar           浏览器，只限JS平台
bv                int4              浏览器版本，只限JS平台
utm_source        varchar           广告来源，标识来自哪个渠道，只限JS平台
utm_medium        varchar           广告媒介，标识来自哪种媒介，只限JS平台
utm_campaign      varchar           广告名称，标识推广的主题，只限JS平台
utm_content       varchar           广告内容，标识同一推广主题下的不同版本或不同内容，只限JS平台
utm_term          varchar           广告关键词，标识推广所使用的关键字，只限JS平台
duration          int8              持续时间
utc_date          timestamp         UTC时间
===============   ===============   ===============


事件属性表：b_user_event_attr

===============   ===============   ===============
字段          	  类型         		字段说明
ls_id             int8
device_id         int4              设备id
user_id           int4
session_id        int8              会话id
event_id          int4              事件类型id,事件类型id包含两个特定事件的值：-1为会话开始、-2为会话结束
event_name		  varchar           事件名称
attr_id           int4              事件属性id
attr_name         varchar           事件属性名称
attr_data_type    varchar           事件属性数据类型
attr_value        varchar           事件属性值
begin_date        timestamp         开始时间
begin_day_id      int4              日期，开始时间的整数格式(yyyyMMdd)
platform          int2              平台，1 Android、2 iOS、3 JS
utc_date          timestamp         UTC时间
===============   ===============   ===============




* 用户表：b_user_

===============   ===============   ===============
字段          	  类型         		字段说明
device_id		  int4              设备id
user_id           int4              记录每一位用户的唯一id，可以是用户id，email等唯一值作为用户在诸葛io的user_id
ls_id             int8              logserviceid
begin_date        timestamp         生成时间
platform          int2              平台，1 Android、2 IOS、3 JS
===============   ===============   ===============



* 设备表：b_device_

===============   ===============   ===============
字段          	  类型         		字段说明
device_id    	  int4         		设备id
device_md5	 	  varchar      		md5
platform     	  int2         		平台，1 Android、2 IOS、3 JS
device_type  	  varchar      		设备类型
l            	  int4         		水平像素
h            	  int4         		垂直像素
device_brand 	  varchar      		设备商标
device_model 	  varchar      		设备型号
resolution   	  varchar      		分辨率
imei         	  varchar      		移动设备标识，由15位数字组成\
mac          	  varchar      		mac地址
is_prison_break   int2              是否越狱
is_crack          int2              是否破解
language          varchar           语言
timezone          varchar           时区
===============   ===============   ===============