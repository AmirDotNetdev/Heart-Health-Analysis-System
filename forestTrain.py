
from pathlib import Path
import time

import numpy as np
import pandas as pd
import joblib

from sklearn.ensemble import (
    RandomForestClassifier,
    ExtraTreesClassifier,
    HistGradientBoostingClassifier
)

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    classification_report,
    confusion_matrix
)

from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_sample_weight


start_time = time.time()

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "cardio_train.csv"
MODEL_PATH = BASE_DIR / "cardio_model.joblib"

TARGET_RECALL = 0.95

df = pd.read_csv(DATA_PATH, sep=";")

df["age"] = df["age"] / 365.25
df["gender"] = df["gender"].map({1: 0, 2: 1})

df = df[
    (df["ap_hi"].between(60, 250)) &
    (df["ap_lo"].between(40, 200)) &
    (df["ap_hi"] >= df["ap_lo"]) &
    (df["height"].between(100, 250)) &
    (df["weight"].between(30, 200))
].copy()

df["bmi"] = df["weight"] / (df["height"] / 100) ** 2
df["pulse_pressure"] = df["ap_hi"] - df["ap_lo"]
df["mean_arterial_pressure"] = (
    df["ap_lo"] + df["pulse_pressure"] / 3
)
df["bp_ratio"] = df["ap_hi"] / df["ap_lo"]

X = df.drop(columns=["cardio", "id"])
y = df["cardio"]

X_train, X_temp, y_train, y_temp = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp,
    y_temp,
    test_size=0.50,
    random_state=42,
    stratify=y_temp
)

medians = X_train.median()

X_train = X_train.fillna(medians)
X_val = X_val.fillna(medians)
X_test = X_test.fillna(medians)

models = {
    "RandomForest": RandomForestClassifier(
        n_estimators=350,
        max_depth=None,
        min_samples_split=5,
        min_samples_leaf=2,
        max_features="sqrt",
        class_weight="balanced_subsample",
        random_state=42,
        n_jobs=-1
    ),

    "ExtraTrees": ExtraTreesClassifier(
        n_estimators=400,
        max_depth=None,
        min_samples_split=5,
        min_samples_leaf=2,
        max_features="sqrt",
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    ),

    "HistGradientBoosting": HistGradientBoostingClassifier(
        max_iter=300,
        learning_rate=0.06,
        max_leaf_nodes=31,
        min_samples_leaf=30,
        l2_regularization=1.0,
        early_stopping=True,
        random_state=42
    )
}

results = []

for name, model in models.items():

    print(f"\nTraining {name}...")

    model_start = time.time()

    if name == "HistGradientBoosting":
        weights = compute_sample_weight(
            class_weight="balanced",
            y=y_train
        )
        model.fit(
            X_train,
            y_train,
            sample_weight=weights
        )
    else:
        model.fit(X_train, y_train)

    probabilities = model.predict_proba(X_val)[:, 1]

    best_threshold = 0.0
    best_precision = -1
    best_recall = 0.0
    best_f1 = 0.0

    for threshold in np.linspace(0.0, 1.0, 501):

        predictions = (probabilities >= threshold).astype(int)

        precision = precision_score(
            y_val, predictions, zero_division=0
        )

        recall = recall_score(
            y_val, predictions, zero_division=0
        )

        f1 = f1_score(
            y_val, predictions, zero_division=0
        )

        if recall >= TARGET_RECALL:

            if (
                precision > best_precision or
                (
                    precision == best_precision and
                    recall > best_recall
                )
            ):
                best_threshold = threshold
                best_precision = precision
                best_recall = recall
                best_f1 = f1

    results.append({
        "name": name,
        "model": model,
        "threshold": best_threshold,
        "precision": best_precision,
        "recall": best_recall,
        "f1": best_f1
    })

    print(f"Validation Precision: {best_precision:.4f}")
    print(f"Validation Recall: {best_recall:.4f}")
    print(f"Validation F1: {best_f1:.4f}")
    print(f"Threshold: {best_threshold:.3f}")
    print(f"Training Time: {time.time() - model_start:.2f} seconds")


best_result = max(
    results,
    key=lambda x: (x["precision"], x["recall"], x["f1"])
)

best_model = best_result["model"]
best_threshold = best_result["threshold"]

print("\n========== FINAL MODEL ==========")
print("Selected Model:", best_result["name"])
print("Selected Threshold:", best_threshold)

test_probabilities = best_model.predict_proba(X_test)[:, 1]

test_predictions = (
    test_probabilities >= best_threshold
).astype(int)

print("\n========== TEST RESULTS ==========")

print("Accuracy:", round(
    accuracy_score(y_test, test_predictions), 4
))

print("Precision:", round(
    precision_score(y_test, test_predictions, zero_division=0), 4
))

print("Recall:", round(
    recall_score(y_test, test_predictions, zero_division=0), 4
))

print("F1 Score:", round(
    f1_score(y_test, test_predictions, zero_division=0), 4
))

print("ROC AUC:", round(
    roc_auc_score(y_test, test_probabilities), 4
))

print("Average Precision:", round(
    average_precision_score(y_test, test_probabilities), 4
))

print("\nClassification Report")
print(classification_report(y_test, test_predictions))

cm = confusion_matrix(y_test, test_predictions)

tn, fp, fn, tp = cm.ravel()

print("\nConfusion Matrix")
print(cm)

print("\nConfusion Matrix Details")
print("True Negative:", tn)
print("False Positive:", fp)
print("False Negative:", fn)
print("True Positive:", tp)

print(
    "Missed Sick Patients (%):",
    round(fn / (fn + tp) * 100, 2)
)

best_model.threshold_ = float(best_threshold)
best_model.feature_names_in_ = np.array(X.columns)

joblib.dump(best_model, MODEL_PATH)

print("\nModel Saved:", MODEL_PATH)
print("Total Execution Time:", round(time.time() - start_time, 2), "seconds")
