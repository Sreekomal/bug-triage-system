import os
import re
import string
import joblib


# ----------------------------
# 1. Model Artifact Paths & Loader
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "saved_models")

VECTORIZER_PATH = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
MODEL_PATH = os.path.join(MODEL_DIR, "linear_svm.pkl")
LABEL_ENCODER_PATH = os.path.join(MODEL_DIR, "label_encoder.pkl")


def load_artifacts():
    """
    Loads and returns the serialized inference artifacts:
    TF-IDF Vectorizer, Linear SVM Model, and Label Encoder.
    """
    if not os.path.exists(VECTORIZER_PATH):
        raise FileNotFoundError(f"TF-IDF vectorizer not found at: {VECTORIZER_PATH}")
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Trained model not found at: {MODEL_PATH}")
    if not os.path.exists(LABEL_ENCODER_PATH):
        raise FileNotFoundError(f"Label encoder not found at: {LABEL_ENCODER_PATH}")

    vectorizer = joblib.load(VECTORIZER_PATH)
    model = joblib.load(MODEL_PATH)
    label_encoder = joblib.load(LABEL_ENCODER_PATH)

    return vectorizer, model, label_encoder


# Load artifacts once at module load time for efficient inference
_vectorizer, _model, _label_encoder = load_artifacts()


# ----------------------------
# 2. Text Cleaning Function (Consistent with preprocessing.py)
# ----------------------------
def clean_text(text):
    """
    Cleans input text using the exact same steps as preprocessing.py:
    lowercase, remove punctuation, remove non-alphanumeric characters,
    and strip extra spaces.
    """
    text = str(text).lower()

    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Remove special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ----------------------------
# 3. Severity Prediction Function
# ----------------------------
def predict_severity(text):
    """
    Predicts the severity level for a given raw bug description string.

    Pipeline:
        raw text
           ↓
        text cleaning (clean_text)
           ↓
        saved TF-IDF vectorizer
           ↓
        saved Linear SVM model
           ↓
        saved label encoder
           ↓
        final severity label

    Parameters:
        text (str): Raw bug description string.

    Returns:
        str: Predicted severity label ('Critical', 'High', 'Medium', or 'Low').

    Raises:
        ValueError: If input is None, not a string, empty, or whitespace-only.
    """
    if text is None or not isinstance(text, str) or not text.strip():
        raise ValueError("A non-empty bug description string is required.")

    cleaned = clean_text(text)
    if not cleaned:
        raise ValueError("A non-empty bug description containing alphanumeric characters is required.")

    # 1. Feature extraction using fitted TF-IDF vectorizer
    features = _vectorizer.transform([cleaned])

    # 2. Model prediction (numerical class)
    encoded_pred = _model.predict(features)

    # 3. Inverse transform numerical class to severity name
    severity_label = _label_encoder.inverse_transform(encoded_pred)[0]

    return str(severity_label)


# ----------------------------
# 4. Main Verification Section
# ----------------------------
if __name__ == "__main__":
    print("=" * 70)
    print("SEVERITY PREDICTION PIPELINE VERIFICATION")
    print("=" * 70)

    sample_bugs = [
        "Application crashes when uploading a large file",
        "Typo in the login page error message",
        "Page takes a long time to load after clicking submit",
        "User cannot save changes to their profile",
    ]

    print("\nSample Bug Predictions:\n")
    for bug in sample_bugs:
        severity = predict_severity(bug)
        print(f"Bug: {bug}")
        print(f"Predicted Severity: {severity}\n")

    print("-" * 70)
    print("Testing input validation with invalid inputs:")
    test_invalid_inputs = [None, "", "   ", "???!!!"]
    for inv_input in test_invalid_inputs:
        try:
            predict_severity(inv_input)
            print(f"  Unexpected success for: {repr(inv_input)}")
        except ValueError as err:
            print(f"  Correctly caught ValueError for {repr(inv_input)}: {err}")

    print("=" * 70)
    print("Prediction pipeline verification completed successfully!")
    print("=" * 70)
