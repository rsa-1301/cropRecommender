#Import Libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder,StandardScaler
from sklearn.model_selection import train_test_split

#Import Dataset
dataset = pd.read_csv(r"D:\SEM 6\ML Project\Implementation\Datasets\apy.csv")
X = dataset.iloc[:,4:-2].values
Y = dataset.iloc[:,9:].values
print(dataset.head())
#Remove Empty records
i=0
while(i<len(Y)):
    if(np.isnan(Y[i][0]) or np.isnan(Y[i][1]) or Y[i][0] == 0 or Y[i][1] == 0):
        X = np.delete(X,i,0)
        Y = np.delete(Y,i,0)
    else:
        i+=1

std_scaler = StandardScaler()
std_scaler.fit(X[:,0:4])
#Data to be Saved
means = std_scaler.mean_ 
var = std_scaler.var_ 
print(means,var)

import pickle
dbfile = open('stdScaler', 'ab')
pickle.dump(std_scaler, dbfile)
dbfile.close()

X[:,0:4] = std_scaler.transform(X[:,0:4])
Y = Y[:,1]/Y[:,0]

cwd = {}
for i in range(len(X)):
    temp = []
    for j in range(0,4):
        temp.append(X[i][j])
    temp.append(Y[i])
    if X[i][4] not in cwd:
        cwd[X[i][4]] = []
    cwd[X[i][4]].append(temp)    

if '/' in "Arhar/Tur":
    print(True)

print("Arhar/Tur".replace('/','&'))

for key in cwd:
    df = pd.DataFrame(cwd[key])
    if '/' in key:
        key = key.replace('/','&')
    path_n = "D:\SEM 6\ML Project\Implementation\Split_Dataset\\" + key +".csv"
    df.to_csv(path_n, index = False)
