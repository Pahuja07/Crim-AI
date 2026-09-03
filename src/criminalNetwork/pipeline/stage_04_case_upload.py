from src.criminalNetwork.components.case_upload_handler import CaseUploadHandler
from src.criminalNetwork.config.configuration import ConfigurationManager


class CaseUploadPipeline:
    def main(self) -> list[dict]:
        config = ConfigurationManager().get_case_upload_config()
        return CaseUploadHandler(config).upload_cases()
