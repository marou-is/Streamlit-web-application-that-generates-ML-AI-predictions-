# ─────────────────────────────────────────────
# views/data_view.py  —  DataView class
# Renders steps 1–6: load, explore, clean
# ─────────────────────────────────────────────

import streamlit as st
import pandas as pd
from modules.data_handler import DataHandler
from modules.session_manager import SessionManager
from config import TARGET


def _sec(title): st.subheader(title)


class DataView:
    """UI for data loading and exploration (steps 1–6)."""

    # ── Step 1 — Upload gate (home page OR analysis) ─────────
    @staticmethod
    def render_upload_gate() -> "DataHandler | None":
        from views.home_view import HomeView

        fichier = st.file_uploader(
            "Importer le fichier « profitentr » (CSV) depuis votre PC",
            type=["csv"],
            label_visibility="collapsed",
        )

        if fichier is not None:
            handler = DataHandler(fichier)
            SessionManager.set("data_handler", handler)
            # Compact title for analysis pages
            st.markdown("""
            <div style="padding:1.4rem 0 .2rem">
              <p class="page-title">📈 <em>Analyse du Dataset</em></p>
            </div>
            """, unsafe_allow_html=True)
            st.divider()
            return handler

        # No file yet — show landing page
        HomeView.render()
        st.markdown("""
        <div style="margin:0 auto;max-width:520px;padding:.5rem 0 2rem">
        """, unsafe_allow_html=True)
        st.file_uploader(
            "Glissez votre fichier CSV ici ou cliquez pour parcourir",
            type=["csv"], key="_upload2",
            label_visibility="visible",
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # Check if second uploader was used
        if st.session_state.get("_upload2") is not None:
            handler = DataHandler(st.session_state["_upload2"])
            SessionManager.set("data_handler", handler)
            st.rerun()
        return None

    @staticmethod
    def render_upload() -> "DataHandler | None":
        return DataView.render_upload_gate()

    # ── Step 2 — Variables ────────────────────────────────────
    @staticmethod
    def render_variables(handler: DataHandler):
        _sec("2. 🏷️ Variables Indépendantes et Variable Cible")
        c1, c2 = st.columns(2)
        c1.info(f"**Variables indépendantes (X) :** "
                f"{', '.join(handler.feature_names)}")
        c2.success(f"**Variable cible (y) :** {TARGET}")

    # ── Step 3 — Dimensions ───────────────────────────────────
    @staticmethod
    def render_dimensions(handler: DataHandler):
        _sec("3. 📐 Nombre d'Instances et d'Attributs")
        c1, c2 = st.columns(2)
        c1.metric("Instances (lignes)",    handler.shape[0])
        c2.metric("Attributs (colonnes)",  handler.shape[1])

    # ── Step 4 — Preview ──────────────────────────────────────
    @staticmethod
    def render_preview(handler: DataHandler):
        _sec("4. 👁️ Premières Lignes du Jeu de Données")
        n = st.slider("Nombre de lignes à afficher", 3, 20, 5)
        st.dataframe(handler.head(n), use_container_width=True)

    # ── Step 5 — Missing values ───────────────────────────────
    @staticmethod
    def render_missing(handler: DataHandler):
        _sec("5. ❓ Analyse des Valeurs Manquantes")
        if handler.missing_columns:
            st.warning(f"**Colonnes avec valeurs manquantes :** "
                       f"{', '.join(handler.missing_columns)}")
            st.warning(f"**Nombre de lignes affectées :** "
                       f"{handler.missing_row_count}")
            st.dataframe(handler.missing_summary(), use_container_width=True)
        else:
            st.success("Aucune valeur manquante détectée.")

    # ── Step 6 — Cleaning ─────────────────────────────────────
    @staticmethod
    def render_cleaning(handler: DataHandler,
                        preprocessor) -> pd.DataFrame | None:
        _sec("6. 🧹 Nettoyage des Données")
        df_work = SessionManager.get("df_cleaned")

        if handler.missing_columns:
            method = st.selectbox("Méthode de remplacement :", [
                "Moyenne (Mean)", "Médiane (Median)", "Mode",
                "Remplacer par 0", "Supprimer les lignes incomplètes",
            ])
            if st.button("✅ Appliquer le Nettoyage"):
                df_work = preprocessor.clean(
                    handler.df, method, handler.numeric_features
                )
                SessionManager.set("df_cleaned", df_work)
                st.success(f"Nettoyage appliqué : **{method}**")
        else:
            if df_work is None:
                df_work = handler.df.copy()
                SessionManager.set("df_cleaned", df_work)
            st.success("Aucune valeur manquante — nettoyage non nécessaire.")

        if df_work is not None:
            st.write("**Aperçu après nettoyage :**")
            st.dataframe(df_work.head(), use_container_width=True)
            if df_work.isnull().sum().sum() == 0:
                st.success("✔ Aucune valeur manquante restante.")

        return df_work
