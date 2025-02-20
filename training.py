# Part 1: Training & Saving the Models
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mode
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from scipy import stats
import joblib
import pickle

# Reading the training data (dropping the last empty column)
DATA_PATH = "dataset/Training.csv"
data = pd.read_csv(DATA_PATH).dropna(axis=1)

# Checking if the dataset is balanced
disease_counts = data["prognosis"].value_counts()
temp_df = pd.DataFrame({
    "Disease": disease_counts.index,
    "Counts": disease_counts.values
})

plt.figure(figsize=(18,8))
sns.barplot(x="Disease", y="Counts", data=temp_df)
plt.xticks(rotation=90)
plt.show()

# Encoding the target variable
encoder = LabelEncoder()
data["prognosis"] = encoder.fit_transform(data["prognosis"])
classes = encoder.classes_

# Splitting features (X) and target (y)
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# Splitting into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=24
)

print(f"Train: {X_train.shape}, {y_train.shape}")
print(f"Test: {X_test.shape}, {y_test.shape}")
print(f"Unique diseases: {len(y.unique())}")

# Initializing and training the models
svm_model = SVC()
nb_model = GaussianNB()
rf_model = RandomForestClassifier(random_state=18)

svm_model.fit(X_train, y_train)
nb_model.fit(X_train, y_train)
rf_model.fit(X_train, y_train)

# Optional: Evaluating models on the test data
preds_svm = svm_model.predict(X_test)
preds_nb = nb_model.predict(X_test)
preds_rf = rf_model.predict(X_test)

print("SVM Test Accuracy:", accuracy_score(y_test, preds_svm))
print("Naive Bayes Test Accuracy:", accuracy_score(y_test, preds_nb))
print("Random Forest Test Accuracy:", accuracy_score(y_test, preds_rf))

# Training final models on the entire dataset
final_svm_model = SVC()
final_nb_model = GaussianNB()
final_rf_model = RandomForestClassifier(random_state=18)

final_svm_model.fit(X, y)
final_nb_model.fit(X, y)
final_rf_model.fit(X, y)

# Saving the models and the LabelEncoder
joblib.dump(final_svm_model, "final_svm_model.pkl")
joblib.dump(final_nb_model, "final_nb_model.pkl")
joblib.dump(final_rf_model, "final_rf_model.pkl")
joblib.dump(encoder, "label_encoder.pkl")

# Creating the symptom-index dictionary
symptoms = X.columns.values
symptom_index = {}
for index, value in enumerate(symptoms):
    # Formatting: "fever" -> "Fever" or "skin_rash" -> "Skin Rash"
    symptom = " ".join([i.capitalize() for i in value.split("_")])
    symptom_index[symptom] = index

data_dict = {
    "symptom_index": symptom_index,
    "predictions_classes": classes
}

with open("data_dict.pkl", "wb") as f:
    pickle.dump(data_dict, f)

print("Models and data dictionary have been saved.")
