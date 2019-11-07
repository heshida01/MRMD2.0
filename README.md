## [mrmd2.0.py](http://lab.malab.cn:5001/MRMD2.0/Home)
 
#### 1. Installation：
We recommend using python3.6(support linux,windows).  


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

#### 4. logs
delete pymrmr  
add rfe , chi2  

If you have any questions.please contact me (heshida@tju.edu.cn)
