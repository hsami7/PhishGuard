import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

def train():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Load original spam_ham_dataset
    dataset_path = os.path.join(current_dir, "..", "data", "spam_ham_dataset.csv")
    print(f"Loading original dataset from: {dataset_path}")
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset not found at {dataset_path}")
    df = pd.read_csv(dataset_path)
    df = df.dropna(subset=["text", "label_num"])
    X_orig = df["text"].tolist()
    y_orig = df["label_num"].astype(int).tolist()
    print(f"Loaded {len(X_orig)} original records.")

    # 2. Load phishing_validation_emails dataset
    val_dataset_path = os.path.join(current_dir, "..", "data", "Phishing_validation_emails.csv")
    print(f"Loading validation dataset from: {val_dataset_path}")
    if not os.path.exists(val_dataset_path):
        raise FileNotFoundError(f"Dataset not found at {val_dataset_path}")
    df_val = pd.read_csv(val_dataset_path)
    df_val = df_val.dropna(subset=["Email Text", "Email Type"])
    X_val = df_val["Email Text"].tolist()
    
    # Map 'Safe Email' -> 0, 'Phishing Email' -> 1
    label_map = {"Safe Email": 0, "Phishing Email": 1}
    y_val = df_val["Email Type"].map(label_map).astype(int).tolist()
    print(f"Loaded {len(X_val)} validation records.")

    # Combine datasets
    X = X_orig + X_val
    y = np.array(y_orig + y_val)
    print(f"Combined dataset: Total records = {len(X)}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"Training set size: {len(X_train)}, Test set size: {len(X_test)}")
    
    # Vectorize text
    print("Vectorizing text using TF-IDF...")
    vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # Train Logistic Regression Model
    print("Training Logistic Regression model...")
    model = LogisticRegression(max_iter=1000, C=1.0, random_state=42)
    model.fit(X_train_vec, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test_vec)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save vectorizer and model
    model_path = os.path.join(current_dir, "email_classifier.pkl")
    vectorizer_path = os.path.join(current_dir, "vectorizer.pkl")
    
    print(f"Saving model to {model_path}...")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
        
    print(f"Saving vectorizer to {vectorizer_path}...")
    with open(vectorizer_path, "wb") as f:
        pickle.dump(vectorizer, f)
        
    print("Training and serialization completed successfully!")

if __name__ == "__main__":
    train()
