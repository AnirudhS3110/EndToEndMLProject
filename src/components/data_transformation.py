import sys 
import os
from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException
# from src.components.dataIngestion import DataIngestion
from src.utils import save_object

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.impute import SimpleImputer # This is for handling missing values

@dataclass
class DataTransformationConfig:
    preprocessor_path = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.datatransformationconfig = DataTransformationConfig()
    
    def get_data_transformer_object(self):
        '''
        This function is Responsible for data Transformation
        '''
        try:
            numerical_cols = [ 'reading_score', 'writing_score']
            char_cols =['gender',
                        'race_ethnicity',
                        'parental_level_of_education',
                        'lunch',
                        'test_preparation_course']
            num_pipe = Pipeline(
                steps = [
                ("imputer",SimpleImputer(strategy="mean")),
                ("standardizer",StandardScaler())
                ]
            )
            char_pipeline =Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("onehotencoder",OneHotEncoder())
                ]
            )

            preprocessor= ColumnTransformer([
                ("numerictransform",num_pipe,numerical_cols),
                ("chartransform",char_pipeline,char_cols)
            ])

            logging.info("Created preprocesoing object")
            return preprocessor

        except Exception as e:
            CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        try:
            preprocessing_obj = self.get_data_transformer_object()

            logging.info("Obtained ppreprocesing object, now teh transformation begins")
            trainds = pd.read_csv(train_path)
            testds = pd.read_csv(test_path)
            target="math_score"

            input_train_ds = trainds.drop('math_score',axis=1)
            input_train_target = trainds[target]

            input_test_ds = testds.drop('math_score',axis=1)
            input_test_target = testds[target]

            input_train_array = preprocessing_obj.fit_transform(input_train_ds)
            input_test_array = preprocessing_obj.transform(input_test_ds)

            train_arr = np.c_[input_train_array, np.array(input_train_target)]
            test_arr = np.c_[input_test_array,np.array(input_test_target)]


            logging.info("Data Transformation ends")
            logging.info("Going to call save_object function")
            save_object(
                path=self.datatransformationconfig.preprocessor_path,
                obj=preprocessing_obj
            )
            logging.info("done with saving")

            return(
                train_arr,
                test_arr,
                self.datatransformationconfig.preprocessor_path
            )
        except Exception as e:
            CustomException(e,sys)






# def Transform():
#     obj = DataIngestion()
#     train_path, test_path = obj.initiate_ingestion()
#     trainds = pd.read_csv(train_path)
#     testds  = pd.read_csv(test_path)
    

#     train_charcols = trainds.select_dtypes(include="object").columns
#     train_numericcols = trainds.select_dtypes(exclude="object").columns

#     # test_charcols = testds.select_dtypes(include="object").columns
#     # test_numericcols = testds.select_dtypes(exclude="object").columns
#     preprocessor1 = ColumnTransformer([
#         ('OneHotEncoding',OneHotEncoder(),train_charcols),
#         ("Standardizer",StandardScaler(),train_numericcols)
#     ])
#     trainds = preprocessor1.fit_transform(trainds)
    # preprocessor2 = ColumnTransformer(
    #     ('OneHotEncoding',OneHotEncoder(),test_charcols),
    #     ("Standardizer",StandardScaler(),test_numericcols)
    # )
    # testds = preprocessor2.fit_transform(testds)
    


#Transform()
