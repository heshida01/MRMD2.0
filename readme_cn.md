## mrmd2.0.py 
 
#### 安装：

### Linux:  
  `pip3 install -r requirements.txt `
  然后解压pymrmr.zip  进入解压后的文件夹：     
  `python3 setup.py install   `
  如果安装过程出现问题可以根据错误提示尝试下面的几个命令：
  ` apt install python3-dev
   apt install build-essential
   pip3 install setuptools
   pip3 install numpy
   pip3 install Cython`

### Windows:
 ` pip3 install -r requirements.txt`  
  然后解压pymrmr.zip  进入解压后的文件夹：  
 ` python3 setup.py install  `  
  如果windows出现问题可以参考上面linux的。
 #### usage:

 `python3  mrmd2.0.py  -i input.csv -s start_index -e end_index -l Step_length  -o metrics.csv  -c Dimensionalized_dataset.csv.csv`

 -i 输入的数据集，目前支持csv，arff,libsvm
 
 -s 用户指定的降维区间开始的位置
 
 -e 用户指定的降维区间结束的位置
 
 -l 区间的步长（步长设置的大一点速度会快，小一点最后的结果会更好）
 
 -o 降维后数据集的一些指标
 
 -c 降维后的数据集
 
 终端输出的数据可以在Logs文件中查找，结果请在Results里面查找，也可以指定i其他目录  
 
 ####Example
 * test.csv是一个150维的数据集  
 * 首先选择一个降维区间（从第1个特征到第150个特征，也就是对整个特征数据集降维）  
 * 步长设为1  
 `python3  mrmd2.0.py  -i test.csv -s 1 -e 150 -l Step_length 1  -o metrics.csv  -c Dimensionalized_dataset.csv`
