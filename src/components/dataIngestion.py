# This will contain coddes of reading the datass
# Dividing the Dataset into Traininf and Test

import os
import sys
from src.exception import CustomException
from src.logger import logging

import pandas as pd
from sklearn.model_selection import train_test_split

from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTraining

from dataclasses import dataclass

@dataclass # using this we can directly Declare and assign Class variable without having any init function, we can use this if  we are only definig variables in a class and nothing other than that
class DataInjectionConfig:
    train_data_path: str = os.path.join('artifacts','train.csv')
    test_data_path: str = os.path.join('artifacts','test.csv')
    raw_data_path: str = os.path.join('artifacts','data.csv')
    # Now this Data Ingestion Component Knows where to save the test ,test and raw parts of the data

class DataIngestion:
    def __init__(self):
        self.dataIngestion  = DataInjectionConfig() #Through this Datainhestion gets all the path nameslo
    
    def initiate_ingestion(self):
        try:
            df = pd.read_csv("notebook/data/stud.csv")
            logging.info("Read the Dataset")
            os.makedirs(os.path.dirname(self.dataIngestion.raw_data_path), exist_ok=True)

            df.to_csv(self.dataIngestion.raw_data_path,header=True,index=False)
            train,test = train_test_split(df, test_size=0.2, random_state=42)
            train.to_csv(self.dataIngestion.train_data_path,header=True,index=False)
            test.to_csv(self.dataIngestion.test_data_path,header=True,index=False)
            logging.info("Dataset was splitted and stored, End of Data Ingestion")

            return(
                self.dataIngestion.train_data_path,
                self.dataIngestion.test_data_path
            )
        
        except Exception as e:
            raise CustomException(e,sys)


if __name__ =="__main__":
    obj = DataIngestion()
    train, test = obj.initiate_ingestion()
    
    data_transformation = DataTransformation()
    train_arr,test_arr,preprocessor_path=data_transformation.initiate_data_transformation(train,test)

    model_trainer = ModelTraining()
    best_score = model_trainer.initiate_training(train_arr,test_arr,preprocessor_path)
    print(best_score)
