# ─────────────────────────────────────────────
# modules/model_manager.py  —  ModelManager class
# Responsibilities:
#   • Train LinearRegression
#   • Compute evaluation metrics
#   • Predict a single prepared row
# ─────────────────────────────────────────────

import numpy as np
import pandas as pd
from dataclasses import dataclass
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from config import TARGET


@dataclass
class Metrics:
    mae:  float
    mse:  float
    rmse: float
    r2:   float


class ModelManager:
    """Wraps LinearRegression training, evaluation and inference."""

    def __init__(self):
        self.model: LinearRegression = None
        self.X_train = None
        self.X_test  = None
        self.y_train = None
        self.y_test  = None
        self.feature_names: list = []

    # ── Split ─────────────────────────────────────────────────
    def split(self, df: pd.DataFrame, test_pct: float = 0.2):
        """Split df_final into train / test sets."""
        X = df.drop(columns=[TARGET])
        y = df[TARGET]
        self.feature_names = X.columns.tolist()
        (self.X_train, self.X_test,
         self.y_train, self.y_test) = train_test_split(
            X, y, test_size=test_pct, random_state=42
        )
        return self.X_train, self.X_test, self.y_train, self.y_test

    # ── Train ─────────────────────────────────────────────────
    def train(self) -> LinearRegression:
        """Fit the model on training data."""
        if self.X_train is None:
            raise RuntimeError("Appelez split() avant train().")
        self.model = LinearRegression()
        self.model.fit(self.X_train, self.y_train)
        return self.model

    @property
    def intercept(self) -> float:
        return self.model.intercept_

    @property
    def coefficients(self) -> pd.DataFrame:
        df = pd.DataFrame({
            "Variable":    self.feature_names,
            "Coefficient": self.model.coef_,
        })
        return df.reindex(
            df["Coefficient"].abs().sort_values(ascending=False).index
        )

    # ── Evaluate ──────────────────────────────────────────────
    def evaluate(self) -> tuple[np.ndarray, Metrics]:
        """Run prediction on test set and return (y_pred, Metrics)."""
        if self.model is None:
            raise RuntimeError("Le modèle n'est pas encore entraîné.")
        y_pred = self.model.predict(self.X_test)
        metrics = Metrics(
            mae  = mean_absolute_error(self.y_test, y_pred),
            mse  = mean_squared_error(self.y_test,  y_pred),
            rmse = float(np.sqrt(mean_squared_error(self.y_test, y_pred))),
            r2   = r2_score(self.y_test, y_pred),
        )
        return y_pred, metrics

    # ── Predict ───────────────────────────────────────────────
    def predict(self, row: pd.DataFrame) -> float:
        """Predict profit for a single prepared row."""
        if self.model is None:
            raise RuntimeError("Le modèle n'est pas encore entraîné.")
        return float(self.model.predict(row)[0])
