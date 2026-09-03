import sys
from src.criminalNetwork.config.configuration import ConfigurationManager
from src.criminalNetwork.components.graph_builder import GraphBuilder
from src.criminalNetwork.utils.logger import logger
from src.criminalNetwork.utils.exception import CriminalNetworkException

STAGE_NAME = "Graph Builder Stage"


class GraphBuilderPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            graph_builder_config = config.get_graph_builder_config()
            graph_builder = GraphBuilder(config=graph_builder_config)
            graph_builder.run()
        except Exception as e:
            raise CriminalNetworkException(e, sys)


if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = GraphBuilderPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
