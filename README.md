## mrmd2.0.py 
 
#### 1. Installation：
Please use the python3.6 , some packages do not support higher versions.  
##### 1.1 Linux(ubuntu):  

  ```
  pip3 install -r requirements.txt 
  ```  
 Then unzip pymrmr.zip and go to the unzipped folder：       
 
  ```
  python3 setup.py install
  ```  
  If there is a problem during the installation process, you can try the following commands based on the error message： 
  
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

##### 1.3  Windows:

 ```
 pip3 install -r requirements.txt
 ```
  Then unzip pymrmr.zip and go to the unzipped folder：   
 ```
 python3 setup.py install  
 ``` 
  If there is a problem with windows, you can refer to the above linux.
  
 #### 2. usage:

 ```
 python3  mrmd2.0.py  -i input.csv -s start_index -e end_index -l Step_length  -o metrics.csv  -c Dimensionalized_dataset.csv.csv
 ```
 
*note: The program can select a certain interval of the data set feature sequence for dimensionality reduction, so you need to select the specified parameter -s, -e. If you want to reduce the dimension of the entire data set, you only need to specify -s 1 , -e -1*

 * -i  the input dataset, supports csv,arff and libsvm 
 
 * -s the location where the user specified interval begins 
 
 * -e User-specified interval ending position 
 
 * -l step length （Larger steps will execute faster, and smaller results will be better.）
 
 * -o  Some indicators of the dimensionality reduction data set 
 
 * -c  Dimensionalized data set 
 
 The data output by the terminal can be found in the Logs directory. Please find the results in 'Results' folder. 

 #### 3. Example
 * Test.csv is a 150-dimensional dataSet
 * First select a dimension reduction interval (here from the first feature to the 150th feature, that is, the dimension reduction of the entire feature data set, of course, you can also choose one of the other continuous feature intervals)  
 * Step size is set to 1  
 
```
python3  mrmd2.0.py  -i test.csv -s 1 -e -1 -l  1  -o metrics.csv  -c Dimensionalized_dataset.csv
```

