import sys
from src.criminalNetwork.config.configuration import ConfigurationManager
from src.criminalNetwork.components.graph_analytics import GraphAnalytics
from src.criminalNetwork.utils.logger import logger
from src.criminalNetwork.utils.exception import CriminalNetworkException

STAGE_NAME = "Graph Analytics Stage"


class GraphAnalyticsPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            graph_analytics_config = config.get_graph_analytics_config()
            graph_analytics = GraphAnalytics(config=graph_analytics_config)
            graph_analytics.run()
        except Exception as e:
            raise CriminalNetworkException(e, sys)


if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = GraphAnalyticsPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
