## mrmd2.0.py 
 
#### Installation：

##### Linux:  
  `pip3 install -r requirements.txt `  
 Then unzip pymrmr.zip and go to the unzipped folder：       
  `python3 setup.py install   `  
  If there is a problem during the installation process, you can try the following commands based on the error message.：  
  ` apt install python3-dev
   apt install build-essential
   pip3 install setuptools
   pip3 install numpy
   pip3 install Cython`

##### Windows:
 ` pip3 install -r requirements.txt`  
  Then unzip pymrmr.zip and go to the unzipped folder：   
 ` python3 setup.py install  `  
  If there is a problem with windows, you can refer to the above linux。
 #### usage:

 `python3  mrmd2.0.py  -i input.csv -s start_index -e end_index -l Step_length  -o metrics.csv  -c Dimensionalized_dataset.csv.csv`

 -i  the input dataset, supports csv,arff and libsvm 
 
 -s the location where the user specified interval begins 
 
 -e User-specified interval ending position 
 
 -l step length （Larger steps will execute faster, and smaller results will be better.）
 
 -o  Some indicators of the dimensionality reduction data set 
 
 -c  Dimensionalized data set 
 
 The data output by the terminal can be found in the Logs directory. Please find the results in 'Results' folder, you can also specify other directories. 
 
 #### Example
 * Test.csv is a 150-dimensional dataSet
 * First select a dimension reduction interval (here from the first feature to the 150th feature, that is, the dimension reduction of the entire feature data set, of course, you can also choose one of the other continuous feature intervals)  
 * Step size is set to 1  
 `python3  mrmd2.0.py  -i test.csv -s 1 -e 150 -l Step_length 1  -o metrics.csv  -c Dimensionalized_dataset.csv`
