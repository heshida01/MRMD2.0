# mrmd2.0.py 
[WebServer](http://lab.malab.cn:5001/MRMD2.0/Home) ,  [Chinese version](https://github.com/heshida01/MRMD2.0/blob/master/README_CN.md)
# News  
### The mrmd2.0 environment can now be deployed with docker.   
[Docker installation reference1](https://www.docker.com/products/docker-desktop)  ,   [Docker installation reference2](https://github.com/komavideo/LearnDocker/tree/master/Lesson02)  
##### pull the image
  ```
  sudo docker pull heshida/mrmd2.0:latest
  ```  
##### usage:  
  ```
  sudo python3 docker_mrmd2.0.py -i test.csv
  ```
  Please find the results in 'Results' folder

###  If you don't want to use docker,You can also install it using the following method:
#### 1. Installation：
We recommend using Aanconda(must python3.6), support linux,windows.  


  ```
  pip3 install -r requirements.txt 
  ```  

  ##### note:
  If the installation of a Windows user's mine package fails, download the corresponding version of the WHL file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/) to install it.
  
 #### 2. usage:

 ```
 python3  mrmd2.0.py  -i input.csv -s start_index -e end_index -l Step_length  -o metrics.csv  -c Dimensionalized_dataset.csv
 ```
 
*note: The program can select a certain interval of the data set feature sequence for dimensionality reduction, so you need to select the specified parameter -s, -e. If you want to reduce the dimension of the entire data set, you only need to specify -s 1 , -e -1*

 * -i  the input dataset, supports csv,arff and libsvm 
 
 * -s the location where the user specified interval begins （default 1）
 
 * -e User-specified interval ending position （default -1）
 
 * -l step length （default 1，Larger steps will execute faster, and smaller results will be better.）
 
 * -o  Some indicators of the dimensionality reduction data set 
 
 * -c  Dimensionalized data set 
 
 The data output by the terminal can be found in the Logs directory. Please find the results in 'Results' folder. 

 #### 3. Example
 * Test.csv is a 150-dimensional dataSet
 * First select a dimension reduction interval (here from the first feature to the 150th feature, that is, the dimension reduction of the entire feature data set, of course, you can also choose one of the other continuous feature intervals)  
 * Step size is set to 1  
 
```
python3  mrmd2.0.py  -i test.csv -o metrics.csv  -c Dimensionalized_dataset.csv
python3  mrmd2.0.py  -i test.arff -o metrics.csv  -c Dimensionalized_dataset.arff
python3  mrmd2.0.py  -i test.libsvm -o metrics.csv  -c Dimensionalized_dataset.libsvm
```
#### 4. FAQs
* problem1: ERROR: Cannot uninstall 'PyYAML'. It is a distutils installed project and thus we cannot accurately determine which files belong to it which would lead to only a partial uninstall.   
solve1: pip install -r requirements.txt  --ignore-installed
*************************
* problem2:  error: command 'x86_64-conda_cos6-linux-gnu-gcc' failed with exit status 1.   
solve2:  conda install gxx_linux-64
#### 5. logs
delete pymrmr  
add rfe , chi2  

If you have any questions.please contact me (heshida@tju.edu.cn)
