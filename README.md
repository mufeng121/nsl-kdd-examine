# nsl-kdd-examine
Anomaly intrusion detection system

## Setup
### Installing tools
```shell
# Install zeek for running the bro scripy
# https://docs.zeek.org/en/master/install.html for installation details
brew install zeek # with brew
```
### Installing dependencies
```shell
pip install -r requirements.txt
```

## Run
```shell
# The .pcap is the network traffic data, which can be replaced by any .pcap format file.
# The output path is the file where you want to output your own dataset with KDD attributes.
# default to be output.csv
python predict.py best_dt_clf.joblib nmap.pcap <output path>
# or
python predict.py model1 nmap.pcap <output path> 
```
<img src="media/run.png" width="80%" height="80%" />

## Notes
If you want to test the program performance with the NSK-KDD test dataset, please run: 
```shell
python test.py best_dt_clf.joblib test.csv
```

# Files -
~~~
./predict.py : main ids script
./test.py : model accuracy test script
./data_preparation_and_modeling.ipynb : notebook file used for training models

./*.joblib : trained joblib models, can be used as input to predict.py and test.py
./model1~5 : trained joblib models, can be used as input to predict.py and test.py

./*.pcap : pcap files for samlple test cases, used as input to predict.py
--./browsing_email.pcap : normal traffics when using email in browser
--./nmap.pcap : traffics of running nmap on a victim machine.
--./tcpflood.pcap : traffics of tcp SYN flood attack on a victim machine.

./*.csv : training and verifying dataset from NSL-KDD

./tcpdump2gureKDDCup99/* : tool from https://github.com/inigoperona/tcpdump2gureKDDCup99.
                          modified for service_name attribute and to run in new version zeek.
./cache/* : runtime folder for ./tcpdump2gureKDDCup99/. do not delete the folder.
~~~

  
   
