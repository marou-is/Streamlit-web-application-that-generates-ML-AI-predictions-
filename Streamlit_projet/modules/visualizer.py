# ─────────────────────────────────────────────
# modules/visualizer.py  —  Visualizer class
# Responsibilities:
#   • Correlation heatmap
#   • PCA variance bar chart
#   • Coefficient bar chart
#   • Real vs Predicted line chart
#   • Scatter plot
# ─────────────────────────────────────────────

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.figure import Figure

BG    = "#111827"
BLUE  = "#00e5c0"
RED   = "#e05c5c"
GREEN = "#2ecc71"
TEXT  = "#e8edf8"


def _style(fig: Figure, axes):
    fig.patch.set_facecolor(BG)
    for ax in (axes if hasattr(axes, "__iter__") else [axes]):
        ax.set_facecolor(BG)
        ax.tick_params(colors=TEXT)
        for spine in ax.spines.values():
            spine.set_edgecolor("#c0c8d8")


class Visualizer:
    """Produces all matplotlib figures used in the app."""

    # ── Correlation heatmap ───────────────────────────────────
    @staticmethod
    def correlation_heatmap(df: pd.DataFrame,
                            cols: list) -> Figure:
        fig, ax = plt.subplots(figsize=(8, 5))
        _style(fig, ax)
        sns.heatmap(
            df[cols].corr(), annot=True, fmt=".2f",
            cmap="coolwarm", linewidths=0.5,
            ax=ax, square=True,
        )
        ax.set_title("Matrice de Corrélation",
                     fontsize=13, fontweight="bold", color=TEXT)
        plt.tight_layout()
        return fig

    # ── PCA variance bar chart ────────────────────────────────
    @staticmethod
    def pca_variance(var_ratio: np.ndarray,
                     component_names: list) -> Figure:
        fig, ax = plt.subplots(figsize=(8, 5))
        _style(fig, ax)
        ax.bar(component_names, var_ratio * 100,
               color=BLUE, edgecolor="white")
        ax.set_ylabel("Variance expliquée (%)", color=TEXT)
        ax.set_title("Variance par composante principale", color=TEXT)
        plt.tight_layout()
        return fig

    # ── Coefficient bar chart ─────────────────────────────────
    @staticmethod
    def coefficients(df_coef: pd.DataFrame) -> Figure:
        fig, ax = plt.subplots(figsize=(8, 5))
        _style(fig, ax)
        colors = [BLUE if v >= 0 else RED
                  for v in df_coef["Coefficient"]]
        ax.barh(df_coef["Variable"], df_coef["Coefficient"],
                color=colors, edgecolor="white")
        ax.axvline(0, color="#333", lw=0.8, linestyle="--")
        ax.set_xlabel("Coefficient", color=TEXT)
        ax.set_title("Coefficients de Régression", color=TEXT)
        plt.tight_layout()
        return fig

    # ── Real vs Predicted line chart ─────────────────────────
    @staticmethod
    def real_vs_predicted(y_true: pd.Series,
                          y_pred: np.ndarray) -> Figure:
        fig, ax = plt.subplots(figsize=(8, 5))
        _style(fig, ax)
        ax.plot(range(len(y_true)), y_true.values,
                "o-", label="Réel",   color=BLUE,  lw=1.8, alpha=0.85)
        ax.plot(range(len(y_pred)), y_pred,
                "x--", label="Prédit", color=RED,  lw=1.8, alpha=0.85)
        ax.set_xlabel("Indice", color=TEXT)
        ax.set_ylabel("Profit ($)", color=TEXT)
        ax.set_title("Valeurs Réelles vs Prédites", color=TEXT)
        ax.legend()
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        plt.tight_layout()
        return fig

    # ── Scatter plot ──────────────────────────────────────────
    @staticmethod
    def scatter(y_true: pd.Series,
                y_pred: np.ndarray) -> Figure:
        fig, ax = plt.subplots(figsize=(6, 6))
        _style(fig, ax)
        ax.scatter(y_true, y_pred, color=GREEN,
                   alpha=0.75, edgecolors="white", s=70)
        lim = [min(y_true.min(), y_pred.min()) * 0.95,
               max(y_true.max(), y_pred.max()) * 1.05]
        ax.plot(lim, lim, "r--", lw=1.5, label="Parfait")
        ax.set_xlabel("Réel ($)", color=TEXT)
        ax.set_ylabel("Prédit ($)", color=TEXT)
        ax.set_title("Nuage de points — Réel vs Prédit", color=TEXT)
        ax.legend()
        ax.grid(linestyle="--", alpha=0.3)
        plt.tight_layout()
        return fig
