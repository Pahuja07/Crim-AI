import pandas as pd

from src.criminalNetwork.entity.config_entity import RelationshipExtractionConfig
from src.criminalNetwork.utils.common import read_yaml
from src.criminalNetwork.utils.logger import logger


class RelationshipExtraction:
    """Build graph-ready relationships from extracted case entities."""

    def __init__(self, config: RelationshipExtractionConfig):
        self.config = config

    def build_relationships(self) -> pd.DataFrame:
        if not self.config.common_entities_path.exists():
            raise FileNotFoundError(f"Common entities file not found: {self.config.common_entities_path}")

        entities = pd.read_csv(self.config.common_entities_path)
        rules = read_yaml(self.config.relationship_mapping_file).get("relationships", [])
        rows: list[dict] = []

        for case_id, case_entities in entities.groupby("case_id"):
            entities_by_type = (
                case_entities.groupby("entity_type")["entity_value"]
                .apply(lambda values: values.dropna().astype(str).unique().tolist())
                .to_dict()
            )
            for rule in rules:
                source_type, target_type = rule["source"], rule["target"]
                sources = [str(case_id)] if source_type == "CASE" else entities_by_type.get(source_type, [])
                for source in sources:
                    for target in entities_by_type.get(target_type, []):
                        rows.append({"case_id": case_id, "source_entity": source,
                                     "source_type": source_type, "relation": rule["relation"],
                                     "target_entity": target, "target_type": target_type})

        columns = ["case_id", "source_entity", "source_type", "relation", "target_entity", "target_type"]
        result = pd.DataFrame(rows, columns=columns).drop_duplicates()
        self.config.output_path.parent.mkdir(parents=True, exist_ok=True)
        result.to_csv(self.config.output_path, index=False)
        logger.info("Created %d relationship record(s): %s", len(result), self.config.output_path)
        return result
