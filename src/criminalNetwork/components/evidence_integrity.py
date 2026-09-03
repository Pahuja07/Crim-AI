import os
import sys
import hashlib
import pandas as pd
from datetime import datetime

from src.criminalNetwork.entity.config_entity import EvidenceIntegrityConfig
from src.criminalNetwork.utils.logger import logger
from src.criminalNetwork.utils.exception import CriminalNetworkException


class EvidenceIntegrity:
    def __init__(self, config: EvidenceIntegrityConfig):
        self.config = config
        self.ledger_records = []

    def _compute_hash(self, file_path: str) -> str:
        """File ka hash compute karta hai chunk-by-chunk (bade files ke liye memory-safe)."""
        try:
            hash_func = hashlib.new(self.config.hash_algorithm)
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
        except Exception as e:
            raise CriminalNetworkException(e, sys)

    def _load_existing_ledger(self) -> pd.DataFrame:
        """Pehle se ledger file hai to load karo, warna empty DataFrame banao."""
        try:
            if os.path.exists(self.config.hash_ledger_file):
                return pd.read_csv(self.config.hash_ledger_file)
            return pd.DataFrame(columns=["file_name", "file_path", "hash", "algorithm", "timestamp", "status"])
        except Exception as e:
            raise CriminalNetworkException(e, sys)

    def register_documents(self):
        """input_documents_dir mein saari files ka hash compute karke ledger mein register karta hai."""
        try:
            existing_ledger = self._load_existing_ledger()
            existing_paths = set(existing_ledger["file_path"]) if not existing_ledger.empty else set()

            new_count = 0
            for root, _, files in os.walk(self.config.input_documents_dir):
                for file_name in files:
                    file_path = os.path.join(root, file_name)

                    if file_path in existing_paths:
                        continue  # already registered, skip (verification alag se hogi)

                    file_hash = self._compute_hash(file_path)
                    self.ledger_records.append({
                        "file_name": file_name,
                        "file_path": file_path,
                        "hash": file_hash,
                        "algorithm": self.config.hash_algorithm,
                        "timestamp": datetime.now().isoformat(),
                        "status": "registered",
                    })
                    new_count += 1

            if new_count == 0:
                logger.info("No new documents found to register")
                return existing_ledger

            new_ledger_df = pd.DataFrame(self.ledger_records)
            updated_ledger = pd.concat([existing_ledger, new_ledger_df], ignore_index=True)
            updated_ledger.to_csv(self.config.hash_ledger_file, index=False)

            logger.info(f"{new_count} new documents registered in evidence ledger")
            return updated_ledger
        except Exception as e:
            raise CriminalNetworkException(e, sys)

    def verify_documents(self, ledger_df: pd.DataFrame):
        """Ledger mein registered files ka current hash recompute karke original se compare karta hai — tamper detection."""
        try:
            verification_records = []
            tampered_count, missing_count = 0, 0

            for _, row in ledger_df.iterrows():
                file_path = row["file_path"]

                if not os.path.exists(file_path):
                    verification_records.append({
                        "file_name": row["file_name"],
                        "file_path": file_path,
                        "original_hash": row["hash"],
                        "current_hash": None,
                        "verification_status": "MISSING",
                    })
                    missing_count += 1
                    logger.warning(f"Evidence file missing: {file_path}")
                    continue

                current_hash = self._compute_hash(file_path)
                is_tampered = current_hash != row["hash"]

                verification_records.append({
                    "file_name": row["file_name"],
                    "file_path": file_path,
                    "original_hash": row["hash"],
                    "current_hash": current_hash,
                    "verification_status": "TAMPERED" if is_tampered else "OK",
                })

                if is_tampered:
                    tampered_count += 1
                    logger.warning(f"TAMPER DETECTED: {file_path} — hash mismatch!")

            verification_df = pd.DataFrame(verification_records)
            verification_df.to_csv(self.config.verification_report_file, index=False)

            logger.info(
                f"Verification complete: {len(verification_df)} checked, "
                f"{tampered_count} tampered, {missing_count} missing"
            )
            return verification_df
        except Exception as e:
            raise CriminalNetworkException(e, sys)

    def run(self):
        try:
            logger.info("Starting evidence integrity stage")

            ledger_df = self.register_documents()
            if ledger_df.empty:
                ledger_df = self._load_existing_ledger()

            self.verify_documents(ledger_df)

            logger.info("Evidence integrity stage completed")
        except Exception as e:
            raise CriminalNetworkException(e, sys)