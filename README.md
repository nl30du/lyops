# lyops
+ 使用Django框架开发的运维管理平台
+ 开发语言: python;
+ 后端框架: Django;
+ 前端框架：bootstrap/jquery；
+ 项目功能：线上用户权限集中控制以及用户操作行为审计(已完成)，自动化任务(开发中)，配置管理(计划中)，流程管理(计划中)；

## 环境：
+ RHEL 6.8 x86_64
+ django-1.11
+ ansible-2.4.2
+ ansible-api-2.3.0
+ python 2.7
+ MySQL 5.6
+ syslog-ng-3.2.5

## lyops更新记录：
    > ansible-api相关功能封装(指定模块执行、动态主机、剧本执行、回调重写)；
    > 自动化任务前端页面构建(开发中)；
    > 权限审计功能完成；
    > 页面用户排序调整(优先显示新添加的用户)；

## 功能介绍
1.**登陆页面**
![登陆](https://github.com/nl30du/blog/blob/master/blog/lyops/pic/login.png)
2.**首页**，显示平台一些说明信息等。
![仪表盘]()
3.**主机列表**
进入主机列表界面，可以选择机房和维护人员，使用ajax处理，每次选择会从库中重新查询符合条件的数据；
这些服务器相关的信息支持自动采集，由于目前写的方法只能完成采集任务，所以并没有将链接放出来，不过可以通过访问指定链接进行访问。
![主机列表](https://github.com/Hasal/dzhops_picture/blob/master/dzhops_pic/asset.png)
4.**SaltStack**
可完成如下功能：
+ 服务器初始化（如模块部署等）
+ 程序、配置更新
+ 日常维护操作
+ 远程命令执行
当对Minion执行操作时，会记录本次目标Minion的数量，然后与返回结果的Minion数量进行对比，找出哪些没有返回结果；当接收到返回结果后，使用bootstrap的模态框显示结果，其中蓝色表示执行成功，红色表示有失败存在，可以点击标签查看详细情况；
![模块部署](https://github.com/Hasal/dzhops_picture/blob/master/dzhops_pic/deploy.png)
![模块部署-返回结果-模态框展开-失败情况](https://github.com/Hasal/dzhops_picture/blob/master/dzhops_pic/deploy_show.png)
![模块部署-返回结果-模态框展开-成功情况](https://github.com/Hasal/dzhops_picture/blob/master/dzhops_pic/deploy_show_success.png)
![远程命令执行](https://github.com/Hasal/dzhops_picture/blob/master/dzhops_pic/execute.png)
5.**MinionKeys管理**
可以分别选择已接受、待接受、已拒绝，并且可以选择机房及维护人员，进行对应的管理操作；
![MinionKeys管理](https://github.com/Hasal/dzhops_picture/blob/master/dzhops_pic/manage.png)
6.**操作记录**
可以记录每次操作执行人的账号、操作、目标、及jid，并可以通过jid查看该次操作的返回结果详细情况。
![操作记录](https://github.com/Hasal/dzhops_picture/blob/master/dzhops_pic/record.png)
![操作记录-详细](https://github.com/Hasal/dzhops_picture/blob/master/dzhops_pic/record_detail.png)
7.**更多细节不再赘述**
