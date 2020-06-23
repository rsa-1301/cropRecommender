#Import Libraries
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import os
import pickle
import json 



Model_Data = {}
Result_Info = {}

folderPath = "D:/SEM 6/ML Project/Implementation/Split_Dataset"
SaveModelPath = "D:/SEM 6/ML Project/Implementation/Saved_Model_new"


for folder,subfolder,files in  os.walk(folderPath):
    for file in files:
                
        Path = folderPath + "/" + file 
        print(Path)
        
        cropName = file.split('.')[0]
        Model_Data[cropName] = []
        
        temp = {}
        dataset = pd.read_csv(Path)
        X = dataset.iloc[:,:-1].values
        Y = dataset.iloc[:,-1].values
        
        
        X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.2, random_state = 0)
        
        from sklearn.svm import SVR
        svr = SVR(kernel='rbf', C=100, gamma='auto', epsilon=.1)
        svr_fit = svr.fit(X_train,Y_train)
        Y_pred_svr = svr_fit.predict(X_test)
        svr_res = mean_squared_error(Y_test, Y_pred_svr)
        temp["SVR"] = svr_res
        
        from sklearn.linear_model import LinearRegression
        from sklearn.preprocessing import PolynomialFeatures
        polynomial_features= PolynomialFeatures(degree=2)
        X_train_poly = polynomial_features.fit_transform(X_train)
        X_test_poly = polynomial_features.fit_transform(X_test)
        Lin_Poly_Model = LinearRegression()
        Lin_Poly_Model.fit(X_train_poly, Y_train)
        Y_Poly_Pred = Lin_Poly_Model.predict(X_test_poly)
        poly_res = mean_squared_error(Y_test, Y_Poly_Pred)
        temp["POLY"] = poly_res        
        
        from sklearn.neural_network import MLPRegressor
        NN_reg = MLPRegressor(random_state=1, max_iter=500).fit(X_train, Y_train)
        Y_pred_NN = NN_reg.predict(X_test)
        NN_res = mean_squared_error(Y_test, Y_pred_NN)
        temp["NN"] = NN_res
        
        import xgboost as xgb
        xgb_model = xgb.XGBRegressor(objective="reg:squarederror", random_state=42)
        xgb_model.fit(X_train, Y_train)
        Y_pred_xgb = xgb_model.predict(X_test)
        xgb_res = mean_squared_error(Y_test, Y_pred_xgb)
        temp["XGB"] = xgb_res
        
        import lightgbm as ltb
        gbm_model = ltb.LGBMRegressor()
        gbm_model.fit(X_train,Y_train)
        Y_pred_gbm = gbm_model.predict(X_test)
        gbm_res = mean_squared_error(Y_test, Y_pred_gbm)
        temp["GBM"] = gbm_res
        
        s = 0
        for k in temp:
            s+=temp[k]
        avg = s/5
        Model_Data[cropName].append(avg)
        print(temp)
        Result_Info[cropName] = temp
        for k in temp:
            if(temp[k]<1 or temp[k]<avg):
                savePath = SaveModelPath + '/' + cropName + "_" + k
                Model_Data[cropName].append([savePath,temp[k]])
                if(k=="SVR"):
                    dbfile = open(savePath, 'ab')
                    pickle.dump(svr_fit, dbfile)                      
                    dbfile.close()
                elif(k=="POLY"):
                    dbfile = open(savePath, 'ab')
                    pickle.dump(Lin_Poly_Model, dbfile)                      
                    dbfile.close() 
                elif(k=="NN"):
                    dbfile = open(savePath, 'ab')
                    pickle.dump(NN_reg, dbfile)                      
                    dbfile.close() 
                elif(k=="XGB"):
                    dbfile = open(savePath, 'ab')
                    pickle.dump(xgb_model, dbfile)                      
                    dbfile.close()
                elif(k=="GBM"):
                    dbfile = open(savePath, 'ab')
                    pickle.dump(gbm_model, dbfile)                      
                    dbfile.close()
                    
        print("================================================")

json_object = json.dumps(Model_Data, indent = 4) 
with open("SavedModelInfoNew.json", "w") as outfile: 
    outfile.write(json_object)
    
json_object = json.dumps(Result_Info, indent = 4) 
with open("TrainedModelErrorInfoNew.json", "w") as outfile: 
    outfile.write(json_object)
    




