import sys

from src.criminalNetwork.components.entity_resolution import EntityResolution
from src.criminalNetwork.config.configuration import ConfigurationManager
from src.criminalNetwork.utils.exception import CriminalNetworkException
from src.criminalNetwork.utils.logger import logger

STAGE_NAME = "Entity Resolution Stage"


class EntityResolutionPipeline:
    def main(self):
        try:
            config = ConfigurationManager().get_entity_resolution_config()
            return EntityResolution(config).run()
        except Exception as error:
            raise CriminalNetworkException(error, sys) from error


if __name__ == "__main__":
    logger.info(">>>>>> stage %s started <<<<<<", STAGE_NAME)
    EntityResolutionPipeline().main()
    logger.info(">>>>>> stage %s completed <<<<<<", STAGE_NAME)
