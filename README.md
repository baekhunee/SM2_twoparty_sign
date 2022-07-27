# 实验名称
SM2_twoparty_sign

# 实验简介
implement sm2 2P sign with real network communication

# 实验完成人
权周雨 

学号：202000460021 

git账户名称：baekhunee

# 运行指导
需要先启动twoparty_sign_client2，再启动twoparty_sign_client1，两个文件均可以直接启动。

# 实现过程
根据课件指导，sm2 two-party sign过程如下所示：
![image](https://user-images.githubusercontent.com/105578152/181214032-0f402343-a999-4852-9bac-34c82989116b.png)

# 部分代码说明
## sm3.py
用于实现SM3算法。后期签名过程中需要用到Hash函数，本次实验选用的即为自己实现的SM3函数。调用方法为：
```
import sm3
m = "..."
sm3.SM3(m)
```

## def epoint_add(x1,y1,x2,y2)
椭圆曲线上的加法,返回值(x,y)=(x1,y1)+(x2,y2)

## def epoint_mult(x,y,k)
椭圆曲线上的点乘，返回值为k*(x,y)

## 核心代码展示
双方具体的签名与收发过程均已在代码中添加注释，不再赘述。

### twoparty_sign_client1
```
# 生成子私钥 d1
d1 = randint(1,n-1)

# 计算P1 = d1^(-1) * G
P1 = epoint_mult(X,Y,invert(d1,p))
x,y = hex(P1[0]),hex(P1[1])

# 向客户2发送P1
addr = (HOST, PORT)
client.sendto(x.encode('utf-8'), addr)
client.sendto(y.encode('utf-8'), addr)

#计算ZA
m = "hello,this is baekhunee!"
m = hex(int(binascii.b2a_hex(m.encode()).decode(), 16)).upper()[2:]
ID_A = "1321699113@qq.com"
ID_A = hex(int(binascii.b2a_hex(ID_A.encode()).decode(), 16)).upper()[2:]
ENTL_A = '{:04X}'.format(len(ID_A) * 4)
ma = ENTL_A + ID_A + '{:064X}'.format(a) + '{:064X}'.format(b) + '{:064X}'.format(X) + '{:064X}'.format(Y)
ZA = sm3.SM3(ma)
e = sm3.SM3(ZA + m)

# 生成随机数k1
k1 = randint(1,n-1)

# 计算Q1 = k1 * G
Q1 = epoint_mult(X,Y,k1)
x,y = hex(Q1[0]),hex(Q1[1])

# 向客户2发送Q1,e
client.sendto(x.encode('utf-8'),addr)
client.sendto(y.encode('utf-8'),addr)
client.sendto(e.encode('utf-8'),addr)

# 从客户2接收r,s2,s3
r,addr = client.recvfrom(1024)
r = int(r.decode(),16)
s2,addr = client.recvfrom(1024)
s2 = int(s2.decode(),16)
s3,addr = client.recvfrom(1024)
s3 = int(s3.decode(),16)

# 计算s
s=((d1 * k1) * s2 + d1 * s3 - r)%n
if s!=0 or s!= n - r:
    print((hex(r),hex(s)))
```

### twoparty_sign_client2
```
# 生成子私钥 d2
d2 = randint(1,n-1)

# 从客户1接收P1=(x,y)
x,addr = client.recvfrom(1024)
x = int(x.decode(),16)
y,addr = client.recvfrom(1024)
y = int(y.decode(),16)

# 计算共享公钥P
P1 = (x,y)
P = epoint_mult(P1[0],P1[1],invert(d2,p))
P = epoint_add(P[0],P[1],X,-Y)

# 从客户1接收Q1=(x,y)与e
x,addr = client.recvfrom(1024)
x = int(x.decode(),16)
y,addr = client.recvfrom(1024)
y = int(y.decode(),16)
Q1 = (x,y)
e,addr = client.recvfrom(1024)
e = int(e.decode(),16)

# 生成随机数k2,k3
k2 = randint(1,n-1)
k3 = randint(1,n-1)

# 计算Q2 = k2 * G
Q2 = epoint_mult(X,Y,k2)

# 计算(x1,y1) = k3 * Q1 + Q2
x1,y1 = epoint_mult(Q1[0],Q1[1],k3)
x1,y1 = epoint_add(x1,y1,Q2[0],Q2[1])
r =(x1 + e)%n
s2 = (d2 * k3)%n
s3 = (d2 * (r+k2))%n

# 向客户1发送r,s2,s3
client.sendto(hex(r).encode(),addr)
client.sendto(hex(s2).encode(),addr)
client.sendto(hex(s3).encode(),addr)
```

# 测试结果

![image](https://user-images.githubusercontent.com/105578152/181214677-7b0d91eb-473e-4683-8744-f834b11ef6f9.png)

![image](https://user-images.githubusercontent.com/105578152/181214740-42d536e9-1b28-4ade-9de7-c7f45ebac8b2.png)

