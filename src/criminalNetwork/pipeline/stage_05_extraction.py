from src.criminalNetwork.components.case_Extraction import CaseEntityExtraction
from src.criminalNetwork.config.configuration import ConfigurationManager


class CaseExtractionPipeline:
    def main(self):
        config = ConfigurationManager().get_case_extraction_config()
        return CaseEntityExtraction(config).initiate_case_extraction()
