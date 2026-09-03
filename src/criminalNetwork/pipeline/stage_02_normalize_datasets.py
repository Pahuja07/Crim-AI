# src/criminalNetwork/pipeline/stage_02_data_preprocessing.py

from src.criminalNetwork.config.configuration import ConfigurationManager
from src.criminalNetwork.components.data_preprocessing import Preprocessing
from src.criminalNetwork.utils.logger import logger

STAGE_NAME = "Data Preprocessing Stage"

# in datasets ko config.yaml ke "datasets" section se bhi dynamically nikala ja sakta hai,
# yahan explicit rakha hai clarity ke liye
class DataPreprocessingPipeline:
    def __init__(self):
        self.config_manager = ConfigurationManager()

    def normalise_datasets(self, dataset_names: list = None):
        """
        Har dataset ke liye Preprocessing run karta hai — raw CSV se
        canonical-schema wali processed CSV banata hai (data/processed/*.csv).
        """
        dataset_names = dataset_names or list(self.config_manager.config["datasets"].keys())

        for dataset_name in dataset_names:
            try:
                logger.info(f">> Normalising dataset: {dataset_name}")
                preprocessing_config = self.config_manager.get_data_preprocessing_config(dataset_name)
                preprocessing = Preprocessing(config=preprocessing_config)
                preprocessing.initiate_preprocessing()
                logger.info(f">> Done: {dataset_name}")
            except Exception as e:
                logger.exception(f"Failed while normalising dataset '{dataset_name}': {e}")
                raise e

    def main(self, dataset_names: list = None):
        self.normalise_datasets(dataset_names)


if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataPreprocessingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
