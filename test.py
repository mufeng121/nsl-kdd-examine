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

model = sys.argv[1]
test_data = sys.argv[2]

col_names = ["duration","protocol","service","flag","src_bytes","dst_bytes","land","wrong_fragment","urgent","hot",
            "num_failed_logins","logged_in","num_compromised","root_shell","su_attempted","num_root","num_file_creations",
            "num_shells","num_access_files","num_outbound_cmds","is_hot_logins","is_giest_login","count","srv_count",
             "serror_rate","srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate","diff_srv_rate","srv_diff_host_rate",
            "dst_host_count","dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
            "dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate",
            "class","difficulty_score"]


df_test = pd.read_csv(test_data,header=None, names=col_names)

df_test['protocol'] = df_test['protocol'].astype('category')
df_test['protocol']= df_test['protocol'].cat.codes
df_test['service'] = df_test['service'].astype('category')
df_test['service']= df_test['service'].cat.codes
df_test['flag'] = df_test['flag'].astype('category')
df_test['flag']= df_test['flag'].cat.codes

y_test = df_test.iloc[:,41]
x_test = df_test.iloc[:,0:41]

clf = load(model)

y_pred = clf.predict(x_test)
print("total accuracy:",metrics.accuracy_score(y_test, y_pred))
result = confusion_matrix(y_test, y_pred)

print("dos accuracy:",result[0][0]/sum(result[0]))
print("normal accuracy",result[1][1]/sum(result[1]))
print("probe accuracy",result[2][2]/sum(result[2]))
print("r2l accuracy",result[3][3]/sum(result[3]))
print("u2r accuracy",result[4][4]/sum(result[4]))

plot_confusion_matrix(clf, x_test, y_test)

print("Classification Report")
print(classification_report(y_test, y_pred))


