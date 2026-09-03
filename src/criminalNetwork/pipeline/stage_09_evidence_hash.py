import sys
from src.criminalNetwork.config.configuration import ConfigurationManager
from src.criminalNetwork.components.evidence_integrity import EvidenceIntegrity
from src.criminalNetwork.utils.logger import logger
from src.criminalNetwork.utils.exception import CriminalNetworkException

STAGE_NAME = "Evidence Integrity Stage"


class EvidenceIntegrityPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            evidence_integrity_config = config.get_evidence_integrity_config()
            evidence_integrity = EvidenceIntegrity(config=evidence_integrity_config)
            evidence_integrity.run()
        except Exception as e:
            raise CriminalNetworkException(e, sys)


if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = EvidenceIntegrityPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e