import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

def train_model():
    df = pd.read_csv("students_clean.csv")

    X = df[["math", "reading", "writing"]]
    y = df["pass_fail"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LogisticRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    print(classification_report(y_test, predictions))

    joblib.dump(model, "model.pkl")
    print("Model saved as model.pkl ✅")

def predict_result(math, reading, writing):
    model = joblib.load("model.pkl")
    input_data = np.array([[math, reading, writing]])
    prediction = model.predict(input_data)[0]
    confidence = model.predict_proba(input_data)[0][prediction] * 100
    return prediction, round(confidence, 2)

if __name__ == "__main__":
    train_model()
    result, conf = predict_result(75, 80, 70)
    print(f"\nTest Prediction: {'Pass ✅' if result == 1 else 'Fail ❌'} ({conf}% confidence)")