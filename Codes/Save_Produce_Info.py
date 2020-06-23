#Import Libraries
import numpy as np
import pandas as pd
import os
import json 

folderPath = "./Split_Dataset"

ProduceInfo = {}

for folder,subfolder,files in  os.walk(folderPath):
    for file in files:
                
        Path = folderPath + "/" + file 
        print(Path)
        
        cropName = file.split('.')[0]
        ProduceInfo[cropName] = {}

        dataset = pd.read_csv(Path)
                                        
        Y = dataset.iloc[:,-1].values
        
        ProduceInfo[cropName]["Max"] = max(Y)
        ProduceInfo[cropName]["Min"] = min(Y)
        ProduceInfo[cropName]["Avg"] = sum(Y)/len(Y)

json_object = json.dumps(ProduceInfo, indent = 4) 
with open("ProduceInfo.json", "w") as outfile: 
    outfile.write(json_object)