from src.data_ingestion import DataIngestion
from src.datapreprocessing import Data_Processor
from src.model_training import ModelTraining
from utils.common_functions import read_yaml
from config.path_config import *

if __name__ == "__main__":
    ## 1. data ingestion
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()
    ## 2. Data Processing
    processor = Data_Processor(TRAIN_FILE_PATH,TEST_FILE_PATH,PROCESSED_DIR,CONFIG_PATH)
    processor.process()
    ## Model training
    trainer = ModelTraining(PROCESSED_TRAIN_DATA_PATH,PROCESSED_Test_DATA_PATH,MODEL_OUTPUT_PATH)
    trainer.run()