# beer_cloud

我用来管理树莓派的文件


### 效果图

![](https://beef-1256523277.cos.ap-chengdu.myqcloud.com/uPic/hsnocd.png)

![](https://beef-1256523277.cos.ap-chengdu.myqcloud.com/uPic/iFnKfN.png)


### 使用

```
cd beer_cloud
bash deploy.sh

cd cloud_api/target 

# 自己修改 cloud_api/src/main/resources/application.yaml 配置文件 后打包
java -jar cloud_api-0.0.1-SNAPSHOT.jar 

# 或者自己指定 配置文件路径
java -jar cloud_api-0.0.1-SNAPSHOT.jar --Dspring.config.location=application.yaml
```

application.yaml 
```
server:
  port: 9000


# 可以指定多个 storages
config:
  storages:
    - path: /home/pi/sda1 # 服务器路径
      name: sda1 # alias web 端显示
      url: http://192.168.31.158:8070 # nginx 管理的文件路径
```

### cloud_api

java 实现的一些接口

### cloud_web

vue 实现的简单页面

### nginx

查看功能会跳出新页面，由 nginx 统一管理权限

