from fastapi import FastAPI
import joblib
import numpy as np
import pickle
import statistics

# FastAPI App initialisieren
app = FastAPI()

# Modelle und Data Dictionary laden
final_svm_model = joblib.load("train_model/final_svm_model.pkl")
final_nb_model = joblib.load("train_model/final_nb_model.pkl")
final_rf_model = joblib.load("train_model/final_rf_model.pkl")

with open("train_model/data_dict.pkl", "rb") as f:
    data_dict = pickle.load(f)

# Funktion zur Krankheitsvorhersage
def predictDisease(symptoms):
    symptoms = [s.strip().capitalize() for s in symptoms]
    
    input_data = [0] * len(data_dict["symptom_index"])
    for symptom in symptoms:
        if symptom in data_dict["symptom_index"]:
            index = data_dict["symptom_index"][symptom]
            input_data[index] = 1
    
    input_data = np.array(input_data).reshape(1, -1)
    
    rf_prediction = data_dict["predictions_classes"][final_rf_model.predict(input_data)[0]]
    nb_prediction = data_dict["predictions_classes"][final_nb_model.predict(input_data)[0]]
    svm_prediction = data_dict["predictions_classes"][final_svm_model.predict(input_data)[0]]

    final_prediction = statistics.mode([rf_prediction, nb_prediction, svm_prediction])

    return {
        "rf_model_prediction": rf_prediction,
        "naive_bayes_prediction": nb_prediction,
        "svm_model_prediction": svm_prediction,
        "final_prediction": final_prediction
    }

# API-Endpunkt für die Vorhersage
@app.post("/predict")
async def predict(symptoms: list):
    result = predictDisease(symptoms)
    return result

# Starte den Server mit: uvicorn backend:app --reload
