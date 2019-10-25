## 油猴脚本
### weibo-interest-skip.js
    新浪微博兴趣推荐页面自动跳转新浪微博首页。
### ac68u-dhcp-sorter.js
    华硕RT-AC68U路由器官方ROM，DHCP配置页面，根据IP地址最后一位排序。

## RightClickBooster
### open_in_terminal_window
    在终端窗口中打开当前目录。
### open_in_sublime
    在Sublime Text中打开文件，如选择对象为目录，则点击无效。
### Simple Http Server
    在当前目录打开python的SimpleHTTPServer

## python
### asus_merlin_custom_ddns.py
使用 python 实现的 ddns，基于阿里云，并实现了自动堆 ECS 授权该 ip 的网络安全组访问
1. 首先安装 Entware
2. 通过 opkg 安装 python3（python2.7 中安装阿里云 API SDK 时发生错误，本人未深入探索）
3. 开启 jffs，并且在 /jffs/scripts 下创建 ddns_start 脚本，样例内容如下：
```shell
#!/bin/sh
PATH=/jffs/scripts/
LOGPATH=/opt/var/log/ddns.log
COMMAND=exec

ACCESSKEY=''
SECRET=''
ENDPOINT=''
RECORDID=''
GROUPID=''

/opt/bin/python $PATH/aliddns.py $COMMAND $ACCESSKEY $SECRET $ENDPOINT $RECORDID $GROUPID $* >> $LOGPATH 2>&1
/sbin/ddns_custom_updated $?
```
4. Merlin 对 Custom DDNS 的说明见 https://github.com/RMerl/asuswrt-merlin/wiki/Custom-DDNS
