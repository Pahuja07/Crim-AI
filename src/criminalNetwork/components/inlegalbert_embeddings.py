"""LangChain-compatible embeddings backed by the Indian legal-domain InLegalBERT model."""

from __future__ import annotations

from typing import Iterable

import torch
from langchain_core.embeddings import Embeddings
from transformers import AutoModel, AutoTokenizer


class InLegalBERTEmbeddings(Embeddings):
    """Create normalized mean-pooled embeddings from InLegalBERT.

    InLegalBERT is a BERT encoder, not a SentenceTransformer. Mean pooling
    converts its contextual token representations into FAISS-ready vectors.
    """

    def __init__(
        self,
        model_name: str = "law-ai/InLegalBERT",
        device: str | None = None,
        batch_size: int = 16,
        max_length: int = 512,
    ) -> None:
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.batch_size = batch_size
        self.max_length = max_length
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)
        self.model.eval()

    @staticmethod
    def _batches(values: list[str], size: int) -> Iterable[list[str]]:
        for start in range(0, len(values), size):
            yield values[start : start + size]

    def _embed(self, texts: list[str]) -> list[list[float]]:
        vectors: list[list[float]] = []
        for batch in self._batches(texts, self.batch_size):
            encoded = self.tokenizer(
                batch, padding=True, truncation=True, max_length=self.max_length, return_tensors="pt"
            ).to(self.device)
            with torch.no_grad():
                token_embeddings = self.model(**encoded).last_hidden_state
            mask = encoded["attention_mask"].unsqueeze(-1).expand(token_embeddings.size()).float()
            pooled = (token_embeddings * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1e-9)
            vectors.extend(torch.nn.functional.normalize(pooled, p=2, dim=1).cpu().tolist())
        return vectors

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._embed(texts)

    def embed_query(self, text: str) -> list[float]:
        return self._embed([text])[0]
