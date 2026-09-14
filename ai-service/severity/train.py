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
# 1. Path Setup & Dataset Loading
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
os.makedirs(model_dir, exist_ok=True)

# Load Label Encoder
encoder_path = os.path.join(model_dir, "label_encoder.pkl")
if not os.path.exists(encoder_path):
    raise FileNotFoundError(f"Label encoder not found at: {encoder_path}")
label_encoder = joblib.load(encoder_path)
class_names = list(label_encoder.classes_)

print("=" * 70)
print("SEVERITY PREDICTION - FINAL MODEL TRAINING (LinearSVC C=0.5)")
print("=" * 70)
print(f"Dataset shape                : {df.shape}")
print(f"Target classes ({len(class_names)})             : {class_names}")


# ----------------------------
# 2. Handle Unexpected Nulls & Prepare Features
# ----------------------------
null_count = df["text"].isnull().sum()
if null_count > 0:
    print(f"Handling null values         : Found {null_count} nulls in 'text', filled with empty string")
df["text"] = df["text"].fillna("")

X = df["text"]
y = df["severity"]


# ----------------------------
# 3. Stratified Train/Test Split (80/20)
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"Train samples count          : {len(X_train)} (80%)")
print(f"Test samples count           : {len(X_test)} (20%)")


# ----------------------------
# 4. Load Saved TF-IDF Vectorizer & Transform
# ----------------------------
vectorizer_path = os.path.join(model_dir, "tfidf_vectorizer.pkl")
if not os.path.exists(vectorizer_path):
    raise FileNotFoundError(f"TF-IDF vectorizer not found at: {vectorizer_path}")

vectorizer = joblib.load(vectorizer_path)
print(f"Loaded TF-IDF features       : {len(vectorizer.get_feature_names_out())}")

X_train_tfidf = vectorizer.transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)
print(f"X_train_tfidf matrix shape   : {X_train_tfidf.shape}")
print(f"X_test_tfidf matrix shape    : {X_test_tfidf.shape}")


# ----------------------------
# 5. Train Final Selected LinearSVC Model (C=0.5)
# ----------------------------
print("\n" + "-" * 70)
print("Training Final LinearSVC Model (C=0.5, class_weight='balanced', random_state=42)...")
print("-" * 70)

final_model = LinearSVC(
    C=0.5,
    class_weight="balanced",
    random_state=42
)
final_model.fit(X_train_tfidf, y_train)

# Evaluate on test set
y_pred = final_model.predict(X_test_tfidf)

acc = accuracy_score(y_test, y_pred)
macro_prec = precision_score(y_test, y_pred, average="macro", zero_division=0)
macro_rec = recall_score(y_test, y_pred, average="macro", zero_division=0)
macro_f1 = f1_score(y_test, y_pred, average="macro", zero_division=0)
weighted_f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)

print(f"Accuracy           : {acc:.4f}")
print(f"Macro Precision    : {macro_prec:.4f}")
print(f"Macro Recall       : {macro_rec:.4f}")
print(f"Macro F1 (Primary) : {macro_f1:.4f}")
print(f"Weighted F1        : {weighted_f1:.4f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=class_names, digits=4, zero_division=0))

print("Confusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
cm_df = pd.DataFrame(cm, index=[f"Actual {c}" for c in class_names], columns=[f"Pred {c}" for c in class_names])
print(cm_df)


# ----------------------------
# 6. Save Final Trained Model
# ----------------------------
model_save_path = os.path.join(model_dir, "linear_svm.pkl")
joblib.dump(final_model, model_save_path)
print(f"\nFinal LinearSVC (C=0.5) model successfully saved to: {model_save_path}")
print("=" * 70)
