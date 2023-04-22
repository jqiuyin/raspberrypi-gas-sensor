# Raspberrypi Gas Sensor

## 接线图

<img src="images/wiring.jpg">

## 镜像地址

[qiuyin/raspberrypi-gas-sensor:dind](https://hub.docker.com/r/qiuyin/raspberrypi-gas-sensor)  
*注意*：镜像使用的架构为**ARMv7**,并且只能在**raspberrypi**上使用
## 使用

```
docker run --device /dev/gpiomem -it --rm raspberrypi-gas-sensor:dind
```