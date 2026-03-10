# ─────────────────────────────────────────────
# views/preprocessing_view.py  —  PreprocessingView
# Renders steps 7–11: encode, normalise,
# correlation, PCA, final dataset
# ─────────────────────────────────────────────

import streamlit as st
import pandas as pd
import numpy as np
from modules.preprocessor import Preprocessor
from modules.visualizer import Visualizer
from modules.session_manager import SessionManager
from config import TARGET


def _sec(title): st.subheader(title)


class PreprocessingView:
    """UI for the full preprocessing pipeline (steps 7–11)."""

    # ── Step 7 — Encoding ─────────────────────────────────────
    @staticmethod
    def render_encoding(df: pd.DataFrame,
                        prep: Preprocessor,
                        cat_cols: list) -> pd.DataFrame:
        _sec("7. Encodage des Variables Catégorielles")
        df_enc = SessionManager.get("df_encoded")

        if cat_cols:
            st.info(f"Colonnes catégorielles : **{', '.join(cat_cols)}**")
            method = st.selectbox("Méthode d'encodage :", [
                "One-Hot Encoding", "Binary Encoding", "Label Encoding",
            ])
            with st.expander("Description des méthodes"):
                st.markdown("""
                - **One-Hot Encoding** : Crée une colonne binaire par catégorie.
                - **Binary Encoding** : Représentation binaire compacte.
                - **Label Encoding** : Entier unique par catégorie (commence à **1**).
                """)
            if st.button("✅ Appliquer l'Encodage"):
                df_enc = prep.encode(df, method, cat_cols)
                SessionManager.set("df_encoded", df_enc)
                SessionManager.set("enc_method",  prep.enc_method)
                SessionManager.set("enc_cols",     prep.enc_cols)
                SessionManager.save_preprocessor(prep)
                st.success(f"Encodage appliqué : **{method}**")
                st.dataframe(df_enc.head(), use_container_width=True)
        else:
            st.info("Aucune colonne catégorielle détectée.")
            if df_enc is None:
                df_enc = df.copy()
                SessionManager.set("df_encoded", df_enc)

        return df_enc if df_enc is not None else df.copy()

    # ── Step 8 — Normalisation ────────────────────────────────
    @staticmethod
    def render_normalisation(df: pd.DataFrame,
                             prep: Preprocessor) -> pd.DataFrame:
        _sec("8. 📏 Normalisation des Données")
        df_norm = SessionManager.get("df_norm")

        method = st.selectbox("Méthode de normalisation :", [
            "Aucune normalisation", "Min-Max Scaling (0-1)",
            "Standardisation Z-score", "Robust Scaling",
        ])
        with st.expander("Description des méthodes"):
            st.markdown("""
            - **Min-Max** : Ramène les valeurs entre 0 et 1.
            - **Z-score** : Moyenne=0, écart-type=1.
            - **Robust** : Basé sur la médiane, robuste aux valeurs aberrantes.
            - *Les colonnes One-Hot / Binary ne sont pas normalisées.*
            """)

        skipped = [c for c in df.columns
                   if c != TARGET
                   and not pd.api.types.is_numeric_dtype(df[c])]
        if skipped:
            st.warning(f"Colonnes non-numériques ignorées : "
                       f"**{', '.join(skipped)}**. Appliquez l'encodage d'abord.")

        if st.button("Appliquer la Normalisation"):
            df_norm = prep.normalise(df, method)
            SessionManager.set("df_norm", df_norm)
            SessionManager.save_preprocessor(prep)
            st.success(f"Normalisation appliquée : **{method}**")
            st.dataframe(df_norm.head(), use_container_width=True)

        return df_norm if df_norm is not None else df.copy()

    # ── Step 9 — Correlation ──────────────────────────────────
    @staticmethod
    def render_correlation(df: pd.DataFrame,
                           enc_method: str,
                           enc_cols: list):
        _sec("9. 🔗 Matrice de Corrélation (Attributs Numériques)")
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        if enc_method in ("One-Hot Encoding", "Binary Encoding"):
            corr_cols = [c for c in num_cols
                         if c not in enc_cols and c != TARGET]
        else:
            corr_cols = [c for c in num_cols if c != TARGET]

        if len(corr_cols) >= 2:
            fig = Visualizer.correlation_heatmap(df, corr_cols)
            st.pyplot(fig)
        else:
            st.warning("Pas assez de colonnes numériques pour la matrice.")

    # ── Step 10 — PCA ─────────────────────────────────────────
    @staticmethod
    def render_pca(df: pd.DataFrame,
                   prep: Preprocessor) -> pd.DataFrame:
        _sec("10. 🔬 Réduction de Dimensionnalité")
        df_final = SessionManager.get("df_final")

        opt = st.radio("Option :", ["Sans réduction", "Réduction avec PCA"],
                       horizontal=True)

        if opt == "Réduction avec PCA":
            numeric_X = [c for c in df.columns
                         if c != TARGET
                         and pd.api.types.is_numeric_dtype(df[c])]
            skipped = [c for c in df.columns
                       if c != TARGET
                       and not pd.api.types.is_numeric_dtype(df[c])]
            if skipped:
                st.warning(f"Colonnes non-numériques exclues de la PCA : "
                           f"**{', '.join(skipped)}**")
            if not numeric_X:
                st.error("Aucune colonne numérique. Encodez d'abord (étape 7).")
                return df_final if df_final is not None else df.copy()

            max_c = min(len(numeric_X), df.shape[0])
            n_c   = st.slider("Nombre de composantes", 1, max_c, min(2, max_c))

            if st.button("Appliquer la PCA"):
                df_pca, var_ratio = prep.apply_pca(df, n_c)
                SessionManager.set("df_final", df_pca)
                SessionManager.save_preprocessor(prep)
                st.success(f"PCA appliquée — Variance expliquée : "
                           f"**{var_ratio.sum():.2%}**")
                names = [f"CP{i+1}" for i in range(n_c)]
                fig = Visualizer.pca_variance(var_ratio, names)
                st.pyplot(fig)
                return df_pca
        else:
            SessionManager.set("df_final", df)
            prep.pca_model = None
            SessionManager.save_preprocessor(prep)

        return SessionManager.get("df_final") if \
            SessionManager.get("df_final") is not None else df.copy()

    # ── Step 11 — Final dataset ───────────────────────────────
    @staticmethod
    def render_final(df: pd.DataFrame):
        _sec("11.Jeu de Données Après Préparation Complète")
        st.dataframe(df, use_container_width=True)
        st.write(f"**Dimensions :** {df.shape[0]} lignes × "
                 f"{df.shape[1]} colonnes")
