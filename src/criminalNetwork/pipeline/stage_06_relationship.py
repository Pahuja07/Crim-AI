from src.criminalNetwork.components.relationship_extraction import RelationshipExtraction
from src.criminalNetwork.config.configuration import ConfigurationManager


class RelationshipExtractionPipeline:
    def main(self):
        config = ConfigurationManager().get_relationship_extraction_config()
        return RelationshipExtraction(config).build_relationships()

