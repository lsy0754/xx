import os
import struct
import numpy as np
import matplotlib.pyplot as plt
from sympy.physics.quantum.circuitplot import matplotlib
from ministdata import X_train, X_test, y_train, y_test
#from train_test import X_train, X_test, y_train, y_test

def Pwi(labels):                #计算先验概率
    arr=[]
    S=labels.tolist()
    for i in range(10):
        arr.append(S.count(i))    #计算0：9每个labels的数量
    arr=np.array(arr)
    arr=arr/len(labels)
    return arr

def PCAH(images):                   #降维28*28->14*14
    newdata=[]
    for i in range(len(images)):
        x=[]
        data=images[i].reshape([28,28])
        for j in range(14):
            for k in range(14):
                if (data[j*2:(j+1)*2,k*2:(k+1)*2].sum()) >0:
                    x.append(1)
                else:
                    x.append(0)
        newdata.append(x)
    newdata=np.array(newdata)
    return newdata

def towzhi(images):                   #二值化
    arr=[np.clip(images[0],0,1).tolist()]        #clip([],min,max)
    for i in range(1,len(images)):
        x=np.clip(images[i],0,1).tolist()
        arr.append(x)
    data=np.array(arr)
    return data

def Pjwi(data,labels):
    P=np.zeros((10,196))
    x={0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}
    for i in range(len(labels)):
        x[labels[i]].append(i)
    for i in range(10):
        for j in range(196):
            for k in x[i]:
                if data[k,j]!=0:
                    P[i,j]+=1
        P[i]=(P[i]+1)/(len(x[i])+2)
    return P

def train():
    #images,labels=load_mnist("D:\mnist_all.mat")   #读取数据
    images=X_train
    labels= y_train
    print('labels',labels)
    images=towzhi(images)                       #二值化
    data=PCAH(images)                       #主成分分析并降维
    P=Pjwi(data,labels)                     #得到类条件概率
    arr=Pwi(labels)
    return data,P,arr                         #返回Pjwi,先验概率

def PwiX(P,arr):                           #计算后验概率
    X=0
    Pi=np.zeros((10))
    for i in range(10):                     #计算分母
        X+=P[i]*arr[i]
    for i in range(10):
        Pi[i]=P[i]*arr[i]/X            #这里实际上除不除X对最后结果影响差别不大
    return Pi

def MAXindex(Pi):                   #返回最大值的后验概率的值
    x=0
    for i in range(len(Pi)):
        if Pi[x]<Pi[i]:
            x=i
    return x

def Pxwi(data,P):                    #计算类条件概率
    Pi=np.ones((10))
    for i in range(10):
        for j in range(196):
            if data[j]==0:
                Pi[i]*=(1-P[i,j])
            else:
                Pi[i]*=P[i,j]
    return Pi

def test(P,arr):                     #测试函数
    T=0;
    #images,labels=load_mnist("D:\py代码", kind='t10k')
    images=X_test
    labels=y_test
    data=PCAH(images)                       #降维
    data=towzhi(data)                       #二值化
    count=[]
    countx=np.zeros(10)
    S=labels.tolist()
    for i in range(10):
        count.append(S.count(i))    #计算0：9每个labels的数量
    for i in range(len(labels)):
        p1=Pxwi(data[i],P)               #计算类条件概率
        p2=PwiX(p1,arr)                  #计算后验概率
        x=MAXindex(p2)                  #返回后验概率最大的那个值
        if x==labels[i]:
            countx[x]+=1
            T+=1
    for i in range(10):
        countx[i]=countx[i]/count[i]
    return T/len(labels),countx

data1414,P,arr=train()
T,F=test(P,arr)
print(T)
print(F)

some_digit = data1414[12345]
some_digit_image = some_digit.reshape(14,14)
plt.imshow(some_digit_image, cmap=matplotlib.cm.binary, interpolation="nearest")
#plt.imshow(some_digit_image)
plt.show()