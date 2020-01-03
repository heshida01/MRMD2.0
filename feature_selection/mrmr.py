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
    try:
        logger.info('mRMR start...')
        result = mRMR(filecsv)
        logger.info('mRMR end.')
    except:
        return []
    else:
        return result

if __name__ == '__main__':
    filecsv = '../mixfeature_frequency_DBD.csv'
    # df = pd.read_csv(filecsv).dropna(axis=1)
    # n = len(df.columns)-1
    #
    # a  =py_mrmr('../mixfeature_frequency_DBD.csv', len(df.columns)-1)
    # print(a)
    info = mRMR(filecsv)
    print(info)



