import numpy as np
import pandas as pd
import math

def read_csv(filecsv):
    dataset=pd.read_csv(filecsv,engine='python').dropna(axis=1)
    features_name = dataset.columns.values.tolist()
    dataset=np.array(dataset)

    X=dataset[:,1:]
    y=dataset[:,0]
    return(X,y,features_name)

def calcE(X,coli,colj):
    # sum=0
    # for i in range(len(X)):
    #
    #      sum+=(X[i,coli]-X[i,colj])*(X[i,coli]-X[i,colj])
    sum = np.sum((X[:,coli]-X[:,colj])**2)


    return math.sqrt(sum)
def Euclidean(X,n):

    Euclideandata=np.zeros([n,n])

    for i in range(n):
        for j in range(n):
            Euclideandata[i,j]=calcE(X,i,j)
            Euclideandata[j,i]=Euclideandata[i,j]
    Euclidean_distance=[]

    for i in range(n):
        sum = np.sum(Euclideandata[i,:])
        Euclidean_distance.append(sum/n)

    return Euclidean_distance
def varience(data,avg1,col1,avg2,col2):

    return np.average((data[:,col1]-avg1)*(data[:,col2]-avg2))

def Person(X,y,n):
    feaNum=n
    #label_num=len(y[0,:])
    label_num=1
    PersonData=np.zeros([n])
    for i in range(feaNum):
        for j in range(feaNum,feaNum+label_num):
            #print('. ', end='')
            average1 = np.average(X[:,i])
            average2 = np.average(y)
            yn=(X.shape)[0]
            y=y.reshape((yn,1))
            dataset = np.concatenate((X,y),axis=1)
            numerator = varience(dataset, average1, i, average2, j);
            denominator = math.sqrt(
                varience(dataset, average1, i, average1, i) * varience(dataset, average2, j, average2, j));
            if (abs(denominator) < (1E-10)):
                PersonData[i]=0
            else:
                PersonData[i]=abs(numerator/denominator)

    return list(PersonData)

def run(filecsv,logger):
    logger.info('mrmd start...')
    X,y,features_name=read_csv(filecsv)
    n=len(features_name)-1


    e=Euclidean(X,n)

    p = Person(X,y,n)

    mrmrValue=[]
    for i,j in zip(p,e):
        mrmrValue.append(i+j)
    mrmr_max=max(mrmrValue)
    mrmrValue = [x / mrmr_max for x in mrmrValue]
    mrmrValue = [(i,j) for i,j in zip(features_name[1:],mrmrValue)]   # features 和 mrmrvalue绑定
    mrmd=sorted(mrmrValue,key=lambda x:x[1],reverse=True)  #按mrmrValue 由大到小排序

    mrmd =[x[0] for x in mrmd]


    logger.info('mrmd end.')
    return mrmd
if __name__ == '__main__':
    import datetime
    print(datetime.datetime.now())
    print ((run('20.csv',1)))
    print(datetime.datetime.now())


