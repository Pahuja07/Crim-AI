import os
import sys
import pandas as pd

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from neo4j import GraphDatabase

from src.criminalNetwork.components.inlegalbert_embeddings import InLegalBERTEmbeddings
from src.criminalNetwork.entity.config_entity import RAGPipelineConfig
from src.criminalNetwork.utils.logger import logger
from src.criminalNetwork.utils.exception import CriminalNetworkException


class RAGPipeline:
    def __init__(self, config: RAGPipelineConfig):
        self.config = config
        self.embedding_model = InLegalBERTEmbeddings(model_name=self.config.embedding_model_name)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap,
        )
        self.chunk_metadata = []

    def load_documents(self):
        """input_documents_dir se saari .txt files load karta hai."""
        try:
            documents = []
            for root, _, files in os.walk(self.config.input_documents_dir):
                for file_name in files:
                    if not file_name.lower().endswith(".txt"):
                        continue
                    file_path = os.path.join(root, file_name)
                    loader = TextLoader(file_path, encoding="utf-8")
                    docs = loader.load()
                    for doc in docs:
                        doc.metadata["source_file"] = file_name
                    documents.extend(docs)

            logger.info(f"Loaded {len(documents)} documents from {self.config.input_documents_dir}")
            return documents
        except Exception as e:
                raise CriminalNetworkException(e, sys)

    def split_documents(self, documents):
        """Documents ko chunks mein todta hai (embedding ke liye manageable size)."""
        try:
            chunks = self.text_splitter.split_documents(documents)
            logger.info(f"Split into {len(chunks)} chunks (chunk_size={self.config.chunk_size})")
            return chunks
        except Exception as e:
                raise CriminalNetworkException(e, sys)

    def build_vector_store(self, chunks):
        """Chunks ko embed karke FAISS vector store banata hai aur disk pe save karta hai."""
        try:
            if not chunks:
                logger.warning("No chunks to index — skipping vector store build")
                return None

            for i, chunk in enumerate(chunks):
                chunk.metadata["chunk_id"] = f"{chunk.metadata.get('source_file', 'unknown')}:{i}"

            vector_store = FAISS.from_documents(chunks, self.embedding_model)
            vector_store.save_local(str(self.config.vector_store_dir))
            logger.info(f"Vector store saved to {self.config.vector_store_dir}")

            for i, chunk in enumerate(chunks):
                self.chunk_metadata.append({
                    "chunk_id": chunk.metadata["chunk_id"],
                    "source_file": chunk.metadata.get("source_file"),
                    "chunk_preview": chunk.page_content[:100].replace("\n", " "),
                })

            metadata_df = pd.DataFrame(self.chunk_metadata)
            metadata_df.to_csv(self.config.chunk_metadata_file, index=False)
            logger.info(f"Chunk metadata saved to {self.config.chunk_metadata_file}")

            return vector_store
        except Exception as e:
                raise CriminalNetworkException(e, sys)

    def link_chunks_to_graph(self, chunks):
        """Merge each indexed chunk into Neo4j as evidence linked to mentioned entities."""
        uri = self.config.neo4j_uri
        if self.config.trust_self_signed_certificate:
            uri = uri.replace("neo4j+s://", "neo4j+ssc://", 1).replace("bolt+s://", "bolt+ssc://", 1)

        try:
            driver = GraphDatabase.driver(uri, auth=(self.config.neo4j_username, self.config.neo4j_password))
            query = """
            MERGE (d:DocumentChunk {chunk_id: $chunk_id})
            SET d.source_file = $source_file, d.preview = $preview
            WITH d
            MATCH (e:Entity)
            WHERE size(e.name) >= 3 AND toLower($chunk_text) CONTAINS toLower(e.name)
            MERGE (e)-[:MENTIONED_IN]->(d)
            RETURN count(e) AS linked_entities
            """
            with driver.session(database=self.config.neo4j_database) as session:
                session.run(
                    "CREATE CONSTRAINT document_chunk_id_unique IF NOT EXISTS "
                    "FOR (d:DocumentChunk) REQUIRE d.chunk_id IS UNIQUE"
                )
                linked_count = 0
                for chunk in chunks:
                    result = session.run(
                        query,
                        chunk_id=chunk.metadata["chunk_id"],
                        source_file=chunk.metadata.get("source_file", "unknown"),
                        preview=chunk.page_content[:500],
                        chunk_text=chunk.page_content,
                    ).single()
                    linked_count += result["linked_entities"] if result else 0
            driver.close()
            logger.info(f"Linked {linked_count} entity-to-document evidence edges in Neo4j")
        except Exception as e:
            raise CriminalNetworkException(e, sys) from e

    def run(self):
        try:
            logger.info("Starting RAG pipeline stage (indexing)")

            documents = self.load_documents()
            if not documents:
                logger.warning("No documents found to index")
                return

            chunks = self.split_documents(documents)
            vector_store = self.build_vector_store(chunks)
            if vector_store is not None:
                self.link_chunks_to_graph(chunks)

            logger.info("RAG pipeline stage (indexing) completed")
        except Exception as e:
                raise CriminalNetworkException(e, sys)
