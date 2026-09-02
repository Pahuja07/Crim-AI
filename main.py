from src.criminalNetwork.config.configuration import DataIngestion
from src.criminalNetwork.pipeline.stage_01_bulk_ingestion import load_all_raw_datasets
from src.criminalNetwork.utils.logger import logger

if __name__ == "__main__":
    logger.info(">>>>>> Stage 1: Bulk Data Ingestion started <<<<<<")
    
    config_manager = DataIngestion()
    raw_datasets = load_all_raw_datasets(config_manager)

    logger.info(">>>>>> Stage 1: Bulk Data Ingestion completed <<<<<<")
    
    # raw_datasets = {"property_stolen_and_recovered": <DataFrame>, "arrests": <DataFrame>, ...}