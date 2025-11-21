# Any function that will be useed in common by all , for example, settinmg up MOnmgoDB client, otr savinmg model in Cloud, we can  write teh saving code over here
import os
import sys
from src.logger import logging
from src.exception import CustomException
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

import numpy as np
import pandas as pd
import dill  # Library which helps to create pil file

def save_object(path,obj):
    try:
        logging.info("Into the try block of saving teh pkle file")
        dir_path = os.path.dirname(path)

        os.makedirs(dir_path,exist_ok=True)

        with open(path,'wb') as file_obj:
            dill.dump(obj,file_obj)

    except Exception as e:
        CustomException(e,sys)

def evaluate_model(x_train,y_train,x_test,y_test,models,params):
    try:
        report={}
        for name,model in models.items():
            para = params[name]
            gs = GridSearchCV(model,para,cv=3)
            gs.fit(x_train,y_train)
            model.set_params(**gs.best_params_)
            model.fit(x_train,y_train)
            train_pred = model.predict(x_train)
            test_pred = model.predict(x_test)
            train_score = r2_score(y_train,train_pred)
            test_score = r2_score(y_test,test_pred)
            report[name] = test_score
        return report
    except Exception as e:
        raise CustomException(e,sys)
