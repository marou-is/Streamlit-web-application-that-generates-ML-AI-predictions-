
import streamlit as st
from config import PAGE_CONFIG
from modules.styles       import inject
from modules.data_handler import DataHandler
from modules.model_manager import ModelManager
from modules.session_manager import SessionManager
from views.home_view          import HomeView
from views.data_view          import DataView
from views.preprocessing_view import PreprocessingView
from views.model_view         import ModelView

st.set_page_config(**PAGE_CONFIG)
inject()
SessionManager.init()

# Hero + upload gate
fichier, handler = HomeView.render_hero()
if handler is None:
    st.stop()

prep = SessionManager.load_preprocessor()
mgr  = SessionManager.get("model_manager") or ModelManager()

DataView.render_variables(handler)
DataView.render_dimensions(handler)
DataView.render_preview(handler)
DataView.render_missing(handler)
df_cleaned = DataView.render_cleaning(handler, prep)

if df_cleaned is None:
    st.stop()

df_encoded = PreprocessingView.render_encoding(df_cleaned, prep, handler.categorical_features)
df_norm    = PreprocessingView.render_normalisation(df_encoded, prep)
PreprocessingView.render_correlation(df_norm, SessionManager.get("enc_method"), SessionManager.get("enc_cols"))
df_final   = PreprocessingView.render_pca(df_norm, prep)
PreprocessingView.render_final(df_final)

ModelView.render_split(df_final, mgr)
ModelView.render_training(mgr)
ModelView.render_evaluation()
ModelView.render_prediction(handler, prep)
