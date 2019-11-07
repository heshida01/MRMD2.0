## [mrmd2.0.py](http://lab.malab.cn:5001/MRMD2.0/Home)
 
#### 1. 安装：
推荐python3.6
###### 1.1 Linux:  
  ```
  pip3 install -r requirements.txt 
  ```
 
 #### 2. usage:

 ```
 python3  mrmd2.0.py  -i input.csv -s start_index -e end_index -l Step_length  -o metrics.csv  -c Dimensionalized_dataset.csv.csv
 ```
  程序可以选择数据集特征序列的某一区间进行降维，所以需要选择指定参数-s,-e，如果是对整个数据集进行降维，只需指定-s 1 ,-e -1 
  
 * -i 输入的数据集，目前支持csv，arff,libsvm
 
 * -s 用户指定的降维区间开始的位置（1是数据集的第一个特征的序号，不是0）
 
 * -e 用户指定的降维区间结束的位置(-1代表最后一个特征的序号，也可以写实际的序号)
 
 * -l 区间的步长（步长设置的大一点速度会快，小一点最后的结果会更好）
 
 * -o 降维后数据集的一些指标
 
 * -c 降维后的数据集
 
 终端输出的数据可以在Logs文件中查找，结果请在Results里面查找.
 
 #### 3. Example
 * test.csv是一个150维的数据集  
 * 首先选择一个降维区间（从第1个特征到第150个特征，也就是对整个特征数据集降维,当然也可以自己选择一个其他的连续的特征区间）  
 * 步长设为1  

```
python3  mrmd2.0.py  -i test.csv -o metrics.csv  -c Dimensionalized_dataset.csv  
python3  mrmd2.0.py  -i test.arff -o metrics.csv  -c Dimensionalized_dataset.arff  
python3  mrmd2.0.py  -i test.libsvm -o metrics.csv  -c Dimensionalized_dataset.libsvm  
```

