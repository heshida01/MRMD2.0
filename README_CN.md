## mrmd2.0.py 
 
#### 1. 安装：
请用python3.6，有的包不支持更高的版本。  
###### 1.1 Linux:  
  ```
  pip3 install -r requirements.txt 
  ```
  然后解压pymrmr.zip  进入解压后的文件夹：       
  ```
  python3 setup.py install   
  ```
  如果安装过程出现问题可以根据错误提示尝试下面的几个命令：   
  (linux用户必须需要提前安装下面几个包，如果出错，可以根据提示的错误信息，选择下面的命令进行安装)
  ```
   ### Command 'pip3' not found
   apt install python3-pip
   ###  ModuleNotFoundError: No module named 'setuptools'
   pip3 install setuptools 
   ### ModuleNotFoundError: No module named 'numpy'
   pip3 install numpy     
   ### error: command 'x86_64-linux-gnu-gcc' failed with exit status 1
   apt install python3-dev  
   apt install build-essential 
   ### ModuleNotFoundError: No module named 'Cython'
   pip3 install Cython
   ### ValueError: numpy.ufunc has the wrong size, try recompiling. Expected 192, got 216
   pip uninstall numpy
   pip install numpy
   ```
   
##### 1.2 docker(debian)

```
### use debian
docker pull debian
docker run -i -t debian /bin/bash

apt update

###install miniconda3 (python3.6)
apt install wget
wget  https://repo.anaconda.com/miniconda/Miniconda3-4.5.4-Linux-x86_64.sh
apt install bzip2
bash  Miniconda3-4.5.4-Linux-x86_64.sh
source ~/.bashrc

apt install git
git clone https://github.com/heshida01/MRMD2.0.git

### install packages
cd MRMD2.0
apt install build-essential
pip install numpy
pip install -r requirements.txt

apt install unzip
unzip pymrmr.zip
cd pymrmr
pip install Cython 
python setup.py install

### fix bug  "ValueError: numpy.ufunc has the wrong size, try recompiling. Expected 192, got 216"
pip uninstall numpy
pip install numpy
###test
python  mrmd2.0.py  -i test.arff -s 1 -e  -1  -l 5  -o metrics.csv  -c Dimensionalized_dataset.csv
```

###### 1.3 Windows:
  ```
  pip3 install -r requirements.txt
  ```
  然后解压pymrmr.zip  进入解压后的文件夹：  
  ```
  python3 setup.py install  
  ```
  如果windows出现问题可以参考上面linux的。
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
 python3  mrmd2.0.py  -i test.csv -s 1 -e -1 -l  1  -o metrics.csv  -c Dimensionalized_dataset.csv
 ```
