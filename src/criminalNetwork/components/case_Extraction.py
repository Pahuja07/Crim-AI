import csv
import json
import re
from pathlib import Path

import pandas as pd

from src.criminalNetwork.entity.config_entity import CaseExtractionConfig
from src.criminalNetwork.utils.logger import logger


class CaseEntityExtraction:
    """Extracts graph-ready entities from every case registered in the upload manifest."""

    PATTERNS = {
        "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "PHONE": r"\b(?:\+?\d[\d .()-]{7,}\d)\b",
        "DATE": r"\b(?:\d{4}-\d{2}-\d{2}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b",
        "CASE_REFERENCE": r"\b(?:FIR|CASE|CR|REPORT)[ -]?[A-Z0-9/-]{3,}\b",
    }

    def __init__(self, config: CaseExtractionConfig):
        self.config = config

    @staticmethod
    def _read_text(path: Path) -> str:
        suffix = path.suffix.lower()
        if suffix == ".txt":
            return path.read_text(encoding="utf-8", errors="ignore")
        if suffix == ".json":
            return json.dumps(json.loads(path.read_text(encoding="utf-8")))
        if suffix == ".csv":
            with path.open(encoding="utf-8", errors="ignore", newline="") as file:
                return "\n".join(" ".join(row) for row in csv.reader(file))
        if suffix == ".pdf":
            from pypdf import PdfReader
            return "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)
        if suffix in {".png", ".jpg", ".jpeg"}:
            import pytesseract
            from PIL import Image
            return pytesseract.image_to_string(Image.open(path))
        return ""

    def _extract(self, text: str, case_id: str, filename: str) -> list[dict]:
        rows = []
        for entity_type, pattern in self.PATTERNS.items():
            for value in sorted(set(re.findall(pattern, text, flags=re.IGNORECASE))):
                rows.append({
                    "case_id": case_id,
                    "entity_type": entity_type,
                    "entity_value": value.strip(),
                    "source_file": filename,
                })
        return rows

    def initiate_case_extraction(self) -> pd.DataFrame:
        if not self.config.manifest_path.exists():
            raise FileNotFoundError(f"Case-upload manifest not found: {self.config.manifest_path}")
        cases = json.loads(self.config.manifest_path.read_text(encoding="utf-8"))
        rows = []
        for case in cases:
            path = Path(case["stored_path"])
            try:
                rows.extend(self._extract(self._read_text(path), case["case_id"], case["original_filename"]))
            except Exception as error:
                logger.warning("Could not extract case file %s: %s", path.name, error)
        columns = ["case_id", "entity_type", "entity_value", "source_file"]
        entities = pd.DataFrame(rows, columns=columns).drop_duplicates()
        entities.to_csv(self.config.common_entities_path, index=False)
        logger.info("Created common graph input with %d entity record(s): %s", len(entities), self.config.common_entities_path)
        return entities
