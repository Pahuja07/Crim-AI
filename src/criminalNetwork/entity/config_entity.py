from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    raw_path: Path
    processed_path: Path
    mapping_file: Path


@dataclass(frozen=True)
class DataPreprocessingConfig:
    root_dir: Path
    dataset_name: str
    raw_path: Path
    processed_path: Path
    mapping_file: Path


@dataclass(frozen=True)
class EntityExtractionConfig:
    root_dir: Path
    processed_data_dir: Path
    output_dir: Path
    dataset_names: list[str]
    processed_paths: dict[str, Path]


@dataclass(frozen=True)
class CaseUploadConfig:
    input_dir: Path
    upload_dir: Path
    manifest_path: Path


@dataclass(frozen=True)
class CaseExtractionConfig:
    manifest_path: Path
    output_dir: Path
    common_entities_path: Path

@dataclass(frozen=True)
class RelationshipExtractionConfig:
    common_entities_path: Path
    relationship_mapping_file: Path
    output_path: Path

@dataclass(frozen=True)
class EntityResolutionConfig:
    root_dir: Path
    input_entities_file: Path
    input_relationships_file: Path
    resolved_entities_file: Path
    resolved_relationships_file: Path
    entity_mapping_file: Path
    fuzzy_threshold: int

@dataclass(frozen=True)
class GraphBuilderConfig:
    root_dir: Path
    entity_mapping_file: Path
    resolved_entities_file: Path
    resolved_relationships_file: Path
    graph_build_log_file: Path
    graph_schema_file: Path          # ← new field
    neo4j_uri: str
    neo4j_username: str
    neo4j_password: str
    neo4j_database: str | None
    trust_self_signed_certificate: bool

@dataclass(frozen=True)
class GraphAnalyticsConfig:
    root_dir: Path
    centrality_output_file: Path
    community_output_file: Path
    top_n_report_file: Path
    top_n: int
    neo4j_uri: str
    neo4j_username: str
    neo4j_password: str
    neo4j_database: str | None
    trust_self_signed_certificate: bool


@dataclass(frozen=True)
class EvidenceIntegrityConfig:
    root_dir: Path
    input_documents_dir: Path
    hash_ledger_file: Path
    verification_report_file: Path
    hash_algorithm: str

@dataclass(frozen=True)
class RAGPipelineConfig:
    root_dir: Path
    input_documents_dir: Path
    vector_store_dir: Path
    chunk_metadata_file: Path
    embedding_model_name: str
    chunk_size: int
    chunk_overlap: int
    neo4j_uri: str
    neo4j_username: str
    neo4j_password: str
    neo4j_database: str | None
    trust_self_signed_certificate: bool
@dataclass(frozen=True)
class AgentConfig:
    vector_store_dir: Path
    embedding_model_name: str
    top_suspects_file: Path
    centrality_file: Path
    community_file: Path
    llm_model_name: str
    retrieval_k: int
    neo4j_uri: str
    neo4j_username: str
    neo4j_password: str
    neo4j_database: str | None
    trust_self_signed_certificate: bool
    openai_api_key: str

