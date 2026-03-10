# ─────────────────────────────────────────────
# config.py  —  Global constants & session state
# ─────────────────────────────────────────────

TARGET = "Profit"

PAGE_CONFIG = dict(
    page_title = "Prédiction de Profit",
    layout     = "wide",
    page_icon  = "📈",
)

SESSION_DEFAULTS = dict(
    df_cleaned            = None,
    df_encoded            = None,
    df_norm               = None,
    df_final              = None,
    enc_method            = "Aucun",
    enc_cols              = [],
    model                 = None,
    X_test                = None,
    y_test                = None,
    feature_names         = [],
    pipeline_scaler       = None,
    pipeline_cols_to_nrm  = [],
    pipeline_enc_method   = "Aucun",
    pipeline_enc_cols     = [],
    pipeline_mp           = {},
    pipeline_le           = {},
    pipeline_pca          = None,
    pipeline_pca_cols     = [],
)

PIPELINE_STEPS = [
    ("📂", "Chargement du fichier CSV",  "Importez votre dataset CSV"),
    ("🏷️", "Variables X et cible",       "Identification des features"),
    ("📐", "Dimensions",                  "Lignes et colonnes du dataset"),
    ("👁️", "Premières lignes",            "Aperçu rapide des données"),
    ("❓", "Valeurs manquantes",          "Détection des données absentes"),
    ("🧹", "Nettoyage",                   "Imputation ou suppression"),
    ("🔤", "Encodage",                    "OHE / Binary / Label"),
    ("📏", "Normalisation",               "Min-Max · Z-score · Robust"),
    ("🔗", "Corrélation",                 "Matrice de corrélation"),
    ("🔬", "Réduction PCA",               "Réduction de dimensionnalité"),
    ("✅", "Données préparées",           "Jeu de données final"),
    ("✂️", "Séparation Train/Test",       "Split configurable"),
    ("🏋️", "Entraînement",               "Régression Linéaire Multiple"),
    ("🧪", "Test & Métriques",            "MAE · MSE · RMSE · R²"),
    ("🔮", "Prédiction",                  "Prédire un nouveau profit"),
]
