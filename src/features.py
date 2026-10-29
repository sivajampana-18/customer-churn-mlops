from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUMERIC = ["tenure", "monthly_charges", "total_charges", "senior_citizen"]
CATEGORICAL = ["contract", "internet_service", "tech_support", "online_security",
               "payment_method", "paperless_billing", "partner", "dependents"]
FEATURES = NUMERIC + CATEGORICAL

def build_preprocessor():
    numeric_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])
    category_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])
    return ColumnTransformer([
        ("numeric", numeric_pipe, NUMERIC),
        ("categorical", category_pipe, CATEGORICAL)
    ])
