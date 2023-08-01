# Raspberrypi Gas Sensor

## 接线图

<img src="images/wiring.jpg">

## 镜像地址

[qiuyin/raspberrypi-gas-sensor:dind](https://hub.docker.com/r/qiuyin/raspberrypi-gas-sensor)  
*注意*：镜像使用的架构为**ARMv7**,并且只能在**raspberrypi**上使用

## 使用

### 云端

1. 安装k8s  
2. 安装kubeedge，参考资料[kubeedge](https://kubeedge.io/docs/setup/keadm)  
3. 为边缘节点命名

   ```
   kubectl label nodes raspberrypi name=raspberrypi
   ```

4. 创建资源

    ```
    kubectl apply -f crds/model.yaml
    kubectl apply -f crds/instance.yaml
    kubectl create -f deployment.yaml
    ```

### 边缘端

1. 安装kubeedge，参考资料[kubeedge](https://kubeedge.io/docs/setup/keadm)  
2. 安装mosquitto

    ```
    apt install mosquitto
    ```

### 云端查询数据

1. 使用命令行查询

   ```
   kubectl get device concentration -oyaml -w
   ```

2. 效果如下

   ```
    apiVersion: devices.kubeedge.io/v1alpha2

    kind: Device
    metadata:
    annotations:
        kubectl.kubernetes.io/last-applied-configuration: |
        {"apiVersion":"devices.kubeedge.io/v1alpha2","kind":"Device","metadata":{"annotations":{},"labels":{"description":"concentration","manufacturer":"test"},"name":"concentration","namespace":"default"},"spec":{"deviceModelRef":{"name":"concentration-model"},"nodeSelector":{"nodeSelectorTerms":[{"matchExpressions":[{"key":"","operator":"In","values":["raspberrypi"]}]}]}},"status":{"twins":[{"desired":{"metadata":{"type":"string"},"value":""},"propertyName":"concentration-status"}]}}
    creationTimestamp: "2023-08-01T05:42:27Z"
    generation: 1187
    labels:
        description: concentration
        manufacturer: test
    name: concentration
    namespace: default
    resourceVersion: "80910"
    uid: 77b3b45b-07d6-45af-8d18-178122c94f2b
    spec:
    deviceModelRef:
        name: concentration-model
    nodeSelector:
        nodeSelectorTerms:
        - matchExpressions:
        - key: ""
            operator: In
            values:
            - raspberrypi
    status:
    twins:

    - desired:
        metadata:
            type: string
        value: ""
        propertyName: concentration-status
        reported:
        metadata:
            timestamp: "1690881938358"
            type: string
        value: 0.83V
   ```
