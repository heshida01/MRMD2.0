
from minepy import MINE
import numpy as np
import pandas as pd
from multiprocessing import Pool,Manager
import  psutil
import datetime

def readData(file):
    dataset=pd.read_csv(file,engine='python').dropna(axis=1)
    feature_name = dataset.columns.values.tolist()
    dataset=np.array(dataset)
    #print(feature_name)
    return (dataset,feature_name)

def multi_processing_mic(datas):
    n=psutil.cpu_count(logical=False)
    n = 1
    pool=Pool()
    manager = Manager()
    dataset = datas[0]
    features_name = datas[1][1:]  # 去掉label的名字

    mic_score=manager.dict()
    features_and_index = manager.dict()
    features_queue = manager.Queue()
    i = 1

    for name in features_name:
        features_and_index[name]=i
        features_queue.put(name)
        i+=1
    for i in range (n):
        pool.apply_async(micscore,(dataset,features_queue,features_and_index,mic_score))
    pool.close()
    pool.join()
    mic_score =[(a,b) for a,b in mic_score.items()]
    mic_score = sorted(mic_score,key = lambda x:x[1],reverse=True)
    mic_features =[x[0] for x in mic_score]
    return mic_features,features_name
def micscore(dataset,features_queue,features_and_index,mic_score):
    #print('. ',end='')

    mine = MINE(alpha=0.6, c=15)
    Y = dataset[:,0]

    while not features_queue.empty():
        name = features_queue.get()
        i = features_and_index[name]
        X=dataset[:,i]

        mine.compute_score(X, Y)
        score=mine.mic()
        mic_score[name]= score

    return mic_score

def run(filecsv,logger):
    logger.info('mic start...')
    datas = readData(filecsv)
    'mic,features_name = micscore(datas)'
    mic, features_name=multi_processing_mic(datas)
    #print()

    logger.info('mic end.')
    return mic,list(features_name)

if __name__ == '__main__':
    a=datetime.datetime.now()
    mic=run('20.csv')
    print(mic)
    b = datetime.datetime.now()
    print((b-a).seconds)   #427



