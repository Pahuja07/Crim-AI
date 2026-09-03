# src/criminalNetwork/components/data_preprocessing.py

import pandas as pd

from src.criminalNetwork.utils.logger import logger
from src.criminalNetwork.entity.config_entity import DataPreprocessingConfig
from src.criminalNetwork.utils.common import read_yaml


class Preprocessing:
    def __init__(self, config: DataPreprocessingConfig):
        self.config = config

    def load_data(self) -> pd.DataFrame:
        logger.info(f"[{self.config.dataset_name}] Loading raw data from {self.config.raw_path}")
        return pd.read_csv(self.config.raw_path)

    def load_mapping(self) -> dict:
        logger.info(f"[{self.config.dataset_name}] Loading mapping from {self.config.mapping_file}")
        mapping = read_yaml(self.config.mapping_file)
        return mapping

    def apply_column_mapping(self, df: pd.DataFrame, column_mapping: dict) -> pd.DataFrame:
        logger.info(f"[{self.config.dataset_name}] Renaming columns to canonical schema")
        df = df.rename(columns=column_mapping)
        # sirf wahi columns rakho jo mapping mein define hain (canonical schema)
        canonical_cols = list(column_mapping.values())
        keep_cols = [c for c in canonical_cols if c in df.columns]
        df = df[keep_cols]
        return df

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info(f"[{self.config.dataset_name}] Cleaning: trimming, dropping full duplicates")
        df = df.drop_duplicates()

        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].astype(str).str.strip()

        if "phone" in df.columns:
            df["phone"] = df["phone"].str.replace(r"\D", "", regex=True)

        if "address" in df.columns:
            df["address"] = df["address"].str.lower()

        return df

    def add_source_column(self, df: pd.DataFrame) -> pd.DataFrame:
        df["source_dataset"] = self.config.dataset_name
        return df

    def save_data(self, df: pd.DataFrame):
        logger.info(f"[{self.config.dataset_name}] Saving processed data to {self.config.processed_path}")
        df.to_csv(self.config.processed_path, index=False)

    def initiate_preprocessing(self):
        df = self.load_data()
        column_mapping = self.load_mapping()
        df = self.apply_column_mapping(df, column_mapping)
        df = self.clean_data(df)
        df = self.add_source_column(df)
        self.save_data(df)
        logger.info(f"[{self.config.dataset_name}] Preprocessing completed")
