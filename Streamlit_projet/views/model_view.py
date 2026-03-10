
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from modules.model_manager  import ModelManager
from modules.visualizer     import Visualizer
from modules.session_manager import SessionManager
from config import TARGET

def _sec(title): st.subheader(title)

class ModelView:

    @staticmethod
    def render_split(df, mgr):
        _sec("12. ✂️ Séparation Entraînement / Test")
        pct_train = st.slider("Pourcentage d'entraînement (%)", 50, 90, 80)
        pct_test  = 100 - pct_train
        c1, c2 = st.columns(2)
        c1.info(f"🏋️ Entraînement : **{pct_train}%**")
        c2.info(f"🧪 Test : **{pct_test}%**")
        mgr.split(df, test_pct=pct_test / 100)
        st.write(f"Entraînement : **{len(mgr.X_train)}** échantillons | Test : **{len(mgr.X_test)}** échantillons")

    @staticmethod
    def render_training(mgr):
        _sec("13. 🏋️ Entraînement du Modèle de Régression Linéaire Multiple")
        if st.button("🚀 Lancer l'Entraînement"):
            mgr.train()
            SessionManager.save_model(mgr)
            st.success("✔ Modèle entraîné avec succès !")
            st.write(f"**Intercept :** {mgr.intercept:,.4f}")
            df_coef = mgr.coefficients
            st.dataframe(df_coef, use_container_width=True)
            st.pyplot(Visualizer.coefficients(df_coef))

    @staticmethod
    def render_evaluation():
        _sec("14. 🧪 Test du Modèle & Métriques d'Évaluation")
        if st.button("📋 Tester le Modèle"):
            model = SessionManager.get("model")
            if model is None:
                st.error("⚠️ Entraînez d'abord le modèle (étape 13).")
                return
            X_test = SessionManager.get("X_test")
            y_test = SessionManager.get("y_test")
            y_pred = model.predict(X_test)
            mae  = mean_absolute_error(y_test, y_pred)
            mse  = mean_squared_error(y_test, y_pred)
            rmse = float(np.sqrt(mse))
            r2   = r2_score(y_test, y_pred)

            st.subheader("📊 Métriques")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("MAE",  f"{mae:,.2f}")
            m2.metric("MSE",  f"{mse:,.2f}")
            m3.metric("RMSE", f"{rmse:,.2f}")
            m4.metric("R²",   f"{r2:.4f}")

            if   r2 >= 0.9: st.success(f"🎯 Excellent modèle — R² = {r2:.4f}")
            elif r2 >= 0.7: st.info(   f"👍 Bon modèle — R² = {r2:.4f}")
            else:           st.warning(f"⚠️ Modèle à améliorer — R² = {r2:.4f}")

            st.pyplot(Visualizer.real_vs_predicted(y_test, y_pred))
            st.pyplot(Visualizer.scatter(y_test, y_pred))

    @staticmethod
    def render_prediction(handler, prep):
        _sec("15. 🔮 Prédiction sur de Nouvelles Données")
        model = SessionManager.get("model")
        if model is None:
            st.info("⚙️ Entraînez d'abord le modèle (étape 13).")
            return

        st.write("Entrez les valeurs **originales** — l'application applique automatiquement l'encodage, la normalisation et la réduction :")

        saisie = {}
        num_cols = handler.numeric_features
        if num_cols:
            cols_ui = st.columns(min(len(num_cols), 3))
            for i, col in enumerate(num_cols):
                with cols_ui[i % len(cols_ui)]:
                    saisie[col] = st.number_input(col, value=handler.median(col), format="%.2f", key=f"pred_{col}")

        cat_cols = handler.categorical_features
        if cat_cols:
            cat_ui = st.columns(len(cat_cols))
            for i, col in enumerate(cat_cols):
                with cat_ui[i]:
                    saisie[col] = st.selectbox(col, handler.category_values(col), key=f"pred_cat_{col}")

        if st.button("🎯 Prédire le Profit"):
            try:
                train_cols = SessionManager.get("feature_names")
                row  = prep.transform_input(saisie, cat_cols, train_cols)
                pred = model.predict(row)[0]
                st.success(f"💰 **Profit prédit : {pred:,.2f} $**")
            except Exception as e:
                st.error(f"Erreur lors de la prédiction : {e}")
