# ─────────────────────────────────────────────
# modules/session_manager.py  —  SessionManager
# Responsibilities:
#   • Initialise Streamlit session state
#   • Persist / restore DataHandler, Preprocessor,
#     ModelManager objects across reruns
# ─────────────────────────────────────────────

import streamlit as st
from config import SESSION_DEFAULTS


class SessionManager:
    """Thin wrapper around st.session_state for typed access."""

    @staticmethod
    def init():
        for k, v in SESSION_DEFAULTS.items():
            if k not in st.session_state:
                st.session_state[k] = v
        # Object slots for the three main classes
        for k in ("data_handler", "preprocessor", "model_manager"):
            if k not in st.session_state:
                st.session_state[k] = None

    # ── Generic get / set ─────────────────────────────────────
    @staticmethod
    def get(key, default=None):
        return st.session_state.get(key, default)

    @staticmethod
    def set(key, value):
        st.session_state[key] = value

    # ── Typed shortcuts ───────────────────────────────────────
    @staticmethod
    def save_preprocessor(prep):
        """Persist a fitted Preprocessor and its artefacts."""
        st.session_state.preprocessor         = prep
        st.session_state.pipeline_enc_method  = prep.enc_method
        st.session_state.pipeline_enc_cols    = prep.enc_cols
        st.session_state.pipeline_mp          = prep.enc_mp
        st.session_state.pipeline_le          = prep.enc_le
        st.session_state.pipeline_scaler      = prep.scaler
        st.session_state.pipeline_cols_to_nrm = prep.cols_to_nrm
        st.session_state.pipeline_pca         = prep.pca_model
        st.session_state.pipeline_pca_cols    = prep.pca_cols

    @staticmethod
    def load_preprocessor():
        """Restore a Preprocessor from session state."""
        from modules.preprocessor import Preprocessor
        prep = st.session_state.get("preprocessor")
        if prep is None:
            prep = Preprocessor()
            prep.enc_method  = st.session_state.pipeline_enc_method
            prep.enc_cols    = st.session_state.pipeline_enc_cols
            prep.enc_mp      = st.session_state.pipeline_mp
            prep.enc_le      = st.session_state.pipeline_le
            prep.scaler      = st.session_state.pipeline_scaler
            prep.cols_to_nrm = st.session_state.pipeline_cols_to_nrm
            prep.pca_model   = st.session_state.pipeline_pca
            prep.pca_cols    = st.session_state.pipeline_pca_cols
        return prep

    @staticmethod
    def save_model(mgr):
        st.session_state.model_manager = mgr
        st.session_state.model         = mgr.model
        st.session_state.X_test        = mgr.X_test
        st.session_state.y_test        = mgr.y_test
        st.session_state.feature_names = mgr.feature_names
