from math import ceil
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate
from feature_Rank import feature_rank
import argparse
import sklearn.metrics
import time
import logging
import os
from scipy.io import arff
from sklearn.datasets import load_svmlight_file
from sklearn.datasets import dump_svmlight_file
from format import pandas2arff

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", type=int, help="start index")
    parser.add_argument("-i", type=str, help="input file")
    parser.add_argument("-e", type=int, help="end index")
    parser.add_argument("-l",  type=int, help="step length")
    parser.add_argument("-m", type=int, help="mrmr features top n",default=-1)
    parser.add_argument("-o", type=str, help="result score file")
    parser.add_argument("-c", type=str, help="output  file")
    args = parser.parse_args()

    return args

class Dim_Rd(object):

    def __init__(self,file_csv,logger):
        self.file_csv=file_csv
        self.logger = logger
    def read_data(self):  #default csv

        def read_csv():
            self.df = pd.read_csv(self.file_csv).dropna(axis=1)
            datas = np.array(self.df)
            self.datas = datas
            self.X = datas[:, 1:]
            self.y = datas[:, 0]

        file_type = self.file_csv.split('.')[-1]
        if file_type == 'csv':
            read_csv()
            # self.df=pd.read_csv(self.file_csv).dropna(axis=1)
            # datas = np.array(self.df)
            # self.datas=datas
            # self.X=datas[:,1:]
            # self.y=datas[:,0]



    def range_steplen(self, start=1, end=1, length=1):
        self.start = start
        self.end = end
        self.length = length

    def Randomforest(self,X,y):
        clf = RandomForestClassifier(random_state=1, n_estimators=100)
        clf.fit(X,y)
        cv_results=cross_validate(clf,X,y,return_train_score=False,cv=10,n_jobs=-1)
        ypred = sklearn.model_selection.cross_val_predict(clf, X, y, n_jobs=-1, cv=10)
        f1=sklearn.metrics.f1_score(y,ypred,average='weighted')
        precision = sklearn.metrics.precision_score(self.y, ypred, average='weighted')
        recall = sklearn.metrics.recall_score(self.y, ypred, average='weighted')
        roc = sklearn.metrics.roc_auc_score(self.y, ypred, average='weighted')

        return cv_results['test_score'].mean(),f1,precision,recall,roc

    def Result(self,seqmax,clf,features,csvfile):
        ypred = sklearn.model_selection.cross_val_predict(clf,self.X[:,seqmax],self.y, n_jobs=-1,cv=10)
        confusion_matrix = sklearn.metrics.confusion_matrix(self.y,ypred,)

        TP = confusion_matrix[1, 1]
        TN = confusion_matrix[0, 0]
        FP = confusion_matrix[0, 1]
        FN = confusion_matrix[1, 0]
        logger.info('***confusion matrix***')
        #f.write(('***confusion matrix***'+'\n'))
        s1 = '{:<15}'.format('')
        #f.write(s1)
        s2 = '{:<15}'.format('pos_class')
        #f.write(s2)
        s3 = '{:<15}'.format('neg_class')
        #f.write(s3 )
        logger.info(s1+s2+s3)

        s1 = '{:<15}'.format('pos_class')
        #f.write(s1)
        s2 = 'TP:{:<15}'.format(TP)
        #f.write(s2)
        s3 = 'FN:{:<15}'.format(FN)
        #f.write(s3)
        logger.info(s1 + s2 + s3)

        s1 = '{:<15}'.format('neg_class')
        #f.write(s1)
        s2 = 'FP:{:<15}'.format(FP)
        #f.write(s2)
        s3 = 'TN:{:<15}'.format(TN)
        #f.write(s3)
        logger.info(s1+s2+s3)
        acc = sklearn.metrics.accuracy_score(self.y,ypred,)

        logger.info('accuarcy = {:} '.format(acc))
        #f.write('accuarcy = {:} \n'.format(acc))
        precision = sklearn.metrics.precision_score(self.y,ypred,average='weighted')
        logger.info('precision ={} '.format(precision))
        #f.write('precision ={} \n'.format(precision))
        recall = sklearn.metrics.recall_score(self.y,ypred,average ='weighted')
        logger.info(('recall ={}'.format(recall)))
        #f.write('recall ={}\n '.format(recall))
        f1 = sklearn.metrics.f1_score(self.y,ypred,average='weighted')
        #f.write('f1 ={}\n '.format(f1))
        logger.info(('f1 ={} '.format(f1)))
        roc = sklearn.metrics.roc_auc_score(self.y,ypred,average='weighted')
        #f.write('roc area = {}\n'.format(roc))
        logger.info('roc area = {}'.format(roc))
        #with open('test.arff') as f:
        #data=np.concatenate((self.y,self.X[:,seqmax]),axis=1)
        columns_index=[0]
        columns_index.extend([i+1 for i in seqmax])
        data = np.concatenate((self.y.reshape(len(self.y),1), self.X[:, seqmax]),axis=1)
        features_list=(self.df.columns.values)

        df=pd.DataFrame(data,columns=features_list[columns_index])
        df.to_csv(csvfile,index=None)
    def Dim_reduction(self,features,features_sorted,outfile,csvfile):
        logger.info("Start dimension reduction ...")
        features_number=[]
        for value in features_sorted:
            features_number.append(features[value[0]]-1)
        stepSum=0
        max=0
        seqmax=[]
        scorecsv=outfile
        '''
        datadict = { }  #记录数据指标 画图用

        def line_chart(datadict):  #画图
            x_axis = datadict['len']
            datadict.pop('len')
            line = Line("metrics line")
            for metric_name in datadict:
                line.add(
                    metric_name,
                    x_axis,
                    datadict[metric_name]
                )
        
            line.render()
        '''
        with open(scorecsv,'w') as f:
            f.write('length,accuracy,f1,precision,recall,roc\n')
            for i in range(int(ceil((self.end-self.start)/self.length))+1):
                if (stepSum + self.start )<self.end:
                    n=stepSum + self.start
                else:
                    n=self.end

                stepSum+=self.length

                ix = features_number[self.start - 1:n]
                acc,f1,precision,recall,roc = self.Randomforest(self.X[:, ix], self.y)
                if acc > max:
                    max = acc
                    seqmax = ix

                '''
                logger.info('length={} accuarcy={:0.4f} f1={:0.4f} '.format( len(ix),acc,f1))
                f.write('{},{:0.4f},{:0.4f}\n'.format(len(ix),acc,f1))
                #sklearn.metrics.f1_score(self.y, ypred, average='weighted')
                '''
                logger.info('length={} accuarcy={:0.4f} f1={:0.4f} precision={:0.4f} recall={:0.4f} roc={:0.4f} '.format(len(ix), acc, f1,precision,recall,roc))
                f.write('{},{:0.4f},{:0.4f},{:0.4f},{:0.4f},{:0.4f}\n'.format(len(ix), acc,f1,precision,recall,roc))

                # datadict['len'].append(len(ix))
                # datadict['acc'].append(acc)
                # datadict['f1'].append(f1)
                # datadict['precision'].append(precision)
                # datadict['recall'].append(recall)
                # datadict['roc'].append(roc)
                '''
                datadict.setdefault('len',[]).append(len(ix))
                datadict.setdefault('acc', []).append(acc)
                datadict.setdefault('f1', []).append(f1)
                datadict.setdefault('precision', []).append(precision)
                datadict.setdefault('recall', []).append(recall)
                datadict.setdefault('roc', []).append(roc)
              
        line_chart(datadict)
        '''

        logger.info('----------')
        logger.info('the max acc = {:0.4f}'.format(max))


        index_add1 = [x + 1 for x in seqmax]
        logger.info('{},length = {}'.format(self.df.columns.values[index_add1],len(seqmax)))
        logger.info('-----------')
        clf = RandomForestClassifier(random_state=1, n_estimators=100)
        self.Result(seqmax,clf,features,csvfile)
        logger.info('-----------')

    def run(self,inputfile):

        args = parse_args()
        file = inputfile

        outputfile =args.o
        csvfile = args.c
        mrmr_featurLen = args.m
        features,features_sorted=feature_rank(file,self.logger,mrmr_featurLen)
        self.read_data()
        self.range_steplen(args.s, args.e, args.l)
        outputfile = os.getcwd()+os.sep+'Results'+os.sep+outputfile
        csvfile = os.getcwd()+os.sep+'Results'+os.sep+csvfile
        self.Dim_reduction(features,features_sorted,outputfile,csvfile)

