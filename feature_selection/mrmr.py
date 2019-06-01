
import pandas as pd
import pymrmr
import datetime

#      pymrmr
#       This program and the respective minimum Redundancy Maximum Relevance (mRMR)
#      algorithm were developed by Hanchuan Peng <hanchuan.peng@gmail.com>for
#      the paper
#      "Feature selection based on mutual information: criteria of
#       max-dependency, max-relevance, and min-redundancy,"
#       Hanchuan Peng, Fuhui Long, and Chris Ding,
#       IEEE Transactions on Pattern Analysis and Machine Intelligence,
#       Vol. 27, No. 8, pp.1226-1238, 2005
# .
#       （ 源代码有所改动）

def py_mrmr(filecsv,select_n):

    df = pd.read_csv(filecsv).dropna(axis=1)
    n = len(df.columns)-1
    if n > 500 and n < 2000:
        n = 100
    elif n > 2000 and n < 5000:
        n = 80
    elif n > 5000 and n < 7000:
        n = 60
    elif n > 7000 and n <10000:
        n = 30
    elif n > 10000:
        n = 10
    if select_n != -1:
        n = select_n
    result=pymrmr.mRMR(df, 'MIQ', n)
    return result

def run(filecsv,logger,select_n):
    logger.info('mRMR start...')
    result = py_mrmr(filecsv,select_n)
    logger.info('mRMR end.')
    return result

if __name__ == '__main__':
    a = datetime.datetime.now()
    mrmra=run('allinvadf1.libsvm.csv')
    print(mrmra)
    b = datetime.datetime.now()

