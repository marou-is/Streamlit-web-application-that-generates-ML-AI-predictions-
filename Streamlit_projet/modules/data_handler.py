# ─────────────────────────────────────────────
# modules/data_handler.py  —  DataHandler class
# Responsibilities:
#   • Load CSV file
#   • Expose variables / dimensions / preview
#   • Detect missing values
# ─────────────────────────────────────────────

import pandas as pd
import numpy as np
from config import TARGET


class DataHandler:
    """Handles raw data loading and basic exploration."""

    def __init__(self, fichier):
        self.df: pd.DataFrame = pd.read_csv(fichier)

    # ── Exploration ───────────────────────────────────────────
    @property
    def shape(self) -> tuple:
        return self.df.shape

    @property
    def feature_names(self) -> list:
        return [c for c in self.df.columns if c != TARGET]

    @property
    def numeric_features(self) -> list:
        return [c for c in self.feature_names
                if pd.api.types.is_numeric_dtype(self.df[c])]

    @property
    def categorical_features(self) -> list:
        return [c for c in self.feature_names
                if not pd.api.types.is_numeric_dtype(self.df[c])]

    def head(self, n: int = 5) -> pd.DataFrame:
        return self.df.head(n)

    # ── Missing values ────────────────────────────────────────
    @property
    def missing_columns(self) -> list:
        return self.df.columns[self.df.isnull().any()].tolist()

    @property
    def missing_row_count(self) -> int:
        return int(self.df.isnull().any(axis=1).sum())

    def missing_summary(self) -> pd.DataFrame:
        counts = self.df[self.missing_columns].isnull().sum().reset_index()
        counts.columns = ["Colonne", "Nb valeurs manquantes"]
        return counts

    def category_values(self, col: str) -> list:
        """Return sorted unique values for a categorical column."""
        return sorted(self.df[col].dropna().unique().tolist())

    def median(self, col: str) -> float:
        return float(self.df[col].median())
