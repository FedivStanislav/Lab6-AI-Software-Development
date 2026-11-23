
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

RANDOM_STATE = 42
rng = np.random.default_rng(RANDOM_STATE)

# Generate synthetic software module metrics
n_samples = 500

data = pd.DataFrame({
    "lines_of_code": rng.integers(30, 1000, n_samples),
    "complexity": rng.integers(1, 35, n_samples),
    "code_changes": rng.integers(0, 30, n_samples),
    "previous_bugs": rng.integers(0, 12, n_samples)
})

# Synthetic defect risk model used to generate labels
risk_score = (
    0.002 * data["lines_of_code"]
    + 0.10 * data["complexity"]
    + 0.08 * data["code_changes"]
    + 0.20 * data["previous_bugs"]
    + rng.normal(0, 0.8, n_samples)
)

data["has_defect"] = (risk_score > 4.8).astype(int)

features = [
    "lines_of_code",
    "complexity",
    "code_changes",
    "previous_bugs"
]

X = data[features]
y = data["has_defect"]

# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=RANDOM_STATE,
    stratify=y
)

# Train Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=RANDOM_STATE
)

model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)

print("=== ML Defect Risk Prediction ===")
print(f"Dataset size: {len(data)}")
print(f"Training samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")
print(f"Accuracy: {accuracy_score(y_test, predictions):.2%}")

print("\nClassification Report:")
print(classification_report(y_test, predictions))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

# Feature importance analysis
importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
}).sort_values("Importance", ascending=False)

print("\nFeature Importance:")
print(importance.to_string(index=False))

# Predict defect risk for a new module
new_module = pd.DataFrame([{
    "lines_of_code": 850,
    "complexity": 28,
    "code_changes": 24,
    "previous_bugs": 8
}])

risk_probability = model.predict_proba(new_module)[0][1]

print("\n=== New Module Prediction ===")
print(f"Defect risk probability: {risk_probability:.2%}")
print(
    "Risk level:",
    "HIGH" if risk_probability >= 0.5 else "LOW"
)
