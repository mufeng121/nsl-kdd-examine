import pandas as pd
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from sklearn.ensemble import GradientBoostingClassifier,VotingClassifier,RandomForestClassifier
from sklearn.linear_model import SGDClassifier
#from sklearn import tree
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report, confusion_matrix, plot_confusion_matrix, plot_roc_curve
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import sys
from sklearn.metrics import plot_confusion_matrix
from sklearn.model_selection import GridSearchCV
from joblib import dump, load

import sys
import os

model = sys.argv[1]
datapath = sys.argv[2]
outputfile = "output.csv"
if len(sys.argv) == 4:
    outputfile = sys.argv[3]

os.system("zeek -r " + datapath + " ./tcpdump2gureKDDCup99/darpa2gurekddcup.zeek > ./cache/conn.list 2>/dev/null")
os.system("sort -n ./cache/conn.list > ./cache/conn_sort.list 2>/dev/null")
os.system("gcc ./tcpdump2gureKDDCup99/trafAld.c -o ./tcpdump2gureKDDCup99/trafAld 2>/dev/null")
os.system("rm *.log 2>/dev/null")
os.system("./tcpdump2gureKDDCup99/trafAld ./cache/conn_sort.list 2>/dev/null")

col_names = ["number","start_time","orig_port","resp_port","orig_ip","resp_ip","duration","protocol","service","flag","src_bytes","dst_bytes","land","wrong_fragment","urgent","hot",
            "num_failed_logins","logged_in","num_compromised","root_shell","su_attempted","num_root","num_file_creations",
            "num_shells","num_access_files","num_outbound_cmds","is_hot_logins","is_giest_login","count","srv_count",
             "serror_rate","srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate","diff_srv_rate","srv_diff_host_rate",
            "dst_host_count","dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
            "dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate",
            ]


df_test = pd.read_csv("output.csv",header=None,delimiter = " ",names=col_names)
df_ip_list = df_test.iloc[:,:6]
df_test = df_test.drop(labels=["number","start_time","orig_port","resp_port","orig_ip","resp_ip"],axis=1)
df_test.to_csv(outputfile, sep="\t")
print("Dataset is saved to", outputfile)
df_test['protocol'] = df_test['protocol'].astype('category')
df_test['protocol']= df_test['protocol'].cat.codes
df_test['service'] = df_test['service'].astype('category')
df_test['service']= df_test['service'].cat.codes
df_test['flag'] = df_test['flag'].astype('category')
df_test['flag']= df_test['flag'].cat.codes
x_test = df_test.iloc[:,:]
if '.joblib' in model:
    clf = load(model)
    y_pred = clf.predict(x_test)
    print("=========predicting==========")

    print(df_test.shape[0], "connections are examined\n")
    print((y_pred=="normal").sum(), "connections are predict to be normal\n")

    if 'dos' in y_pred:
        print("dos attack might happend!")
        print((y_pred=="dos").sum(), "connections are predict to be dos attack.\n")
    if 'probe' in y_pred:
        print("probe attack might happend!")
        print((y_pred=="probe").sum(), "connections are predict to be probe attack.\n")
    if 'r2l' in y_pred:
        print("r2l attack might happend!")
        print((y_pred=="r2l").sum(), "connections are predict to be r2l attack.\n")
    if 'u2r' in y_pred:
        print("u2r attack might happend!")
        print((y_pred=="u2r").sum(), "connections are predict to be u2r attack.\n")
        
    print("=============================")
    print("For the accuracy of this prediction, run same model with \n 'python test.py model.joblib test.csv'")

else:
    loaded_model = tf.keras.models.load_model(model)
    y_pred = np.argmax(loaded_model.predict(x_test), axis=-1)
    print(type(y_pred))
    print("=========predicting==========")

    print(df_test.shape[0], "connections are examined\n")
    print((y_pred==0).sum(), "connections are predict to be normal\n")

    if 1 in y_pred:
        print("dos attack might happend!")
        print((y_pred==1).sum(), "connections are predict to be dos attack.\n")
    if 2 in y_pred:
        print("probe attack might happend!")
        print((y_pred==2).sum(), "connections are predict to be probe attack.\n")
    if 3 in y_pred:
        print("r2l attack might happend!")
        print((y_pred==3).sum(), "connections are predict to be r2l attack.\n")
    if 4 in y_pred:
        print("u2r attack might happend!")
        print((y_pred==4).sum(), "connections are predict to be u2r attack.\n")
        
    print("=============================")
    print("For the accuracy of this prediction, run same model with \n 'python test.py model.joblib test.csv'")
