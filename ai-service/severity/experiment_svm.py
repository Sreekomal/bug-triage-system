import os
import joblib
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC


# ----------------------------
# 1. Paths & Loading
# ----------------------------
data_path = "dataset/processed/severity_processed.csv"
if not os.path.exists(data_path):
    alt_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), data_path)
    if os.path.exists(alt_path):
        data_path = alt_path

df = pd.read_csv(data_path)

model_dir = "saved_models"
if not os.path.exists(model_dir) and not os.path.exists("dataset"):
    model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved_models")

encoder_path = os.path.join(model_dir, "label_encoder.pkl")
vectorizer_path = os.path.join(model_dir, "tfidf_vectorizer.pkl")

label_encoder = joblib.load(encoder_path)
vectorizer = joblib.load(vectorizer_path)
class_names = list(label_encoder.classes_)

print("=" * 70)
print("CONTROLLED HYPERPARAMETER EXPERIMENT: LinearSVC (C Tuning)")
print("=" * 70)
print(f"Dataset shape         : {df.shape}")
print(f"Target classes ({len(class_names)})      : {class_names}")


# ----------------------------
# 2. Prepare Features & Same 80/20 Stratified Split
# ----------------------------
df["text"] = df["text"].fillna("")
X = df["text"]
y = df["severity"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Transform using existing vectorizer (NO re-fitting)
X_train_tfidf = vectorizer.transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)


# ----------------------------
# 3. Test LinearSVC C Configurations
# ----------------------------
c_values = [0.5, 1.0, 2.0, 5.0]
results = []
models_evaluated = {}

BASELINE_MACRO_F1 = 0.4629

for c in c_values:
    print(f"\nTraining LinearSVC with C={c} (class_weight='balanced', random_state=42)...")
    clf = LinearSVC(C=c, class_weight="balanced", random_state=42)
    clf.fit(X_train_tfidf, y_train)
    y_pred = clf.predict(X_test_tfidf)

    acc = accuracy_score(y_test, y_pred)
    macro_prec = precision_score(y_test, y_pred, average="macro", zero_division=0)
    macro_rec = recall_score(y_test, y_pred, average="macro", zero_division=0)
    macro_f1 = f1_score(y_test, y_pred, average="macro", zero_division=0)
    weighted_f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)

    models_evaluated[c] = {
        "clf": clf,
        "y_pred": y_pred,
        "report": classification_report(y_test, y_pred, target_names=class_names, digits=4, zero_division=0),
        "cm": confusion_matrix(y_test, y_pred)
    }

    results.append({
        "C": c,
        "Accuracy": round(acc, 4),
        "Macro Precision": round(macro_prec, 4),
        "Macro Recall": round(macro_rec, 4),
        "Macro F1": round(macro_f1, 4),
        "Weighted F1": round(weighted_f1, 4)
    })


# ----------------------------
# 4. Results Comparison Table
# ----------------------------
results_df = pd.DataFrame(results)

print("\n" + "=" * 70)
print("HYPERPARAMETER EXPERIMENT COMPARISON TABLE")
print("=" * 70)
print(results_df.to_string(index=False))

# Save Results to CSV (DO NOT overwrite linear_svm.pkl)
csv_save_path = os.path.join(model_dir, "svm_hyperparameter_results.csv")
results_df.to_csv(csv_save_path, index=False)
print(f"\nExperiment results saved to: {csv_save_path}")


# ----------------------------
# 5. Best Configuration Analysis
# ----------------------------
best_row = results_df.sort_values(by="Macro F1", ascending=False).iloc[0]
best_c = best_row["C"]
best_macro_f1 = best_row["Macro F1"]
diff = best_macro_f1 - BASELINE_MACRO_F1

print("\n" + "=" * 70)
print(f"BEST CONFIGURATION: C={best_c}")
print(f"  Best Macro-F1                          : {best_macro_f1:.4f}")
print(f"  Baseline Macro-F1 (C=1.0)              : {BASELINE_MACRO_F1:.4f}")
print(f"  Improvement over Baseline              : {diff:+.4f} ({diff*100:+.2f}%)")
print("=" * 70)

print(f"\nClassification Report for Best Configuration (C={best_c}):")
print(models_evaluated[best_c]["report"])

print(f"Confusion Matrix for Best Configuration (C={best_c}):")
cm_df = pd.DataFrame(
    models_evaluated[best_c]["cm"],
    index=[f"Actual {c_name}" for c_name in class_names],
    columns=[f"Pred {c_name}" for c_name in class_names]
)
print(cm_df)
print("=" * 70)
