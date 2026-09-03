# src/criminalNetwork/components/entity_extraction.py

import pandas as pd
from pathlib import Path

from src.criminalNetwork.utils.logger import logger
from src.criminalNetwork.entity.config_entity import EntityExtractionConfig


class EntityExtraction:
    def __init__(self, config: EntityExtractionConfig):
        self.config = config
        self.exclude_columns = {"source_dataset"}

    def load_processed_dataset(self, dataset_name: str) -> pd.DataFrame:
        path = self.config.processed_paths[dataset_name]
        logger.info(f"[{dataset_name}] Loading processed data from {path}")
        return pd.read_csv(path)

    def extract_entities_from_dataset(self, df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
        records = []

        entity_columns = [c for c in df.columns if c not in self.exclude_columns]
        case_col = "case_id" if "case_id" in df.columns else None

        for idx, row in df.iterrows():
            case_id = row.get(case_col) if case_col else None

            for col in entity_columns:
                value = row.get(col)
                if pd.isna(value) or str(value).strip() == "":
                    continue

                records.append({
                    "entity_type": col.upper(),
                    "entity_value": str(value).strip(),
                    "case_id": case_id,
                    "source_dataset": dataset_name,
                    "record_id": f"{dataset_name}_{idx}",
                })

        logger.info(f"[{dataset_name}] Extracted {len(records)} entity records across {len(entity_columns)} entity types")
        return pd.DataFrame(records)

    def save_entities(self, entities_df: pd.DataFrame, dataset_name: str):
        output_path = self.config.output_dir / f"{dataset_name}_entities.csv"
        logger.info(f"[{dataset_name}] Saving {len(entities_df)} entities to {output_path}")
        entities_df.to_csv(output_path, index=False)

    def initiate_entity_extraction(self):
        for dataset_name in self.config.dataset_names:
            try:
                df = self.load_processed_dataset(dataset_name)
                entities_df = self.extract_entities_from_dataset(df, dataset_name)
                entities_df = entities_df.drop_duplicates()
                self.save_entities(entities_df, dataset_name)
            except FileNotFoundError:
                logger.warning(f"[{dataset_name}] Processed file not found, skipping")
                continue

        logger.info("Entity extraction completed successfully for all datasets")
        
