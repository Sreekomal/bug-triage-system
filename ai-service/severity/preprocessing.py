import os
import re
import string
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder


# ----------------------------
# 1. Load Dataset
# ----------------------------
data_path = "dataset/raw/filtered_data.csv"
if not os.path.exists(data_path):
    alt_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), data_path)
    if os.path.exists(alt_path):
        data_path = alt_path

df = pd.read_csv(data_path)


# ----------------------------
# 2. Keep Required Columns & Rename
# ----------------------------
df = df[["Short Description", "Severity Label"]]
df.columns = ["text", "severity"]


# ----------------------------
# 3. Text Cleaning Function
# ----------------------------
def clean_text(text):
    text = str(text).lower()

    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Remove special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# Apply cleaning
df["text"] = df["text"].apply(clean_text)


# ----------------------------
# 4. Map Bugzilla Severity Labels to 4 Application Classes
# ----------------------------
label_mapping = {
    "blocker": "Critical",
    "critical": "Critical",
    "major": "High",
    "normal": "Medium",
    "minor": "Low",
    "trivial": "Low",
}

df["severity"] = df["severity"].str.lower().str.strip().map(label_mapping)

# Check for unmapped labels
unmapped_count = df["severity"].isnull().sum()
if unmapped_count > 0:
    raise ValueError(f"Found {unmapped_count} unmapped severity label(s)!")

# Record raw class distribution before numerical encoding
class_distribution_raw = df["severity"].value_counts()


# ----------------------------
# 5. Encode Severity Labels (4 Application Classes)
# ----------------------------
label_encoder = LabelEncoder()
df["severity"] = label_encoder.fit_transform(df["severity"])


# ----------------------------
# 6. Create Output Folders
# ----------------------------
output_dir = "dataset/processed"
model_dir = "saved_models"
if not os.path.exists(output_dir) and not os.path.exists("dataset"):
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset", "processed")
    model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved_models")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(model_dir, exist_ok=True)


# ----------------------------
# 7. Save Processed Dataset
# ----------------------------
processed_csv_path = os.path.join(output_dir, "severity_processed.csv")
df.to_csv(processed_csv_path, index=False)


# ----------------------------
# 8. Save Label Encoder
# ----------------------------
encoder_path = os.path.join(model_dir, "label_encoder.pkl")
joblib.dump(label_encoder, encoder_path)


# ----------------------------
# 9. Display Information & Verification
# ----------------------------
print("=" * 60)
print("Severity Preprocessing Completed Successfully!")
print("=" * 60)
print(f"Final Dataset Shape: {df.shape}")
print(f"Number of Classes: {len(label_encoder.classes_)}")

print("\n4 Application Classes:")
for index, label in enumerate(label_encoder.classes_):
    print(f"  [{index}] {label}")

print("\nClass Distribution (Count & Percentage):")
for label in label_encoder.classes_:
    count = class_distribution_raw[label]
    pct = (count / len(df)) * 100
    encoded_val = label_encoder.transform([label])[0]
    print(f"  {label:<10} (encoded: {encoded_val}): {count:>6} samples ({pct:>5.2f}%)")

print("\nProcessed Dataset Preview:")
print(df.head())

print(f"\nProcessed dataset saved to : {processed_csv_path}")
print(f"Label encoder saved to     : {encoder_path}")
print("=" * 60)