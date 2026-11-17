
import pandas as pd
import joblib

from ucimlrepo import fetch_ucirepo
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# 1. دریافت دیتاست رسمی UCI
dataset = fetch_ucirepo(id=45)

X = dataset.data.features.copy()
y = dataset.data.targets.iloc[:, 0]

# 2. تبدیل هدف به دو کلاس:
# 0 = نبود بیماری در برچسب دیتاست
# 1 = وجود بیماری در برچسب دیتاست
y = (pd.to_numeric(y, errors="coerce") > 0).astype(int)

# 3. تعیین ویژگی‌های عددی و دسته‌ای
categorical = [
    "sex", "cp", "fbs", "restecg",
    "exang", "slope", "ca", "thal"
]
numeric = [
    "age", "trestbps", "chol",
    "thalach", "oldpeak"
]

# بررسی ساختار دیتاست
X = X[numeric + categorical]

# 4. آماده‌سازی داده‌ها
numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("numeric", numeric_pipeline, numeric),
    ("categorical", categorical_pipeline, categorical)
])

# 5. ساخت مدل
model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(max_iter=2000))
])

# 6. تقسیم داده‌ها
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 7. آموزش
model.fit(X_train, y_train)

# 8. ارزیابی
predictions = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, predictions))
print(classification_report(
    y_test, predictions, zero_division=0
))
print("Confusion matrix:")
print(confusion_matrix(y_test, predictions))

# 9. ذخیره مدل
joblib.dump(model, "heart_model.joblib")

print("Model saved: heart_model.joblib")
