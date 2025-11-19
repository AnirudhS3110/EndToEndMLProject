# Any function that will be useed in common by all , for example, settinmg up MOnmgoDB client, otr savinmg model in Cloud, we can  write teh saving code over here
import os
import sys
from src.logger import logging
from src.exception import CustomException

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