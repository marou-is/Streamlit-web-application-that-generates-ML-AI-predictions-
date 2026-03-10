# ─────────────────────────────────────────────
# modules/preprocessor.py  —  Preprocessor class
# Responsibilities:
#   • Clean missing values
#   • Encode categorical features
#   • Normalise numeric features
#   • Apply / store PCA
#   • Transform a single raw row (for prediction)
# ─────────────────────────────────────────────

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, LabelEncoder
from sklearn.decomposition import PCA
from config import TARGET


class Preprocessor:
    """Full data-preparation pipeline with state storage for inference."""

    def __init__(self):
        # ── Fitted artefacts (persisted in session state) ─────
        self.enc_method: str        = "Aucun"
        self.enc_cols:   list       = []
        self.enc_mp:     dict       = {}   # OHE dummy cols OR Binary int-map per column
        self.enc_le:     dict       = {}   # LabelEncoder per column

        self.scaler                 = None
        self.cols_to_nrm: list      = []

        self.pca_model              = None
        self.pca_cols:   list       = []

    # ══════════════════════════════════════════════════════════
    # 1. CLEANING
    # ══════════════════════════════════════════════════════════
    def clean(self, df: pd.DataFrame, method: str,
              numeric_cols: list) -> pd.DataFrame:
        """
        Fill / drop missing values.
        method: 'Moyenne (Mean)' | 'Médiane (Median)' | 'Mode' |
                'Remplacer par 0' | 'Supprimer les lignes incomplètes'
        """
        df = df.copy()
        if method == "Moyenne (Mean)":
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        elif method == "Médiane (Median)":
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        elif method == "Mode":
            for c in df.columns:
                df[c] = df[c].fillna(df[c].mode()[0])
        elif method == "Remplacer par 0":
            df[numeric_cols] = df[numeric_cols].fillna(0)
        elif method == "Supprimer les lignes incomplètes":
            df = df.dropna().reset_index(drop=True)
        return df

    # ══════════════════════════════════════════════════════════
    # 2. ENCODING
    # ══════════════════════════════════════════════════════════
    def encode(self, df: pd.DataFrame, method: str,
               cat_cols: list) -> pd.DataFrame:
        """
        Encode categorical columns and store artefacts for inference.
        method: 'One-Hot Encoding' | 'Binary Encoding' | 'Label Encoding'
        """
        df = df.copy()
        new_enc_cols = []
        mp_store     = {}
        le_store     = {}

        for col in cat_cols:
            if method == "One-Hot Encoding":
                dummies = pd.get_dummies(df[col], prefix=col).astype(int)
                mp_store[col] = dummies.columns.tolist()
                df = pd.concat([df.drop(columns=[col]), dummies], axis=1)
                new_enc_cols += mp_store[col]

            elif method == "Binary Encoding":
                uniq   = sorted(df[col].dropna().unique())
                mp     = {v: i for i, v in enumerate(uniq)}
                mp_store[col] = mp
                arr    = df[col].map(mp).fillna(0).astype(int).to_numpy()
                nb     = max(1, int(np.ceil(np.log2(len(uniq) + 1))))
                for b in range(nb):
                    nm = f"{col}_bit{b}"
                    df[nm] = ((arr >> b) & 1).astype(int)
                    new_enc_cols.append(nm)
                df = df.drop(columns=[col])

            elif method == "Label Encoding":
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str)) + 1
                le_store[col] = le
                new_enc_cols.append(col)

        # Store artefacts
        self.enc_method = method
        self.enc_cols   = new_enc_cols
        self.enc_mp     = mp_store
        self.enc_le     = le_store
        return df

    # ══════════════════════════════════════════════════════════
    # 3. NORMALISATION
    # ══════════════════════════════════════════════════════════
    def normalise(self, df: pd.DataFrame, method: str) -> pd.DataFrame:
        """
        Fit-transform numeric (non-dummy) columns.
        method: 'Aucune normalisation' | 'Min-Max Scaling (0-1)' |
                'Standardisation Z-score' | 'Robust Scaling'
        """
        df = df.copy()
        cols_X = [c for c in df.columns if c != TARGET]

        # Exclude dummy/binary cols from scaling
        if self.enc_method in ("One-Hot Encoding", "Binary Encoding"):
            cols_to_nrm = [c for c in cols_X if c not in self.enc_cols]
        else:
            cols_to_nrm = cols_X

        # Always exclude any remaining non-numeric columns
        cols_to_nrm = [c for c in cols_to_nrm
                       if pd.api.types.is_numeric_dtype(df[c])]

        scaler_map = {
            "Min-Max Scaling (0-1)":    MinMaxScaler(),
            "Standardisation Z-score":  StandardScaler(),
            "Robust Scaling":           RobustScaler(),
        }
        scaler = None
        for key in scaler_map:
            if key in method:
                scaler = scaler_map[key]
                break

        if scaler and cols_to_nrm:
            df[cols_to_nrm] = scaler.fit_transform(df[cols_to_nrm])

        self.scaler       = scaler
        self.cols_to_nrm  = cols_to_nrm
        return df

    # ══════════════════════════════════════════════════════════
    # 4. PCA
    # ══════════════════════════════════════════════════════════
    def apply_pca(self, df: pd.DataFrame, n_components: int) -> pd.DataFrame:
        """
        Fit PCA on numeric columns (excluding target) and return
        a DataFrame of principal components + target.
        """
        cols_X = [c for c in df.columns
                  if c != TARGET and pd.api.types.is_numeric_dtype(df[c])]
        X_in   = df[cols_X].apply(pd.to_numeric, errors="coerce").fillna(0)

        pca    = PCA(n_components=n_components)
        X_pca  = pca.fit_transform(X_in)

        self.pca_model = pca
        self.pca_cols  = cols_X

        col_names = [f"CP{i+1}" for i in range(n_components)]
        df_pca    = pd.DataFrame(X_pca, columns=col_names)
        df_pca[TARGET] = df[TARGET].values
        return df_pca, pca.explained_variance_ratio_

    # ══════════════════════════════════════════════════════════
    # 5. INFERENCE TRANSFORM  (single raw row → model-ready row)
    # ══════════════════════════════════════════════════════════
    def transform_input(self, raw: dict,
                        orig_cat_cols: list,
                        train_cols: list) -> pd.DataFrame:
        """
        Apply the stored pipeline to a single raw dict of user inputs.
        Returns a 1-row DataFrame aligned to train_cols.
        """
        row = pd.DataFrame([raw])

        # ── Encoding ─────────────────────────────────────────
        for col in orig_cat_cols:
            if self.enc_method == "One-Hot Encoding":
                dummy_cols = self.enc_mp.get(col, [])
                for dc in dummy_cols:
                    cat_val = dc.replace(f"{col}_", "", 1)
                    row[dc] = int(str(raw[col]) == cat_val)
                row = row.drop(columns=[col])

            elif self.enc_method == "Binary Encoding":
                mp_col  = self.enc_mp.get(col, {})
                int_val = int(mp_col.get(raw[col], 0))
                nb      = max(1, int(np.ceil(np.log2(len(mp_col) + 1))))
                for b in range(nb):
                    row[f"{col}_bit{b}"] = int((int_val >> b) & 1)
                row = row.drop(columns=[col])

            elif self.enc_method == "Label Encoding":
                le_col = self.enc_le.get(col)
                if le_col:
                    val = raw[col]
                    row[col] = (int(le_col.transform([val])[0]) + 1
                                if val in le_col.classes_ else 1)

        # ── Normalisation ─────────────────────────────────────
        if self.scaler and self.cols_to_nrm:
            existing = [c for c in self.cols_to_nrm if c in row.columns]
            row[existing] = self.scaler.transform(row[existing])

        # ── PCA ───────────────────────────────────────────────
        if self.pca_model is not None:
            existing_pca = [c for c in self.pca_cols if c in row.columns]
            pca_arr = self.pca_model.transform(row[existing_pca])
            row = pd.DataFrame(
                pca_arr,
                columns=[f"CP{i+1}" for i in range(pca_arr.shape[1])]
            )

        # ── Align to training columns ─────────────────────────
        for c in train_cols:
            if c not in row.columns:
                row[c] = 0
        return row[train_cols]
