import pandas as pd
import numpy as np
import pickle
import os
import json
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

    # 4. Load newly downloaded Phishing_Email.csv dataset (large dataset)
    phish_email_path = os.path.join(current_dir, "..", "data", "Phishing_Email.csv")
    X_phish = []
    y_phish = []
    if os.path.exists(phish_email_path):
        print(f"Loading large Phishing Email dataset from: {phish_email_path}")
        df_phish = pd.read_csv(phish_email_path)
        df_phish = df_phish.dropna(subset=["Email Text", "Email Type"])
        X_phish = df_phish["Email Text"].tolist()
        y_phish = df_phish["Email Type"].map(label_map).astype(int).tolist()
        print(f"Loaded {len(X_phish)} records from Phishing Email dataset.")

    # 5. Load Kaggle emails directory (newly downloaded)
    kaggle_dir = os.path.join(current_dir, "..", "data", "kaggle_emails")
    X_kaggle = []
    y_kaggle = []
    if os.path.exists(kaggle_dir):
        print(f"Loading Kaggle email datasets from: {kaggle_dir}")
        for filename in sorted(os.listdir(kaggle_dir)):
            if filename.endswith(".csv"):
                file_path = os.path.join(kaggle_dir, filename)
                try:
                    df_k = pd.read_csv(file_path)
                    cols = list(df_k.columns)
                    text_col = None
                    label_col = None
                    for c in cols:
                        if c.lower() in ["text_combined", "text", "body", "email text"]:
                            text_col = c
                        if c.lower() in ["label", "email type", "type", "status"]:
                            label_col = c
                    
                    if text_col and label_col:
                        df_k = df_k.dropna(subset=[text_col, label_col])
                        texts = df_k[text_col].tolist()
                        labels = df_k[label_col].tolist()
                        mapped_labels = []
                        for val in labels:
                            if val in [0, 1, "0", "1"]:
                                mapped_labels.append(int(val))
                            elif str(val).lower() in ["safe email", "ham", "legitimate"]:
                                mapped_labels.append(0)
                            elif str(val).lower() in ["phishing email", "spam", "phishing"]:
                                mapped_labels.append(1)
                            else:
                                mapped_labels.append(None)
                                
                        valid_x = []
                        valid_y = []
                        for txt, lbl in zip(texts, mapped_labels):
                            if lbl is not None:
                                valid_x.append(txt)
                                valid_y.append(lbl)
                                
                        X_kaggle.extend(valid_x)
                        y_kaggle.extend(valid_y)
                        print(f"  Loaded {len(valid_x)} records from {filename}.")
                except Exception as e:
                    print(f"  Failed to load {filename}: {e}")

    # 6. Load Hugging Face texts.json (repaired JSON parsing)
    hf_path = os.path.join(current_dir, "..", "data", "texts.json")
    X_hf = []
    y_hf = []
    if os.path.exists(hf_path):
        print(f"Loading Hugging Face dataset from: {hf_path}")
        with open(hf_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        last_brace = content.rfind('}')
        if last_brace != -1:
            valid_json = content[:last_brace+1] + '\n]'
            try:
                data = json.loads(valid_json)
                for item in data:
                    if "text" in item and "label" in item:
                        X_hf.append(item["text"])
                        y_hf.append(int(item["label"]))
                print(f"Loaded {len(X_hf)} records from Hugging Face dataset.")
            except Exception as e:
                print(f"Failed to parse Hugging Face dataset: {e}")

    # Combine datasets
    X = X_orig + X_val + X_phish + X_kaggle + X_hf
    y = np.array(y_orig + y_val + y_phish + y_kaggle + y_hf)
    print(f"Combined dataset: Total records = {len(X)}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"Training set size: {len(X_train)}, Test set size: {len(X_test)}")
    
    # Vectorize text
    print("Vectorizing text using TF-IDF...")
    vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # Train Logistic Regression Model with L1 Regularization (Lasso)
    # L1 penalty performs feature selection by driving weights of irrelevant features to 0.
    print("Training Logistic Regression model with L1 feature selection...")
    model = LogisticRegression(max_iter=1000, C=1.0, penalty="l1", solver="liblinear", random_state=42)
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
