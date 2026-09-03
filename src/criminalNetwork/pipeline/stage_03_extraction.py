# src/criminalNetwork/pipeline/stage_03_entity_extraction.py

from src.criminalNetwork.config.configuration import ConfigurationManager
from src.criminalNetwork.components.entity_extraction import EntityExtraction
from src.criminalNetwork.utils.logger import logger

STAGE_NAME = "Entity Extraction Stage"


class EntityExtractionPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        entity_extraction_config = config.get_entity_extraction_config()
        entity_extraction = EntityExtraction(config=entity_extraction_config)
        entity_extraction.initiate_entity_extraction()


if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = EntityExtractionPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e