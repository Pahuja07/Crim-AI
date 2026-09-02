import os
import pandas as pd
from src.criminalNetwork.utils.logger import logger
from src.criminalNetwork.utils.exception import CriminalNetworkException
from src.criminalNetwork.config.configuration import DataIngestionConfig
import sys


def get_available_datasets(config_manager: DataIngestionConfig):
    """config.yaml ke 'datasets' block se saare dataset names nikalta hai"""
    try:
        dataset_names = list(config_manager.config.datasets.keys())
        logger.info(f"Found datasets in config: {dataset_names}")
        return dataset_names
    except Exception as e:
        raise CriminalNetworkException(e, sys)


def load_raw_dataset(config_manager: DataIngestionConfig, dataset_name: str) -> pd.DataFrame:
    """Ek dataset ka raw CSV load karta hai, config.yaml ke path ke through"""
    try:
        ingestion_config = config_manager.get_data_ingestion_config(dataset_name)
        
        if not os.path.exists(ingestion_config.raw_path):
            logger.warning(f"Raw file not found for '{dataset_name}' at {ingestion_config.raw_path}, skipping.")
            return None

        logger.info(f"Loading raw dataset: {dataset_name} from {ingestion_config.raw_path}")
        df = pd.read_csv(ingestion_config.raw_path)
        logger.info(f"Loaded '{dataset_name}' — shape: {df.shape}")
        return df

    except Exception as e:
        raise CriminalNetworkException(e, sys)


def load_all_raw_datasets(config_manager: ConfigurationManager) -> dict:
    """Saare datasets ko config se scan karke, ek-ek karke load karta hai"""
    try:
        dataset_names = get_available_datasets(config_manager)
        raw_data = {}

        for name in dataset_names:
            df = load_raw_dataset(config_manager, name)
            if df is not None:
                raw_data[name] = df

        logger.info(f"Successfully loaded {len(raw_data)} dataset(s): {list(raw_data.keys())}")
        return raw_data

    except Exception as e:
        raise CriminalNetworkException(e, sys)