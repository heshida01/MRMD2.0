<<<<<<< HEAD
import os
import pandas as pd
import  subprocess
import sys


def process_terminal_info(info:str):
    info = info.split('***')[4].split()[6::4]
    return info
#http://home.penglab.com/proj/mRMR/
def mRMR(filecsv):
    df = pd.read_csv(filecsv,engine='python').dropna(axis=1)
    n = len(df.columns) - 1

    if 1000>=n>500:
        n = 500
    elif 4500>=n>1000:
        n = 300
    elif n>=4500:
        n = 100

    dirname_ = os.path.dirname(__file__)
    if sys.platform =="linux":
        if not os.access("chmod 777 {}/util/mrmr".format(dirname_), os.X_OK):  # 如果没有执行权限
            cmd0 = "chmod +x {}/util/mrmr".format(dirname_)
            subprocess.Popen(cmd0.split())
        cmd = "{}/util/mrmr -i {} -n {} ".format(dirname_,filecsv,n)
    elif sys.platform == "win32":
        cmd = "{}/util/mrmr_win32.exe -i {} -n {} ".format(dirname_,filecsv,n)
    elif sys.platform == 'darwin':
        cmd = "{}/util/mrmr_osx_maci_leopard -i {} -n {} ".format(dirname_,filecsv,n) # mac mrmr_osx_maci_leopard

    terminal_info = subprocess.Popen(cmd.split(), universal_newlines=True,stdout=subprocess.PIPE)
    features_order = process_terminal_info(terminal_info.communicate()[0])
    return  features_order


def run(filecsv,logger):
    logger.info('mRMR start...')
    result = mRMR(filecsv)
=======

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
>>>>>>> 693f4dc7a2f863b47ee6530f5ac9eb12fbe8672b
    logger.info('mRMR end.')
    return result

if __name__ == '__main__':
<<<<<<< HEAD
    filecsv = '../mixfeature_frequency_DBD.csv'
    # df = pd.read_csv(filecsv).dropna(axis=1)
    # n = len(df.columns)-1
    #
    # a  =py_mrmr('../mixfeature_frequency_DBD.csv', len(df.columns)-1)
    # print(a)
    info = mRMR(filecsv)
    print(info)


=======
    a = datetime.datetime.now()
    mrmra=run('allinvadf1.libsvm.csv')
    print(mrmra)
    b = datetime.datetime.now()
>>>>>>> 693f4dc7a2f863b47ee6530f5ac9eb12fbe8672b