def arff2csv(file):
    data = arff.loadarff(file)
    df = pd.DataFrame(data[0])
    df['class'] = df['class'].map(lambda x:x.decode())

    # eg: 0  1    2     3     4  mean =>>  mean   0     1     2    3    4 in dataframe
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]

    file_csv = file+'.csv'
    df.to_csv(file_csv,index=None)
    return file_csv

def libsvm2csv(file):
    data = load_svmlight_file(file)
    df = pd.DataFrame(data[0].todense())
    df['class'] = pd.Series(np.array(data[1])).astype(int)

    # eg: 0  1    2     3     4  mean =>>  mean   0     1     2    3    4 in dataframe
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]

    file_csv = file + '.csv'
    df.to_csv(file_csv, index=None)

    return file_csv

if __name__ == '__main__':

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    log_path = os.getcwd() + os.sep+'Logs'+os.sep
    rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    log_name = log_path + rq + '.log'
    logfile = log_name
    fh = logging.FileHandler(logfile, mode='w')
    fh.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # logging.basicConfig(level=logging.INFO,
    #                     format='[%(asctime)s]: %(message)s')  # logging.basicConfig函数对日志的输出格式及方式做相关配置
    formatter = logging.Formatter('[%(asctime)s]: %(message)s')
    #文件
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    #控制台
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.info("---mrmd 2.0 start----")

    args = parse_args()
    file = args.i

    file_type = file.split('.')[-1]
    if file_type == 'csv':
        pass
    elif file_type == 'arff':
        file = arff2csv(file)
    elif file_type == 'libsvm':

        file = libsvm2csv(file)
    else:
        assert "format error"
    #format : arff or libsvm to csv
    if args.e == -1:
        args.e = len(pd.read_csv(file).columns) - 1
    d=Dim_Rd(file,logger)

    d.run(inputfile=file)
    outputfile = os.getcwd() + os.sep + 'Results' + os.sep + args.o
    csvfile = os.getcwd() + os.sep + 'Results' + os.sep + args.c
    logger.info("The  output by the terminal's log has been saved in the {}.".format(logfile))
    logger.info('metrics have been saved in the {}.'.format(outputfile))

    #处理输出文件的类型
    if file_type == 'csv':
        logger.info('reduced dimensional dataset has been saved in the {}.'.format(csvfile))

    elif file_type == 'arff':
        df = pd.read_csv(csvfile)
        filename, ext = os.path.splitext(args.i)

        if df['class'].dtype == np.float:
            df['class'] = df['class'].astype(int)
        temp = df['class']
        df = df.drop(columns=['class'], axis=1)
        df['class'] = temp
        DimensionReduction_filename = os.path.abspath('./Result') + filename + '.Dimensionality_reduction' + '.arff'
        pandas2arff.pandas2arff(df, DimensionReduction_filename, wekaname=filename, cleanstringdata=False, cleannan=True)
        logger.info('reduced dimensional dataset has been saved in the {}.'.format(csvfile))
        #clean_csv(csvfile)

    elif file_type == 'libsvm':
        df = pd.read_csv(csvfile)
        for x in df.columns:
            if x.lower() == 'class':
                label = x
                break
        y = df[label]
        X = df.drop(columns=label, axis=1)

        inputfile = args.i
        filename ,ext = os.path.splitext(inputfile)
        DimensionReduction_filename = os.path.abspath('./Result')+filename + '.Dimensionality_reduction'+'.libsvm'
        dump_svmlight_file(X, y, DimensionReduction_filename, zero_based=True, multilabel=False)
        logger.info('reduced dimensional dataset has been saved in the {}.'.format(csvfile))

    logger.info("---mrmd 2.0 end---")
