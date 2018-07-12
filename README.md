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
![首页](https://github.com/nl30du/blog/blob/master/blog/lyops/pic/index.png)
3.**用户列表**，显示所有用户信息(id，真实用户，登录用户权限，数据指纹，复制key到其他项目，控制用户访问等)。
![用户列表](https://github.com/nl30du/blog/blob/master/blog/lyops/pic/userlist.png)
4.**用户添加**，选择对应项目以及用户权限类型，执行添加操作，会在后台执行成功后返回对应信息至页面。
![用户添加](https://github.com/nl30du/blog/blob/master/blog/lyops/pic/useradd.png)
5.**项目管理**，添加对应项目(中控机)，用户密码或者秘钥认证。
![项目管理](https://github.com/nl30du/blog/blob/master/blog/lyops/pic/managepro.png)
6.**命令记录**显示用户操作命令行为记录。
![项目管理](https://github.com/nl30du/blog/blob/master/blog/lyops/pic/commandlist.png)

## 安装
安装必备软件

```
yum -y update && yum -y install mysql-devel wget epel-release python-devel gcc c++ make openssl openssl-devel passwd libffi libffi-devel
yum -y install ansible
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
```

mysql-5.6安装
```
安装方式(略),注意修改mysql字符集为utf8
建立对应的数据库：
mysql>CREATE DATABASE `lyops` DEFAULT CHARACTER SET utf8;
```

配置django配置文件lyops/settings.py

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lyops',
        'USER': '对应授权用户名',
        'PASSWORD': '对应授权用户密码',
        'HOST': 'IP',
        'PORT': 'PORT',
    }
}
```


上面这些操作都完成后就可以部署项目了

安装依赖

pip install -r requirements.txt

同步数据库

python manage.py makemigrations

python manage.py migrate

创建管理员

python manage.py createsuperuser

runserver运行检查是否正常

python manage.py runserver 0.0.0.0:8080

如果无法正常运行，请检查以上步骤

访问路径：
http://ip:8080/ops/
  
email：tangcc_tl@163.com  

PS:

  正常运行后，正式上线最好部署django+nginx+uwsgi(gunicorn)环境  
  


水平有限请见谅。

