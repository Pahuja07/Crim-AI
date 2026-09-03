from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    raw_path: Path
    processed_path: Path
    mapping_file: Path


@dataclass(frozen=True)
class RelationshipExtractionConfig:
    common_entities_path: Path
    relationship_mapping_file: Path
    output_path: Path

