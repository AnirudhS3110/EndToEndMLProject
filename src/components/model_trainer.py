# HEre is where training fo the model happens
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import (
    RandomForestRegressor,
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestClassifier
)
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor    
from catboost import CatBoostRegressor

from src.exception import CustomException
from src.utils import save_object,evaluate_model
from src.logger import logging

from dataclasses import dataclass
import os
import sys

@dataclass
class ModelTrainerConfig:
    train_model_path = os.path.join('artifacts','model.pkl')

class ModelTraining: 
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    
    def initiate_training(self,train_arr,test_arr,preprocesser_path):
        try:
            logging.info("Splitting training and test input data")
            x_train,y_train,x_test,y_test = (
            train_arr[:,:-1],
            train_arr[:,-1],
            test_arr[:,:-1],
            test_arr[:,-1]
            ) 
            models={
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "K-neighbours Classifier": KNeighborsRegressor(),
                "XGBClassifier": XGBRegressor(),
                "Catboost Classifier": CatBoostRegressor(),
                "Adaboost Classifer":AdaBoostRegressor()
            }
            model_report = evaluate_model(x_train,y_train,x_test,y_test,models)

            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("There is no best model")
            logging.info(f"best model found on both training and test dataset and the best score is:{best_model_score}")

            save_object(
                path=self.model_trainer_config.train_model_path,
                obj=best_model
            )
            logging.info("best model is saved!")
            return(
                 best_model_score
            )

        except Exception as e:
            raise CustomException(e,sys)
