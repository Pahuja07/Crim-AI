from src.criminalNetwork.constants import CONFIG_FILE_PATH
from src.criminalNetwork.entity.config_entity import DataIngestionConfig, RelationshipExtractionConfig
from src.criminalNetwork.utils.common import read_yaml, create_directories


class DataIngestion:
    def __init__(self, config_filepath=CONFIG_FILE_PATH):
        self.config = read_yaml(config_filepath)
        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self, dataset_name: str) -> DataIngestionConfig:
        dataset_cfg = self.config.datasets[dataset_name]

        create_directories([self.config.data_ingestion.processed_data_dir])

        return DataIngestionConfig(
            root_dir=self.config.data_ingestion.raw_data_dir,
            raw_path=dataset_cfg.raw_path,
            processed_path=dataset_cfg.processed_path,
            mapping_file=dataset_cfg.mapping_file,
        )

    def get_relationship_extraction_config(self) -> RelationshipExtractionConfig:
        cfg = self.config.relationship_extraction

        return RelationshipExtractionConfig(
            common_entities_path=cfg.common_entities_path,
            relationship_mapping_file=cfg.relationship_mapping_file,
            output_path=cfg.output_path,
        )